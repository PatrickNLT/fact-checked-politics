#!/usr/bin/env python3
"""PROTOTYPE (issue #37): throwaway check-worthiness probe on one French debate transcript.

Answers: can the check-worthy factual claims in a French televised debate be identified well
enough to seed a human review queue, and how many are there in one debate? Is the result a
triage aid (a human reads a ranked shortlist) or a full manual read (a human reads everything
anyway)?

Not production code. No tests, no error handling beyond what makes it run. The validated
decisions feed the v3 gate (#29); the code itself stays on this throwaway branch.

Input is `transcript.json` as the transcription prototype (#13) emitted it, on branch
claude/issue-13-1a8681 under prototypes/transcription/out/.

Steps (each a subcommand, each writes into --out):

  sample     seeded uniform draw of N Segments -> out/gold/round1.json   (round 1: the blind
             gold set; drawn BEFORE any model runs, which is what keeps precision/recall honest)
  page       build the self-contained labelling page from a sample -> out/gold/<id>.html
  detect     run one arm over every Segment -> out/detect/<arm>.json (Statements keyed by
             Segment id + character offsets, plus tokens, cost and wall-clock)
  shortlist  round 2: the top-k of an arm's ranking, for precision@k -> out/gold/round2-<arm>.json
  score      gold labels x arm outputs -> out/findings.json (P/R/F1 strict and lenient,
             Cohen's kappa, P@k, volume with a Wilson interval, distributions)
  volume     distributions of one arm's full pass, no labels needed

Run:
  uv run probe.py sample --transcript ../transcription/out/transcript.json
  open out/gold/round1.html                     # Patrick labels, exports labels-round1.json
  uv run probe.py detect --arm rules            # free, no API
  uv run probe.py detect --arm haiku            # needs ANTHROPIC_API_KEY or `ant auth login`
  uv run probe.py score --gold out/gold/labels-round1.json
"""

import argparse
import hashlib
import json
import math
import os
import random
import re
import sys
import time
import unicodedata
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE / "out"
DEFAULT_TRANSCRIPT = HERE / "input" / "transcript.json"

APPEARANCE = "2026-08-27-lci-debat-medef"

# Prices are USD per million tokens, from the Claude API docs (read 2026-09-07). The Batch API
# is half these. Token counts are recorded raw as well, so a price change does not invalidate
# a run: rerun `score` and the dollars move, the tokens do not.
ARMS = {
    "rules":  {"kind": "rules",   "model": None,               "in": 0.0, "out": 0.0},
    "haiku":  {"kind": "claude",  "model": "claude-haiku-4-5", "in": 1.0, "out": 5.0},
    "sonnet": {"kind": "claude",  "model": "claude-sonnet-5",  "in": 2.0, "out": 10.0},
    "opus":   {"kind": "claude",  "model": "claude-opus-5",    "in": 5.0, "out": 25.0},
    # Any OpenAI-compatible server on the Mac (LM Studio, llama.cpp, Ollama). --model names it.
    "local":  {"kind": "openai",  "model": None,               "in": 0.0, "out": 0.0},
}
KINDS = ["numerical", "historical", "attributive", "predictive", "other"]
LABELS = ["oui", "limite", "non"]

# The gold draw. Changing either number makes a run incomparable with earlier ones, so they
# are constants here rather than defaults that drift on the command line.
SEED = 20260907
ROUND1_N = 250

CTX_BEFORE, CTX_AFTER = 1, 1        # neighbouring Segments shown to human and model alike
BATCH_TARGETS, BATCH_LEAD = 12, 3   # Segments judged per request, and context Segments before them


# ---------------------------------------------------------------- small helpers

def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def dump(obj, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1))
    print(f"wrote {path} ({path.stat().st_size // 1024} KiB)")


def load(path):
    return json.loads(Path(path).read_text())


def sha8(text):
    return hashlib.sha256(text.encode()).hexdigest()[:8]


