# MicroSim Screenshot TODO

This file tracks MicroSims that still need preview screenshots captured. The
three workflow sims (`workflow-rag`, `workflow-graphrag`, `workflow-ckg`)
render their previews from their committed Mermaid source via
`@mermaid-js/mermaid-cli`; see `docs/sims/workflow-*/diagram.mmd`.

## Missing Screenshots

### Architecture Comparison — logged 2026-04-17

`architecture-comparison` is an interactive p5.js sim, so its preview needs a
headless-browser capture rather than a static render.

```bash
~/.local/bin/bk-capture-screenshot docs/sims/architecture-comparison
```

If the screenshot capture tool is not installed, any manual capture of
`docs/sims/architecture-comparison/main.html` saved as
`architecture-comparison.png` in the same directory will satisfy the index
page's card image requirement.
