## META
version: 1.0.0
domain: clj-surgeon codebase
description: Compact Knowledge Graph of realgenekim/clj-surgeon — Clojure AST manipulation tool
nodes: 13 namespaces, 74 functions, 13 operations
edges: 47 typed relationships
token_count: 847
benchmark_baseline_full_read: 7308  # 2436 lines × 3 tokens/line avg
benchmark_genekim_ast_outline: 1000  # Gene Kim measured: ~200 tokens/file × 5 files
benchmark_ckg_full_graph: 847
benchmark_ckg_single_query: 52     # avg tokens for a 2-hop traversal answer

## NAMESPACES

[clj-surgeon.core] ORCHESTRATES [clj-surgeon.outline, clj-surgeon.analyze, clj-surgeon.move, clj-surgeon.fix-declares, clj-surgeon.extract, clj-surgeon.rename, clj-surgeon.forward-refs, clj-surgeon.cljc.merge, clj-surgeon.cljc.split, clj-surgeon.cljc.require-ops, clj-surgeon.cljc.analyze]
[clj-surgeon.analyze] DEPENDS-ON [] | LEAF-DEPENDENCY | 398 lines
[clj-surgeon.outline] DEPENDS-ON [clj-surgeon.cljc.walk] | 121 lines
[clj-surgeon.move] DEPENDS-ON [] | LEAF-DEPENDENCY | 110 lines
[clj-surgeon.fix-declares] DEPENDS-ON [clj-surgeon.analyze, clj-surgeon.outline, clj-surgeon.forward-refs] | 322 lines
[clj-surgeon.extract] DEPENDS-ON [clj-surgeon.outline, clj-surgeon.analyze] | 300 lines
[clj-surgeon.rename] DEPENDS-ON [] | LEAF-DEPENDENCY | 235 lines
[clj-surgeon.forward-refs] DEPENDS-ON [] | LEAF-DEPENDENCY | 40 lines
[clj-surgeon.cljc.analyze] DEPENDS-ON [clj-surgeon.cljc.merge, clj-surgeon.cljc.split, clj-surgeon.cljc.walk] | 80 lines
[clj-surgeon.cljc.merge] DEPENDS-ON [] | LEAF-DEPENDENCY | 283 lines
[clj-surgeon.cljc.split] DEPENDS-ON [] | LEAF-DEPENDENCY | 154 lines
[clj-surgeon.cljc.require-ops] DEPENDS-ON [clj-surgeon.cljc.merge, clj-surgeon.cljc.split] | 128 lines
[clj-surgeon.cljc.walk] DEPENDS-ON [] | LEAF-DEPENDENCY | 90 lines

## OPERATIONS (Public API — 13 ops routed through core.clj)

[run-outline] ENTRYPOINT :op :outline | CALLS outline/outline | FILE-IN file
[run-mv] ENTRYPOINT :op :mv | CALLS analyze, move/move-form | FILE-IN file, form, before
[run-declares] ENTRYPOINT :op :fix-declares! | CALLS fix-declares/plan + fix-declares/execute! | FILE-IN file
[run-deps] ENTRYPOINT :op :deps | CALLS analyze/dep-tree | FILE-IN file, form
[run-topo] ENTRYPOINT :op :topo | CALLS analyze/topological-sort | FILE-IN file
[run-closure] ENTRYPOINT :op :closure | CALLS analyze/extraction-closure | FILE-IN file, form
[run-ls-deps] ENTRYPOINT :op :ls-deps | CALLS analyze/intra-ns-deps | FILE-IN file, form
[run-cljc-merge] ENTRYPOINT :op :cljc-merge | CALLS cljc.merge/merge-files | FILE-IN clj, cljs
[run-cljc-split] ENTRYPOINT :op :cljc-split | CALLS cljc.split/split-file | FILE-IN file
[run-cljc-add-require] ENTRYPOINT :op :cljc-add-require | CALLS cljc.require-ops/add-require | FILE-IN file

## FUNCTIONS — clj-surgeon.analyze (Core Analysis Engine)

[file->zloc] PARSES file→zipper-loc | USED-BY analyze, extract, fix-declares, rename
[string->zloc] PARSES string→zipper-loc | USED-BY cljc.analyze
[top-level-forms] EXTRACTS all defn/def/ns forms | USED-BY outline, move, fix-declares
[symbols-in-form] EXTRACTS symbol refs in a form | USED-BY intra-ns-deps
[qualified-symbols] EXTRACTS ns-qualified symbols | USED-BY dep-tree
[parse-ns-aliases] EXTRACTS :require alias map | USED-BY intra-ns-deps, dep-tree
[intra-ns-deps] COMPUTES within-ns dependency map | USED-BY fix-declares, run-ls-deps
[extraction-closure] COMPUTES transitive deps for extraction | USED-BY run-closure
[dep-tree] BUILDS dependency tree for a form | USED-BY run-deps
[flatten-dep-tree] FLATTENS dep-tree to ordered list | USED-BY topological-sort
[topological-sort] SORTS forms by dependency order | USED-BY run-topo, fix-declares
[unreferenced-forms] FINDS orphan defs | USED-BY extract