def clock(seconds):
    s = int(seconds)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def seg_id(n):
    """The data model writes Segment ids as `s` + counter (docs/data-model.md)."""
    return f"s{n}"


def wilson(k, n, z=1.96):
    """95 % interval for a proportion. Small samples need it; the normal approximation lies."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


# ---------------------------------------------------------------- the transcript

class Transcript:
    """Read-only view of the #13 output, in the vocabulary of CONTEXT.md."""

    def __init__(self, path):
        raw = load(path)
        self.speakers = raw["speakers"]
        self.segments = []
        for s in raw["segments"]:
            who = self.speakers.get(s["speaker"], {})
            self.segments.append({
                "segment": seg_id(s["id"]),
                "n": s["id"],
                "cluster": s["speaker"],
                "speaker": who.get("participant") or s["speaker"],
                "role": who.get("role"),
                "start": s["start"],
                "clock": clock(s["start"]),
                "text": s["text"].strip(),
                "words": len(s["text"].split()),
                "overlap": bool(s.get("overlap_words")),
            })
        self.by_id = {s["segment"]: s for s in self.segments}
        self.index = {s["segment"]: i for i, s in enumerate(self.segments)}

    def context(self, segment):
        i = self.index[segment]
        before = self.segments[i - 1] if i > 0 else None
        after = self.segments[i + 1] if i + 1 < len(self.segments) else None
        return before, after

    def item(self, segment):
        """One Segment as the labelling page and the detector both see it."""
        s = self.by_id[segment]
        before, after = self.context(segment)
        thin = lambda x: x and {"speaker": x["speaker"], "text": x["text"]}
        return {**{k: s[k] for k in
                   ("segment", "speaker", "role", "clock", "text", "words", "overlap")},
                "before": thin(before), "after": thin(after)}


# ---------------------------------------------------------------- sample (round 1)

def cmd_sample(a):
    """Uniform, seeded, over every Segment — including the two-word interjections.

    Not stratified and not filtered: a biased draw would give a biased prevalence, and
    prevalence is the number that sizes the v3 queue. Short Segments cost one keystroke.
    """
    t = Transcript(a.transcript)
    rng = random.Random(SEED)
    picked = sorted(rng.sample([s["segment"] for s in t.segments], a.n),
                    key=lambda sid: t.index[sid])
    sample = {
        "schema": "fcp-claim-sample/0",
        "sample_id": a.sample_id,
        "round": 1,
        "appearance": APPEARANCE,
        "drawn_at": now(),
        "draw": {"method": "uniform without replacement over all Segments",
                 "seed": SEED, "n": a.n, "population": len(t.segments),
                 "before_any_model_ran": True},
        "items": [t.item(sid) for sid in picked],
    }
    dump(sample, Path(a.out) / "gold" / f"{a.sample_id}.json")
    build_page(sample, Path(a.out) / "gold" / f"{a.sample_id}.html")


def build_page(sample, dest):
    tpl = (HERE / "labeller.template.html").read_text()
    guideline = (HERE / "guideline.md").read_text()
    calibration = load(HERE / "calibration.json")["examples"]
    rnd = sample.get("round", 1)
    lede = ("Round 1 of the check-worthiness probe (issue #37). "
            f"{len(sample['items'])} Segments drawn uniformly at random from the "
            f"{sample['draw']['population']} Segments of the MEDEF debate of 27 August 2026, "
            "with seed " + str(sample["draw"]["seed"]) + ". Judge each one against the "
            "guideline: is there a checkable factual claim in it?"
            ) if rnd == 1 else (
            "Round 2 of the check-worthiness probe (issue #37). These are the "
            f"{len(sample['items'])} Segments a machine ranked highest, shuffled and stripped "
            "of every score, so that precision@k can be measured. Same guideline, same "
            "question. You are not told which model, nor what it thought.")
    payload = {
        "sample_id": sample["sample_id"],
        "appearance": sample["appearance"],
        "guideline_sha": sha8(guideline),
        "guideline_html": md_to_html(guideline),
        "calibration": calibration,
        "items": sample["items"],
    }
    html = (tpl.replace("__TITLE__", f"Check-worthy? — {sample['sample_id']}")
               .replace("__LEDE__", lede)
               .replace("__DATA__", json.dumps(payload, ensure_ascii=False)))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    print(f"wrote {dest} ({dest.stat().st_size // 1024} KiB) — open it in a browser")


