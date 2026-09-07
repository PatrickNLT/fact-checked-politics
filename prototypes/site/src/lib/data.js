// PROTOTYPE — throwaway. Reads the ADR 0005 files under ../data and hands the pages
// plain objects. The real build will want a schema check and a proper parser; this one
// throws on a malformed header and stops there.

import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..", "..", "data");

const readJson = (...p) => JSON.parse(readFileSync(join(root, ...p), "utf8"));

// A person's registry entry carries `first_name` and `last_name`; a `narration` Speaker
// carries a plain `name`. Both the display name and the sort key are derived from that,
// so nothing has to guess where a surname starts — "Marine Le Pen" files under L because
// `last_name` says so, not because a particle list worked it out.
export const displayName = (s) =>
  s.name ?? [s.first_name, s.last_name].filter(Boolean).join(" ");

export const sortKey = (s) =>
  s.last_name ? `${s.last_name} ${s.first_name ?? ""}`.trim() : displayName(s);

export const speakers = Object.fromEntries(
  readdirSync(join(root, "speakers")).map((f) => {
    const s = readJson("speakers", f);
    return [s.id, s];
  }),
);

export const sources = Object.fromEntries(
  readdirSync(join(root, "sources")).map((f) => {
    const s = readJson("sources", f);
    return [s.id, s];
  }),
);

const HEADER =
  /^### (s\d+) ([a-z0-9-]+) (\d\d:\d\d:\d\d\.\d\d\d) --> (\d\d:\d\d:\d\d\.\d\d\d) text:(draft|verified) speaker:(draft|verified)( overlap)?$/;

const seconds = (hms) => {
  const [h, m, s] = hms.split(":");
  return Number(h) * 3600 + Number(m) * 60 + Number(s);
};

function parseTranscript(md) {
  const body = md.replace(/^---\n[\s\S]*?\n---\n/, "");
  const segments = [];
  for (const block of body.split("\n\n")) {
    const trimmed = block.trim();
    if (!trimmed) continue;
    const [head, ...rest] = trimmed.split("\n");
    const m = HEADER.exec(head);
    if (!m) throw new Error(`transcript.md: bad Segment header\n${head}`);
    segments.push({
      id: m[1],
      speaker: m[2],
      start: seconds(m[3]),
      end: seconds(m[4]),
      startLabel: m[3].slice(0, 8),
      textStatus: m[5],
      speakerStatus: m[6],
      overlap: Boolean(m[7]),
      text: rest.join(" ").trim(),
    });
  }
  return segments;
}

// Colours are the prototype's own, one per participant, so the eye can follow a voice.
// Nothing in the data model says a Speaker has a colour; if a variant wins, whether the
// site colours speakers at all is a spec question.
const PALETTE = [
  "#1f6feb", "#8250df", "#bf3989", "#cf222e", "#9a6700",
  "#1a7f37", "#0e7490", "#7d4e00", "#57606a", "#6e7781",
];

export function appearance(id) {
  const meta = readJson("appearances", id, "appearance.json");
  const segments = parseTranscript(
    readFileSync(join(root, "appearances", id, "transcript.md"), "utf8"),
  );
  const words = readJson("appearances", id, "words.json").segments;

  const participants = meta.participants.map((p, i) => {
    const registry = speakers[p.speaker];
    const candidate = Boolean(registry?.candidacy && !registry.candidacy.ended_on);
    const own = segments.filter((s) => s.speaker === p.speaker);
    const label = p.label ?? p.speaker;
    return {
      ...p,
      name: registry ? displayName(registry) : label,
      // An Appearance-scoped Speaker has no registry entry, so its label is its sort key.
      sortName: registry ? sortKey(registry) : label,
      kind: registry?.kind ?? null,
      party: registry?.party ?? null,
      candidate,
      colour: PALETTE[i % PALETTE.length],
      segmentCount: own.length,
      speakingSeconds: own.reduce((t, s) => t + (s.end - s.start), 0),
    };
  });

  const byId = Object.fromEntries(participants.map((p) => [p.speaker, p]));
  const embedded = meta.replays.find((r) => r.embedded) ?? null;

  return {
    meta,
    segments,
    words,
    participants,
    participantsById: byId,
    embedded,
    source: sources[meta.source] ?? null,
    // Every Segment's text is machine-produced until a human has checked it (AI Act art. 50).
    reviewed: {
      text: segments.filter((s) => s.textStatus === "verified").length,
      speaker: segments.filter((s) => s.speakerStatus === "verified").length,
      total: segments.length,
    },
  };
}

export function appearanceIds() {
  return readdirSync(join(root, "appearances"));
}

// A Candidate's appearances: every Appearance they are a participant of.
export function appearancesOf(speakerId) {
  return appearanceIds()
    .map((id) => appearance(id))
    .filter((a) => a.meta.participants.some((p) => p.speaker === speakerId));
}

export function candidates() {
  return Object.values(speakers).filter((s) => s.candidacy);
}

export const clock = (t) => {
  const s = Math.floor(t);
  const h = Math.floor(s / 3600);
  const m = String(Math.floor((s % 3600) / 60)).padStart(2, "0");
  const sec = String(s % 60).padStart(2, "0");
  return h ? `${h}:${m}:${sec}` : `${m}:${sec}`;
};

// Words the recogniser was unsure of, for the correction hint. Only ever read for a
// Segment whose text is still draft (ADR 0005: words.json is dropped on verification).
export const shakyWords = (words, id, threshold = 0.5) =>
  new Set((words[id] ?? []).filter((w) => w.p < threshold).map((w) => w.w));
