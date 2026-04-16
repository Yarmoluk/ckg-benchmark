"""
Minimal OpenAI-compatible embedding server using sentence-transformers.

Exposes POST /v1/embeddings so GraphRAG (and anything else expecting
an OpenAI embedding endpoint) can use local sentence-transformer models
without an OpenAI API key.

Usage:
    python evaluation/embed_server.py               # default port 4001
    python evaluation/embed_server.py --port 4001
    python evaluation/embed_server.py --model all-mpnet-base-v2

GraphRAG settings.yaml:
    embedding_models:
      default_embedding_model:
        model_provider: openai
        model: text-embedding-ada-002
        api_key: local-key
        api_base: http://localhost:4001
"""

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
_model = None


def get_model(name: str) -> SentenceTransformer:
    global _model, MODEL_NAME
    if _model is None or MODEL_NAME != name:
        print(f"Loading {name}...")
        _model = SentenceTransformer(name)
        MODEL_NAME = name
    return _model


class EmbedHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        import sys
        print(f"  [{self.command}] {self.path}", file=sys.stderr)

    def do_POST(self):
        if self.path not in ("/v1/embeddings", "/embeddings"):
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length))
        texts  = body.get("input", [])
        if isinstance(texts, str):
            texts = [texts]

        model  = get_model(MODEL_NAME)
        vecs   = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)

        data = [
            {"object": "embedding", "index": i, "embedding": v.tolist()}
            for i, v in enumerate(vecs)
        ]
        resp = {
            "object": "list",
            "data":   data,
            "model":  MODEL_NAME,
            "usage":  {"prompt_tokens": sum(len(t.split()) for t in texts),
                       "total_tokens":  sum(len(t.split()) for t in texts)},
        }
        resp_bytes = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(resp_bytes))
        self.end_headers()
        self.wfile.write(resp_bytes)

    def do_GET(self):
        if self.path in ("/health", "/"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        elif self.path in ("/v1/models", "/models"):
            # GraphRAG validates the embedding model before indexing
            resp = json.dumps({
                "object": "list",
                "data": [{"id": "text-embedding-ada-002", "object": "model",
                           "owned_by": "local"}]
            }).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", len(resp))
            self.end_headers()
            self.wfile.write(resp)
        else:
            self.send_response(404)
            self.end_headers()


def main():
    global MODEL_NAME
    parser = argparse.ArgumentParser()
    parser.add_argument("--port",  type=int, default=4001)
    parser.add_argument("--model", default=MODEL_NAME)
    args = parser.parse_args()

    MODEL_NAME = args.model
    get_model(MODEL_NAME)   # preload

    server = HTTPServer(("localhost", args.port), EmbedHandler)
    print(f"Embedding server ready on http://localhost:{args.port}/v1/embeddings")
    print(f"Model: {MODEL_NAME}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