def md_to_html(md):
    """Just enough Markdown for the guideline panel. A prototype does not need a parser."""
    out, in_ul, in_tbl = [], False, False
    for line in md.split("\n"):
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            tag = "th" if not in_tbl else "td"
            if not in_tbl:
                out.append("<table>")
                in_tbl = True
            out.append("<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cells) + "</tr>")
            continue
        if in_tbl:
            out.append("</table>")
            in_tbl = False
        if line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(line[2:])}</li>")
            continue
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if line.startswith("### "):
            out.append(f"<h3>{inline(line[4:])}</h3>")
        elif line.startswith("## "):
            out.append(f"<h3>{inline(line[3:])}</h3>")
        elif line.startswith("# "):
            out.append(f"<h3>{inline(line[2:])}</h3>")
        elif line.strip():
            out.append(f"<p>{inline(line)}</p>")
    if in_ul:
        out.append("</ul>")
    if in_tbl:
        out.append("</table>")
    return "\n".join(out)


def inline(s):
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    return s


def cmd_page(a):
    build_page(load(a.sample), Path(a.sample).with_suffix(".html"))


# ---------------------------------------------------------------- detect

SYSTEM = """Tu es annoteur pour un projet de fact-checking français. Tu lis la transcription \
automatique d'un débat télévisé entre candidats à l'élection présidentielle de 2027 et tu \
repères les Segments qui contiennent une affirmation factuelle vérifiable.

{guideline}

Pour chaque Segment cible qu'on te donne, réponds :
- `checkworthy` : true si le Segment contient au moins une affirmation vérifiable au sens \
ci-dessus (le cas `oui`), false sinon. Un cas `limite` est false, mais avec une `confidence` \
intermédiaire (autour de 0,5).
- `confidence` : entre 0 et 1, ta certitude que ce Segment mérite la file d'attente humaine. \
C'est ce nombre qui sert à classer les Segments, alors gradue-le vraiment.
- `claims` : pour chaque affirmation, l'extrait `span` **copié mot pour mot** du texte du \
Segment cible (aucune reformulation, aucune correction d'orthographe, aucun ajout de \
ponctuation — la chaîne doit se retrouver telle quelle dans le texte) et son `kind`.
Si `checkworthy` est false, `claims` est une liste vide.

Ne juge que les Segments cibles. Le contexte est là pour te faire comprendre l'échange, pas \
pour être annoté. Réponds pour chaque cible exactement une fois, dans l'ordre donné."""

