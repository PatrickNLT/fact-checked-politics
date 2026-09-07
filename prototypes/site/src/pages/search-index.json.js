// PROTOTYPE — throwaway. One JSON blob of every Segment, so the search page can filter
// in the browser. At one Appearance this is ~400 kB and fine; the real site has to choose
// between Pagefind (a built index, chunked) and something like this, and that choice is a
// spec question the prototype only frames.
import { appearanceIds, appearance } from "../lib/data.js";

export function GET() {
  const rows = [];
  for (const id of appearanceIds()) {
    const a = appearance(id);
    for (const s of a.segments) {
      const p = a.participantsById[s.speaker];
      rows.push({
        i: s.id,
        a: id,
        at: a.meta.title,
        d: a.meta.date,
        s: p.name,
        c: p.candidate,
        col: p.colour,
        t: s.text,
        st: s.start,
        tv: s.textStatus === "verified",
        sv: s.speakerStatus === "verified",
      });
    }
  }
  return new Response(JSON.stringify(rows), {
    headers: { "content-type": "application/json" },
  });
}
