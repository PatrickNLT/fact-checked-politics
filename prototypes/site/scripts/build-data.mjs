// PROTOTYPE — throwaway. Converts the transcription prototype's output (issue #13,
// branch claude/issue-13-1a8681) into the ADR 0005 file layout, so the site prototype
// reads the real data model rather than a mock. The real importer is the bridge ticket (#15);
// this script is not it, and is deleted with the rest of the prototype.
//
// Run: node scripts/build-data.mjs

import { readFileSync, writeFileSync, mkdirSync, rmSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const out = join(here, "..", "data");
const APPEARANCE = "2026-08-27-lci-debat-medef";

const raw = JSON.parse(readFileSync(join(here, "input-transcript.json"), "utf8"));

// --- cluster -> speaker id -------------------------------------------------
// From prototypes/transcription/speakers-map.json (issue #13). Named voices get a
// registry id; unnamed ones get an Appearance-scoped `<role>-<n>` id; noise is dropped.
const CLUSTERS = {
  SPEAKER_16: { speaker: "gabriel-attal", confirmed: true, cue: "quand j'étais Premier ministre, j'ai pris une mesure" },
  SPEAKER_06: { speaker: "raphael-glucksmann", confirmed: true, cue: "au Parlement européen, je me suis battu ; Gigafactory de Fos-sur-Mer (00:08:07)" },
  SPEAKER_12: { speaker: "marine-le-pen", confirmed: true, cue: "baisser la TVA de 20 à 5,5 sur l'énergie (02:05:08)" },
  SPEAKER_09: { speaker: "jean-luc-melenchon", confirmed: true, cue: "l'économie monde va prendre de rudes chocs ; la planification écologique (00:15:16)" },
  SPEAKER_07: { speaker: "edouard-philippe", confirmed: true, cue: "je suis content de savoir ce que j'écris (02:23:33)" },
  SPEAKER_02: { speaker: "bruno-retailleau", confirmed: true, cue: "quatre cotisants pour un retraité ; j'assumerai un âge légal (01:00:00)" },
  SPEAKER_14: { speaker: "marine-tondelier", confirmed: true, cue: "conseillère régionale des Hauts-de-France; addressed as Tondelier at 02:08:37" },
  SPEAKER_13: { speaker: "amelie-carrouer", confirmed: true, cue: "moderates throughout, 14.6 min" },
  SPEAKER_01: { speaker: "patrick-martin", confirmed: true, cue: "MEDEF president, opening address at 00:01:11" },
  SPEAKER_03: { speaker: "eric-malenfer", confirmed: false, cue: "thanked by name at 00:25:41 after the pensions question" },
  SPEAKER_05: { speaker: "vincent-furlan", confirmed: false, cue: "introduces himself, membre du COMEX 40, at 01:38:59" },
  SPEAKER_00: { speaker: "colombe-lecoufle", confirmed: false, cue: "orchid grower, payslips question at 02:07:07" },
  SPEAKER_10: { speaker: "questioner-2", confirmed: false, cue: "question at 01:03:18" },
  SPEAKER_11: { speaker: "questioner-3", confirmed: false, cue: "question at 02:33:43" },
  SPEAKER_04: { speaker: "lci-voix-off", confirmed: false, cue: "LCI opening narration, 00:00:00" },
  SPEAKER_15: { speaker: null, confirmed: true, cue: "jingle, hallucinated caption credit at 00:00:08" },
  SPEAKER_08: { speaker: null, confirmed: true, cue: "jingle fragments at 00:00:03" },
};

const PARTICIPANTS = [
  { speaker: "gabriel-attal" },
  { speaker: "raphael-glucksmann" },
  { speaker: "marine-le-pen" },
  { speaker: "jean-luc-melenchon" },
  { speaker: "edouard-philippe" },
  { speaker: "bruno-retailleau" },
  { speaker: "marine-tondelier" },
  { speaker: "amelie-carrouer", role: "journalist" },
  { speaker: "patrick-martin", role: "host" },
  { speaker: "eric-malenfer", role: "questioner" },
  { speaker: "colombe-lecoufle", role: "questioner" },
  { speaker: "vincent-furlan", role: "questioner" },
  { speaker: "questioner-2", role: "questioner", label: "Chef d'entreprise (01:03)" },
  { speaker: "questioner-3", role: "questioner", label: "Chef d'entreprise (02:33)" },
  { speaker: "lci-voix-off", role: "narration" },
];

// --- the one applied correction -------------------------------------------
// The attribution check of issue #13 (out/sample/attribution-check.txt) covers Segments
// 992..1024. It is the only human review that exists, so it is the only source of
// `verified` statuses here. Everything else stays `draft`, which is the point: the page
// has to look right when almost nothing has been reviewed yet.
const attribution = new Map();
for (const line of readFileSync(join(here, "input-attribution-check.txt"), "utf8").split("\n")) {
  if (!line.trim() || line.startsWith("#")) continue;
  const [verdict, id, , emitted] = line.split("\t");
  attribution.set(Number(id), { verdict: verdict.trim(), emitted });
}

// The hand-corrected reference (out/sample/reference-text.txt) is one line per breath,
// not one per Segment, so it cannot be mapped back Segment by Segment. Only the merge the
// data model itself predicts is applied: s1092 ("C") was cut off Tondelier's turn by
// boundary slop, the attribution check says 1000 (= s1092) is really SPEAKER_14, so it is
// re-attributed and merged into s1093. Lower id survives, s1093 is retired.
const MERGE = { survivor: 1092, retired: 1093, speaker: "marine-tondelier" };

// --- build the Segments ----------------------------------------------------
const removed = { noise: 0, hallucination: 0 };
const segments = [];

raw.segments.forEach((seg, index) => {
  const cluster = CLUSTERS[seg.speaker];
  if (!cluster || cluster.speaker === null) {
    removed.noise += 1;
    return;
  }
  const check = attribution.get(index);
  let speaker = cluster.speaker;
  let speakerStatus = "draft";
  let bothVoices = false;
  if (check) {
    if (check.verdict === "ok") speakerStatus = "verified";
    else if (check.verdict === "both") { speakerStatus = "verified"; bothVoices = true; }
    else { speaker = CLUSTERS[check.verdict].speaker; speakerStatus = "verified"; }
  } else if (!cluster.confirmed) {
    // An unconfirmed cluster leaves its Segments' speaker status draft (ADR 0005).
    speakerStatus = "draft";
  }
  segments.push({
    id: index,
    speaker,
    start: seg.start,
    end: seg.end,
    text: seg.text.trim(),
    words: seg.words ?? [],
    textStatus: "draft",
    speakerStatus,
    bothVoices,
  });
});

const byId = new Map(segments.map((s) => [s.id, s]));

// Apply the merge.
const survivor = byId.get(MERGE.survivor);
const retired = byId.get(MERGE.retired);
if (survivor && retired) {
  survivor.speaker = MERGE.speaker;
  survivor.text = `${survivor.text}${retired.text}`;
  survivor.end = retired.end;
  survivor.words = [...survivor.words, ...retired.words];
  // Checked against the replay at the timestamp while doing the attribution pass.
  survivor.textStatus = "verified";
  survivor.speakerStatus = "verified";
  survivor.bothVoices = survivor.bothVoices || retired.bothVoices;
  segments.splice(segments.indexOf(retired), 1);
  byId.delete(MERGE.retired);
}

// Overlap flag: a Segment whose range intersects another Segment of a different Speaker.
segments.sort((a, b) => a.start - b.start || a.id - b.id);
for (let i = 0; i < segments.length; i += 1) {
  for (let j = i + 1; j < segments.length && segments[j].start < segments[i].end; j += 1) {
    if (segments[i].speaker !== segments[j].speaker) {
      segments[i].overlap = true;
      segments[j].overlap = true;
    }
  }
  if (segments[i].bothVoices) segments[i].overlap = true;
}

// --- write transcript.md ---------------------------------------------------
const hms = (t) => {
  const ms = Math.round((t % 1) * 1000);
  const s = Math.floor(t);
  return [Math.floor(s / 3600), Math.floor((s % 3600) / 60), s % 60]
    .map((n) => String(n).padStart(2, "0"))
    .join(":") + "." + String(ms).padStart(3, "0");
};

const blocks = segments.map((s) => {
  const flags = s.overlap ? " overlap" : "";
  return `### s${s.id} ${s.speaker} ${hms(s.start)} --> ${hms(s.end)} text:${s.textStatus} speaker:${s.speakerStatus}${flags}\n${s.text}`;
});

const appearanceDir = join(out, "appearances", APPEARANCE);
rmSync(out, { recursive: true, force: true });
mkdirSync(appearanceDir, { recursive: true });
mkdirSync(join(out, "speakers"), { recursive: true });
mkdirSync(join(out, "sources"), { recursive: true });

writeFileSync(
  join(appearanceDir, "transcript.md"),
  `---\nschema: fcp/1\nappearance: ${APPEARANCE}\n---\n\n${blocks.join("\n\n")}\n`,
);

// --- words.json: only Segments whose text is still draft -------------------
const words = {};
for (const s of segments) {
  if (s.textStatus === "verified") continue;
  words[`s${s.id}`] = s.words.map((w) => {
    const entry = { w: w.w, s: Math.round(w.s * 100) / 100, e: Math.round(w.e * 100) / 100, p: w.p };
    return entry;
  });
}
writeFileSync(
  join(appearanceDir, "words.json"),
  JSON.stringify({ schema: "fcp/1", appearance: APPEARANCE, segments: words }),
);

// --- appearance.json -------------------------------------------------------
const clusterMap = {};
for (const [label, c] of Object.entries(CLUSTERS)) {
  clusterMap[label] = { speaker: c.speaker, confirmed: c.confirmed, cue: c.cue };
}

writeFileSync(
  join(appearanceDir, "appearance.json"),
  JSON.stringify(
    {
      schema: "fcp/1",
      id: APPEARANCE,
      catalogue_row: "D1",
      title: "Débat MEDEF (REF 2026) des candidats à la présidentielle 2027",
      date: "2026-08-27",
      start_time: "16:45",
      language: "fr",
      source: "lci",
      medium: "tv",
      programme: "Le grand débat du Medef sur LCI",
      organiser: "medef",
      venue: "Court Philippe-Chatrier, Roland-Garros, Paris",
      participants: PARTICIPANTS,
      timeline: {
        platform: "youtube",
        video_id: "rpURHoN54bQ",
        url: "https://www.youtube.com/watch?v=rpURHoN54bQ",
        uploader: "LCI",
        duration_s: 11055,
      },
      replays: [
        {
          platform: "youtube", video_id: "z0gJwsrODEw",
          url: "https://www.youtube.com/watch?v=z0gJwsrODEw",
          uploader: "MEDEF", carrier: "medef",
          offset_s: null, embeddable: true, embedded: true,
          embed_check: { method: "playableInEmbed", result: true, checked_on: "2026-09-05" },
          tdm_signals: "none published by MEDEF; YouTube ToS", cgu_version: null, expiry: null,
        },
        {
          platform: "youtube", video_id: "rpURHoN54bQ",
          url: "https://www.youtube.com/watch?v=rpURHoN54bQ",
          uploader: "LCI", carrier: "lci",
          offset_s: 0, embeddable: false, embedded: false,
          embed_check: { method: "playableInEmbed", result: false, checked_on: "2026-09-05" },
          tdm_signals: "TF1 CGU art. 9, tdmrep", cgu_version: "TF1 Info CGU 2025-10-27", expiry: null,
        },
        {
          platform: "tf1plus", video_id: null, url: null, uploader: "TF1", carrier: "tf1",
          offset_s: null, embeddable: false, embedded: false, account_wall: true,
          expiry: "days to weeks",
        },
      ],
      acquisition: {
        basis: "tolerated", fetch_date: "2026-09-06", method: "download",
        tool: "yt-dlp 2026.08.19, logged out, format 140 audio only",
        media_sha256: raw.provenance.media_sha256,
        media_bytes: raw.provenance.media_bytes,
        deletion_date: "held, prototype stage (ADR 0003 amendment of 2026-09-06)",
      },
      pipeline: {
        asr: { model: raw.pipeline.asr.model, library: "mlx-whisper 0.4.3", run_at: raw.pipeline.asr.run_at },
        diarization: { model: raw.pipeline.diarization.model, library: "pyannote.audio 4.0.7", run_at: raw.pipeline.diarization.run_at, speaker_count_hint: null },
        merge: { rule: "most-overlap-ties-shorter/1", run_at: raw.pipeline.merge_run_at },
        gaps_repaired: 12,
        segments_removed: { noise: removed.noise, hallucination: 0 },
      },
      clusters: clusterMap,
      segments: { next_id: raw.segments.length, retired: { [`s${MERGE.retired}`]: `s${MERGE.survivor}` } },
    },
    null,
    1,
  ),
);

// --- registries ------------------------------------------------------------
// Candidacies as the seed catalogue (data/catalogue/seed.md, read 2026-09-05) records them.
const REF_ELECTION = {
  list: "wikipedia-fr",
  url: "https://fr.wikipedia.org/wiki/Candidatures_à_l'élection_présidentielle_française_de_2027",
};
const cand = (contest, listed_on) => ({
  contest, listed_on, reference: REF_ELECTION, read_on: "2026-09-05", ended_on: null, end_reason: null,
});

// A person carries `first_name` and `last_name`, never a single `name`: the display name
// is derived from them and sorting uses `last_name` directly, instead of guessing where a
// surname starts (Marine Le Pen would file under P). A `narration` Speaker is not a person
// and carries a plain `name`.
const SPEAKERS = {
  "gabriel-attal": { first_name: "Gabriel", last_name: "Attal", party: "Renaissance", candidacy: cand("election", "2026-05-22") },
  "raphael-glucksmann": { first_name: "Raphaël", last_name: "Glucksmann", party: "Place publique", candidacy: cand("primaire socialiste", "2026-08-23") },
  "marine-le-pen": { first_name: "Marine", last_name: "Le Pen", party: "Rassemblement national", candidacy: cand("election", "2026-07-07") },
  "jean-luc-melenchon": { first_name: "Jean-Luc", last_name: "Mélenchon", party: "La France insoumise", candidacy: cand("election", "2026-05-03") },
  "edouard-philippe": { first_name: "Édouard", last_name: "Philippe", party: "Horizons", candidacy: cand("election", "2024-09-03") },
  "bruno-retailleau": { first_name: "Bruno", last_name: "Retailleau", party: "Les Républicains", candidacy: cand("election", "2026-04-19") },
  "marine-tondelier": { first_name: "Marine", last_name: "Tondelier", party: "Les Écologistes", candidacy: cand("primaire de la gauche unie", "2025-10-22") },
  "amelie-carrouer": { first_name: "Amélie", last_name: "Carrouër", party: null },
  "patrick-martin": { first_name: "Patrick", last_name: "Martin", party: null },
  "eric-malenfer": { first_name: "Éric", last_name: "Malenfer", party: null },
  "colombe-lecoufle": { first_name: "Colombe", last_name: "Lecoufle", party: null },
  "vincent-furlan": { first_name: "Vincent", last_name: "Furlan", party: null },
  "lci-voix-off": { name: "Voix off LCI", party: null, kind: "narration" },
};

for (const [id, s] of Object.entries(SPEAKERS)) {
  const file = { schema: "fcp/1", id, kind: s.kind ?? "person" };
  if (s.name) file.name = s.name;
  else { file.first_name = s.first_name; file.last_name = s.last_name; }
  file.party = s.party;
  if (s.candidacy) file.candidacy = s.candidacy;
  writeFileSync(join(out, "speakers", `${id}.json`), JSON.stringify(file, null, 1));
}

for (const [id, s] of Object.entries({
  lci: {
    name: "LCI", group: "TF1", kind: "tv", default_acquisition_basis: "tolerated",
    tdm_opposition: { status: "express", where: "CGU TF1 Info art. 9; CG TF1+ I.10; tdmrep.json", checked_on: "2026-09-05" },
    embed_policy: { own_player: "personal sites only", platform_copies: "YouTube, embeddable per video" },
    replay_durability: "TF1+ days to weeks; YouTube open-ended", notice: null,
  },
  medef: {
    name: "MEDEF", group: null, kind: "organiser", default_acquisition_basis: "tolerated",
    tdm_opposition: { status: "none published", where: "no CGU clause and no tdmrep found", checked_on: "2026-09-05" },
    embed_policy: { own_player: null, platform_copies: "YouTube, embeddable per video" },
    replay_durability: "YouTube open-ended", notice: null,
  },
})) {
  writeFileSync(join(out, "sources", `${id}.json`), JSON.stringify({ schema: "fcp/1", id, ...s }, null, 1));
}

const verified = segments.filter((s) => s.speakerStatus === "verified").length;
console.log(
  `${segments.length} Segments written (${removed.noise} noise Segments dropped, ` +
    `${verified} with a verified speaker, ${segments.filter((s) => s.textStatus === "verified").length} with verified text, ` +
    `${segments.filter((s) => s.overlap).length} flagged overlap).`,
);
