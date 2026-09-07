// PROTOTYPE - throwaway. Rendered on demand (node adapter) so `?variant=` is read per
// request: a prerendered page would bake variant A into the HTML and the switcher would
// do nothing.
import { defineConfig } from "astro/config";
import node from "@astrojs/node";

export default defineConfig({
  output: "server",
  adapter: node({ mode: "standalone" }),
  server: { port: 4321 },
  devToolbar: { enabled: false },
});
