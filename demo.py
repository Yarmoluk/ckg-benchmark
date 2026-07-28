"""
CKG Demo — same 8B model, same question, two runs.
Run: python3 demo.py
Requires: ollama running locally (ollama serve) + qwen3:8b pulled
"""

import urllib.request, json, pathlib, textwrap

OLLAMA = "http://localhost:11434/api/generate"
MODEL  = "qwen3:8b"
CKG    = pathlib.Path(__file__).parent / "demo" / "hardware_security_ckg.md"

QUESTION = (
    "How does a hardware attacker get modified firmware to run past secure boot? "
    "Be specific about the attack path, lab tool used, and the countermeasure."
)

SYSTEM_RAW = "You are a hardware security expert. Answer concisely."

SYSTEM_CKG = (
    "You are a hardware security expert. "
    "The following Compressed Knowledge Graph declares the verified relationships in this domain. "
    "Traverse declared edges only — cite every node ID you use. Do not invent connections.\n\n"
    + CKG.read_text()
)


def ask(system, label):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print('='*60)
    payload = json.dumps({
        "model": MODEL,
        "system": system,
        "prompt": QUESTION,
        "stream": False,
        "options": {"temperature": 0}
    }).encode()
    req = urllib.request.Request(OLLAMA, data=payload,
                                  headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.load(r)
    print(textwrap.fill(resp["response"].strip(), width=72))


NEXT_STEPS = """
What you just ran:
  A hand-built 12-node CKG loaded as plain text into the model's context.
  That's the format. The extraction is what Graphify.md provides.

In production the flow is different:

  pip install ckg-mcp          # MCP server — 97 domains, pre-built

  Then in any MCP-compatible client (Claude Desktop, Cursor, etc.):

    list_domains()             → see all available domains
    search_concepts("fault injection")   → resolve exact node label
    query_ckg("Fault Injection Attack")  → subgraph: node + edges
    get_prerequisites("Secure Boot Bypass") → full upstream chain

  The agent traverses the graph via tool calls instead of receiving
  a context blob. No CSV, no prompt engineering, no manual CKG file.
  The extraction, verification, and SHA-256 source provenance per node
  are done once by Graphify.md — you query the result.

  graphifymd.com  ·  pip install ckg-mcp  ·  97 domains live
"""


def main():
    print(f"\nQ: {QUESTION}\n")
    ask(SYSTEM_RAW, "qwen3:8b — no CKG (raw)")
    ask(SYSTEM_CKG, "qwen3:8b + hardware security CKG")
    print("\n" + "="*60)
    print("  Raw: improvised — no node IDs, no traceable path")
    print("  CKG: declared edges only — every hop is a sourced node")
    print("="*60)
    print(NEXT_STEPS)


if __name__ == "__main__":
    main()
