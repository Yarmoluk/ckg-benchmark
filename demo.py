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


def main():
    print(f"\nQ: {QUESTION}\n")
    ask(SYSTEM_RAW, "qwen3:8b — no CKG (raw)")
    ask(SYSTEM_CKG, "qwen3:8b + hardware security CKG")
    print("\n" + "="*60)
    print("  Raw: improvised — no node IDs, no traceable path")
    print("  CKG: declared edges only — every hop is a sourced node")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