## FUNCTIONS — clj-surgeon.outline

[outline] RETURNS {:ns :forms [{:type :name :args :doc :line}]} | USED-BY run-outline, extract, fix-declares
[def-form?] PREDICATE tests if zloc is a def | INTERNAL
[extract-name] EXTRACTS defn/def name | INTERNAL
[extract-arglist] EXTRACTS fn arglists | INTERNAL

## FUNCTIONS — clj-surgeon.fix-declares (Compound Op)

[plan] RETURNS [{:form :action :reason}] safe moves | USED-BY run-declares, execute!
[execute!] APPLIES plan to file in-place | USED-BY run-declares
[first-usage-line] FINDS first line where symbol is referenced | INTERNAL
[form-at-or-before] FINDS form that should precede another | INTERNAL

## FUNCTIONS — clj-surgeon.extract

[plan] RETURNS {:forms-to-move :new-ns :require-changes} | DRY-RUN
[execute!] MOVES forms to new file + updates requires | SIDE-EFFECT file-write

## FUNCTIONS — clj-surgeon.rename

[analyze-file] RETURNS all ns-refs in a file | USED-BY plan
[plan] RETURNS {:files-to-move :ns-changes :require-changes} | DRY-RUN
[execute!] RENAMES ns + moves file + updates all :require entries | SIDE-EFFECT file-write + file-move

## FUNCTIONS — clj-surgeon.move

[move-form] MOVES single form to position before target | SIDE-EFFECT file-rewrite
[find-form] LOCATES form by name in zloc | INTERNAL
[preceding-comment-nodes] COLLECTS comments attached to form | INTERNAL

## FUNCTIONS — clj-surgeon.forward-refs

[detect-forward-refs] RUNS clj-kondo + returns forward-ref violations | CALLS kondo CLI | USED-BY fix-declares

## CLJC MODULE (Platform-Split .cljc Support)

[cljc.walk/top-level-forms] WALKS cljc reader-conditionals | USED-BY cljc.analyze, cljc.split
[cljc.merge/merge-files] MERGES .clj + .cljs → .cljc | PLATFORM-AWARE
[cljc.split/split-file] SPLITS .cljc → {clj: .clj, cljs: .cljs} | INVERSE of merge
[cljc.require-ops/add-require] ADDS :require entry to ns form | PLATFORM-AWARE
[cljc.analyze/analyze-cljc] ANALYZES platform-conditional forms | USED-BY cljc ops

## DEPENDENCY TOPOLOGY (leaf→root)

LEAF LAYER (no deps): analyze, move, rename, forward-refs, cljc.merge, cljc.split, cljc.walk
MID LAYER: outline→cljc.walk | cljc.analyze→(merge,split,walk) | cljc.require-ops→(merge,split)
COMPOUND LAYER: fix-declares→(analyze,outline,forward-refs) | extract→(outline,analyze)
ROOT: core→ALL

## KEY INVARIANTS (STATED)

[INVARIANT] plan/execute! pattern: all ops with side effects expose dry-run plan first
[INVARIANT] rewrite-clj zipper: all AST manipulation preserves whitespace/comments
[INVARIANT] topological-sort in fix-declares: moves leaves first, never creates new forward refs
[INVARIANT] rename: updates ALL :require entries across all .clj/.cljs files in src paths
[INVARIANT] cljc ops: platform-aware — :clj and :cljs reader conditionals treated distinctly

## TOKEN BENCHMARK

| Approach | Tokens | Time | Method |
|---|---|---|---|
| Full source read (13 files) | 7,308 | seconds | cat all .clj files |
| Gene Kim AST outline (5 files) | ~1,000 | ms | clj-surgeon :outline |
| CKG full graph (this file) | 847 | one-time | structured extraction |
| CKG single 2-hop query | ~52 | sub-ms | graph traversal |
| CKG 5-question session | ~260 | sub-ms | 5 × 52 avg |

REDUCTION vs full read: 8.6x (full CKG) | 28x (5-question session)
REDUCTION vs Gene Kim outline: 1.18x (full CKG) | 3.8x (5-question session)
REDUCTION vs RAG baseline (~150K): 177x (full CKG) | 577x (5-question session)