SCHEMA = {
    "type": "object",
    "properties": {
        "segments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "segment": {"type": "string"},
                    "checkworthy": {"type": "boolean"},
                    "confidence": {"type": "number"},
                    "claims": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "span": {"type": "string"},
                                "kind": {"type": "string", "enum": KINDS},
                            },
                            "required": ["span", "kind"],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["segment", "checkworthy", "confidence", "claims"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["segments"],
    "additionalProperties": False,
}


def batches(t):
    """Rolling windows: BATCH_LEAD Segments of context, then BATCH_TARGETS to judge."""
    segs = t.segments
    for start in range(0, len(segs), BATCH_TARGETS):
        targets = segs[start:start + BATCH_TARGETS]
        lead = segs[max(0, start - BATCH_LEAD):start]
        yield lead, targets


def render_batch(lead, targets):
    lines = []
    if lead:
        lines.append("CONTEXTE (ne pas annoter) :")
        for s in lead:
            lines.append(f"  [{s['clock']}] {s['speaker']} : {s['text']}")
        lines.append("")
    lines.append("SEGMENTS CIBLES :")
    for s in targets:
        lines.append(f"  {s['segment']} [{s['clock']}] {s['speaker']} : {s['text']}")
    return "\n".join(lines)


def locate(span, text):
    """Character offsets of a model's verbatim span, per docs/data-model.md.

    v3 Statements attach to a Segment id and character offsets into the Segment text, never to
    word times. A model cannot count characters, so it returns the span and we find it. How
    often that works is itself a finding — `score` reports the exact / normalised / lost split.
    """
    i = text.find(span)
    if i >= 0:
        return i, i + len(span), "exact"

    def fold(s):
        s = unicodedata.normalize("NFD", s.lower())
        s = "".join(c for c in s if not unicodedata.combining(c))
        return re.sub(r"[^a-z0-9]+", " ", s).strip()

    # Map every folded character back to its offset in the original, then match on the fold.
    flat, back = [], []
    for j, ch in enumerate(text):
        f = fold(ch)
        for c in f:
            flat.append(c)
            back.append(j)
    hay, needle = "".join(flat), fold(span)
    hay = re.sub(r"\s+", " ", hay)
    k = hay.find(needle)
    if k >= 0 and needle:
        end = min(k + len(needle), len(back) - 1)
        return back[k], back[end] + 1, "normalised"
    return None, None, "lost"


def rules_arm(t, _a):
    """Zero-cost lexical floor: does the Segment carry a number, a date or a quantity?

    CheckThat! 2024's official baseline scored F1 0.307 on English debate sentences, and
    QuanTemp's whole point is that political claims are numerical. If an LLM cannot beat this,
    it is not buying anything.
    """
    pat = re.compile(
        r"\d|\bpour ?cent\b|%|\bmilliards?\b|\bmillions?\b|\bmilliers?\b|\bcentaines?\b"
        r"|\bdizaines?\b|\beuros?\b|\bpoints?\b|\bfois plus\b|\bfois moins\b|\bmoiti[ée]\b"
        r"|\bquart\b|\btiers\b|\bdouble\b|\btriple\b|\bpremier\b|\bpremi[èe]re\b|\bdernier\b"
        r"|\brecord\b|\btaux\b|\bpourcentage\b|\bd[ée]ficit\b|\bdette\b|\bch[ôo]mage\b"
        r"|\bcroissance\b|\binflation\b|\bPIB\b|\bsmic\b|\bquinquennat\b|\bmandat\b"
        r"|\bloi de \d|\ben (?:19|20)\d\d\b|\bdepuis (?:19|20)\d\d\b", re.I)
    statements = []
    for s in t.segments:
        hits = list(pat.finditer(s["text"]))
        if not hits:
            continue
        statements.append({
            "segment": s["segment"], "speaker": s["speaker"], "clock": s["clock"],
            "confidence": min(1.0, 0.4 + 0.15 * len(hits)),
            "claims": [{"start": h.start(), "end": h.end(), "text": h.group(),
                        "kind": "numerical", "located": "exact"} for h in hits[:3]],
        })
    return statements, {"input_tokens": 0, "output_tokens": 0,
                        "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}


def claude_arm(t, a, arm):
    import anthropic

    client = anthropic.Anthropic(max_retries=5)
    guideline = (HERE / "guideline.md").read_text()
    system = [{"type": "text",
               "text": SYSTEM.format(guideline=guideline),
               "cache_control": {"type": "ephemeral"}}]
    model = a.model or ARMS[arm]["model"]
    # Effort is rejected on Haiku 4.5; on Opus 5 / Sonnet 5 a classification pass wants `low`.
    output_config = {"format": {"type": "json_schema", "schema": SCHEMA}}
    if arm != "haiku":
        output_config["effort"] = "low"

    def one(work):
        lead, targets = work
        r = client.messages.create(
            model=model, max_tokens=4096, system=system,
            output_config=output_config,
            messages=[{"role": "user", "content": render_batch(lead, targets)}],
        )
        text = next(b.text for b in r.content if b.type == "text")
        return json.loads(text)["segments"], r.usage

    jobs = list(batches(t))
    print(f"{arm}: {len(jobs)} requests over {len(t.segments)} Segments, model {model}")
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        results = list(pool.map(one, jobs))
    return collect(t, results)


def openai_arm(t, a, arm):
    """Any OpenAI-compatible /chat/completions server, so the Mac-local answer can be measured."""
    guideline = (HERE / "guideline.md").read_text()
    system = SYSTEM.format(guideline=guideline)
    url = a.base_url.rstrip("/") + "/chat/completions"

    def one(work):
        lead, targets = work
        body = json.dumps({
            "model": a.model, "temperature": 0,
            "response_format": {"type": "json_schema",
                                "json_schema": {"name": "checkworthiness",
                                                "strict": True, "schema": SCHEMA}},
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": render_batch(lead, targets)}],
        }).encode()
        req = urllib.request.Request(url, data=body,
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + os.environ.get(
                                                  "LOCAL_API_KEY", "not-needed")})
        with urllib.request.urlopen(req, timeout=600) as r:
            payload = json.loads(r.read())
        parsed = json.loads(payload["choices"][0]["message"]["content"])
        u = payload.get("usage", {})
        return parsed["segments"], type("U", (), {
            "input_tokens": u.get("prompt_tokens", 0),
            "output_tokens": u.get("completion_tokens", 0),
            "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0})()

    jobs = list(batches(t))
    print(f"{arm}: {len(jobs)} requests over {len(t.segments)} Segments, model {a.model}")
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        results = list(pool.map(one, jobs))
    return collect(t, results)


def collect(t, results):
    """Model answers -> Statement records keyed by Segment id and character offsets."""
    statements, usage = [], Counter()
    for answers, u in results:
        for field in ("input_tokens", "output_tokens",
                      "cache_read_input_tokens", "cache_creation_input_tokens"):
            usage[field] += getattr(u, field, 0) or 0
        for ans in answers:
            sid = ans.get("segment")
            if sid not in t.by_id:
                continue
            text = t.by_id[sid]["text"]
            claims = []
            for c in ans.get("claims", []):
                start, end, how = locate(c["span"], text)
                claims.append({"start": start, "end": end,
                               "text": text[start:end] if start is not None else c["span"],
                               "kind": c.get("kind", "other"), "located": how})
            if not ans.get("checkworthy") and not claims:
                # Still recorded when confidence is non-trivial: the ranking needs the tail.
                if float(ans.get("confidence", 0)) < 0.15:
                    continue
            statements.append({
                "segment": sid, "speaker": t.by_id[sid]["speaker"],
                "clock": t.by_id[sid]["clock"],
                "checkworthy": bool(ans.get("checkworthy")),
                "confidence": float(ans.get("confidence", 0)),
                "claims": claims,
            })
    return statements, dict(usage)


def cmd_detect(a):
    t = Transcript(a.transcript)
    arm = ARMS[a.arm]
    t0 = time.time()
    if arm["kind"] == "rules":
        statements, usage = rules_arm(t, a)
    elif arm["kind"] == "claude":
        statements, usage = claude_arm(t, a, a.arm)
    else:
        statements, usage = openai_arm(t, a, a.arm)
    wall = time.time() - t0

    billable_in = usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0)
    usd = (billable_in / 1e6 * arm["in"]
           + usage.get("cache_read_input_tokens", 0) / 1e6 * arm["in"] * 0.1
           + usage.get("output_tokens", 0) / 1e6 * arm["out"])
    audio_h = max(s["start"] for s in t.segments) / 3600
    dump({
        "schema": "fcp-claim-probe/0",
        "appearance": APPEARANCE,
        "arm": a.arm,
        "model": a.model or arm["model"],
        "run_at": now(),
        "guideline_sha": sha8((HERE / "guideline.md").read_text()),
        "config": {"batch_targets": BATCH_TARGETS, "batch_lead": BATCH_LEAD,
                   "workers": a.workers, "segments": len(t.segments)},
        "cost": {**usage, "usd": round(usd, 4), "usd_batch_api": round(usd / 2, 4),
                 "wall_s": round(wall, 1),
                 "wall_s_per_audio_hour": round(wall / audio_h, 1),
                 "usd_per_audio_hour": round(usd / audio_h, 4)},
        "statements": statements,
    }, Path(a.out) / "detect" / f"{a.arm}.json")


# ---------------------------------------------------------------- shortlist (round 2)

def cmd_shortlist(a):
    """The top-k of an arm's ranking, shuffled, for precision@k.

    Round 1 is uniform, so only about a sixth of any top-100 is in it — too thin to answer
    the question the issue actually asks (triage aid or full manual read). This draws the
    shortlist itself. It is shuffled and carries no scores, so the labelling stays blind.
    """
    t = Transcript(a.transcript)
    det = load(Path(a.out) / "detect" / f"{a.arm}.json")
    ranked = sorted(det["statements"], key=lambda s: -s["confidence"])[:a.k]
    ids = [s["segment"] for s in ranked]
    random.Random(SEED + 1).shuffle(ids)
    sample_id = f"round2-{a.arm}"
    dump({
        "schema": "fcp-claim-sample/0", "sample_id": sample_id, "round": 2,
        "appearance": APPEARANCE, "drawn_at": now(),
        "draw": {"method": f"top-{a.k} of the {a.arm} ranking, shuffled",
                 "seed": SEED + 1, "n": len(ids), "population": len(t.segments),
                 "before_any_model_ran": False, "arm": a.arm},
        "items": [t.item(sid) for sid in ids],
    }, Path(a.out) / "gold" / f"{sample_id}.json")
    build_page(load(Path(a.out) / "gold" / f"{sample_id}.json"),
               Path(a.out) / "gold" / f"{sample_id}.html")


# ---------------------------------------------------------------- score

def confusion(gold, pred):
    tp = sum(1 for s in gold if gold[s] and pred.get(s))
    fp = sum(1 for s in gold if not gold[s] and pred.get(s))
    fn = sum(1 for s in gold if gold[s] and not pred.get(s))
    tn = sum(1 for s in gold if not gold[s] and not pred.get(s))
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    n = tp + fp + fn + tn
    po = (tp + tn) / n if n else 0.0
    pe = (((tp + fp) * (tp + fn) + (fn + tn) * (fp + tn)) / (n * n)) if n else 0.0
    kappa = (po - pe) / (1 - pe) if pe < 1 else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": round(prec, 3), "recall": round(rec, 3), "f1": round(f1, 3),
            "accuracy": round(po, 3), "cohens_kappa": round(kappa, 3)}


def cmd_score(a):
    t = Transcript(a.transcript)
    golds = [load(p) for p in a.gold]
    detects = {}
    for p in sorted((Path(a.out) / "detect").glob("*.json")):
        d = load(p)
        detects[d["arm"]] = d

    findings = {"schema": "fcp-claim-findings/0", "appearance": APPEARANCE,
                "scored_at": now(), "population": len(t.segments),
                "guideline_sha": sha8((HERE / "guideline.md").read_text()),
                "rounds": [], "arms": {}}

    round1 = None
    for g in golds:
        judged = {l["segment"]: l["label"] for l in g["labels"] if l["label"]}
        kinds = Counter(l["kind"] for l in g["labels"] if l["kind"])
        c = Counter(judged.values())
        rec = {"sample_id": g["sample_id"], "annotator": g.get("annotator"),
               "judged": len(judged), "of": len(g["labels"]),
               "counts": dict(c), "kinds": dict(kinds)}
        if g["sample_id"].startswith("round1"):
            round1 = judged
            for name, positives in (("strict", {"oui"}), ("lenient", {"oui", "limite"})):
                k = sum(1 for v in judged.values() if v in positives)
                lo, hi = wilson(k, len(judged))
                rec[name] = {
                    "prevalence": round(k / len(judged), 3) if judged else 0,
                    "prevalence_ci95": [round(lo, 3), round(hi, 3)],
                    "volume_estimate": round(k / len(judged) * len(t.segments)) if judged else 0,
                    "volume_ci95": [round(lo * len(t.segments)), round(hi * len(t.segments))],
                }
        findings["rounds"].append(rec)

    for arm, d in detects.items():
        entry = {"model": d["model"], "cost": d["cost"],
                 "flagged": sum(1 for s in d["statements"] if s.get("checkworthy", True)),
                 "statements": sum(len(s["claims"]) for s in d["statements"]),
                 "offsets": dict(Counter(c["located"] for s in d["statements"]
                                         for c in s["claims"])),
                 "kinds": dict(Counter(c["kind"] for s in d["statements"] for c in s["claims"])),
                 "by_speaker": dict(Counter(s["speaker"] for s in d["statements"]
                                            if s.get("checkworthy", True)).most_common()),
                 }
        conf = {s["segment"]: s["confidence"] for s in d["statements"]}
        flag = {s["segment"]: bool(s.get("checkworthy", True)) for s in d["statements"]}

        if round1:
            for name, positives in (("strict", {"oui"}), ("lenient", {"oui", "limite"})):
                gold = {s: (v in positives) for s, v in round1.items()}
                entry[name] = confusion(gold, flag)
                sweep = []
                for th in [x / 20 for x in range(1, 20)]:
                    pred = {s: conf.get(s, 0) >= th for s in gold}
                    m = confusion(gold, pred)
                    sweep.append({"threshold": th, **m})
                best = max(sweep, key=lambda m: m["f1"])
                entry[name + "_best_threshold"] = best
                entry[name + "_sweep"] = sweep

        # precision@k over whatever is labelled, round 2 included; coverage says how much.
        labelled = {}
        for g in golds:
            for l in g["labels"]:
                if l["label"]:
                    labelled[l["segment"]] = l["label"]
        ranked = [s["segment"] for s in sorted(d["statements"], key=lambda s: -s["confidence"])]
        pk = {}
        for k in (10, 25, 50, 100, 200):
            top = ranked[:k]
            seen = [labelled[s] for s in top if s in labelled]
            if not seen:
                continue
            pk[f"p@{k}"] = {
                "labelled": len(seen), "coverage": round(len(seen) / len(top), 2),
                "strict": round(sum(1 for v in seen if v == "oui") / len(seen), 3),
                "lenient": round(sum(1 for v in seen if v in ("oui", "limite")) / len(seen), 3),
            }
        entry["precision_at_k"] = pk
        findings["arms"][arm] = entry

    dump(findings, Path(a.out) / "findings.json")
    report(findings)


def report(f):
    print()
    print(f"Population: {f['population']} Segments, guideline {f['guideline_sha']}")
    for r in f["rounds"]:
        print(f"\n{r['sample_id']}: {r['judged']}/{r['of']} judged  {r['counts']}")
        for name in ("strict", "lenient"):
            if name in r:
                v = r[name]
                print(f"  {name:8} prevalence {v['prevalence']:.1%} "
                      f"[{v['prevalence_ci95'][0]:.1%}, {v['prevalence_ci95'][1]:.1%}]"
                      f"  ->  {v['volume_estimate']} check-worthy Segments in the debate "
                      f"[{v['volume_ci95'][0]}, {v['volume_ci95'][1]}]")
        if r["kinds"]:
            print(f"  kinds: {r['kinds']}")
    if not f["arms"]:
        print("\nNo detector runs yet — `probe.py detect --arm ...` first.")
        return
    print(f"\n{'arm':8} {'model':22} {'flagged':>8} {'P':>6} {'R':>6} {'F1':>6} "
          f"{'kappa':>6} {'USD':>8} {'wall/h':>8}")
    for arm, e in f["arms"].items():
        s = e.get("strict")
        row = (f"{arm:8} {str(e['model'] or '-')[:22]:22} {e['flagged']:8} ")
        row += (f"{s['precision']:6.3f} {s['recall']:6.3f} {s['f1']:6.3f} {s['cohens_kappa']:6.3f} "
                if s else f"{'-':>6} {'-':>6} {'-':>6} {'-':>6} ")
        row += f"{e['cost']['usd']:8.3f} {e['cost']['wall_s_per_audio_hour']:8.0f}"
        print(row)
    print("\nprecision@k (over labelled Segments only; coverage in brackets)")
    for arm, e in f["arms"].items():
        bits = [f"{k} {v['strict']:.2f}/{v['lenient']:.2f} [{v['coverage']:.0%}]"
                for k, v in e["precision_at_k"].items()]
        print(f"  {arm:8} " + "  ".join(bits or ["—"]))
    print("\ncharacter offsets located from the model's verbatim span")
    for arm, e in f["arms"].items():
        print(f"  {arm:8} {e['offsets']}")


# ---------------------------------------------------------------- volume

def cmd_volume(a):
    t = Transcript(a.transcript)
    d = load(Path(a.out) / "detect" / f"{a.arm}.json")
    flagged = [s for s in d["statements"] if s.get("checkworthy", True)]
    spoken = Counter(s["speaker"] for s in t.segments)
    per = defaultdict(int)
    for s in flagged:
        per[s["speaker"]] += 1
    print(f"\n{a.arm} ({d['model']}): {len(flagged)} of {len(t.segments)} Segments flagged "
          f"({len(flagged)/len(t.segments):.1%}), {sum(len(s['claims']) for s in flagged)} claims\n")
    print(f"{'speaker':24} {'flagged':>8} {'segments':>9} {'rate':>7}")
    for who, n in sorted(per.items(), key=lambda kv: -kv[1]):
        print(f"{who[:24]:24} {n:8} {spoken[who]:9} {n/spoken[who]:6.1%}")
    print(f"\nkinds: {dict(Counter(c['kind'] for s in flagged for c in s['claims']))}")
    print(f"cost: {d['cost']}")


# ---------------------------------------------------------------- cli

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default=str(DEFAULT_OUT))
    p.add_argument("--transcript", default=str(DEFAULT_TRANSCRIPT))
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sample", help="seeded uniform draw + labelling page (round 1)")
    s.add_argument("--n", type=int, default=ROUND1_N)
    s.add_argument("--sample-id", default="round1")
    s.set_defaults(fn=cmd_sample)

    s = sub.add_parser("page", help="rebuild a labelling page from a sample file")
    s.add_argument("sample")
    s.set_defaults(fn=cmd_page)

    s = sub.add_parser("detect", help="run one arm over every Segment")
    s.add_argument("--arm", choices=sorted(ARMS), required=True)
    s.add_argument("--model", default=None, help="override the arm's model id (required for local)")
    s.add_argument("--base-url", default="http://localhost:1234/v1", help="local arm only")
    s.add_argument("--workers", type=int, default=4)
    s.set_defaults(fn=cmd_detect)

    s = sub.add_parser("shortlist", help="top-k of an arm's ranking, for precision@k (round 2)")
    s.add_argument("--arm", required=True)
    s.add_argument("--k", type=int, default=100)
    s.set_defaults(fn=cmd_shortlist)

    s = sub.add_parser("score", help="gold labels x every arm -> findings.json")
    s.add_argument("--gold", nargs="+", required=True)
    s.set_defaults(fn=cmd_score)

    s = sub.add_parser("volume", help="distributions of one arm's full pass")
    s.add_argument("--arm", required=True)
    s.set_defaults(fn=cmd_volume)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
