# Reconstructed tool use and verification scope

Observed November 2, 2026. This reconstruction uses public study sources, exact Git history and the current preparation workflow; it does not copy private correspondence or raw review reports into Git. Machine-readable evidence is in `tool-provenance.json`.

## Original study: coding, experiments, analysis and writing

The public manuscript at [07e3cbd3c4855e5e19344885fbf672c3d7a0f039](https://github.com/yoheinakajima/soft-to-rigid/blob/07e3cbd3c4855e5e19344885fbf672c3d7a0f039/paper/main.tex) acknowledges that code, experiments and verification were developed with Claude (Anthropic) under the author's direction. All 24 inspected original study commits are labelled `Claude Opus 5.5` in AI coauthor trailers. These trailers document a tool label, not a second human author and not authenticated provider model telemetry. Most also contain a Claude Code session trailer; session links are not copied here.

Representative exact evidence:

- [d9b2f535741c529149bedf391542899875bac75d](https://github.com/yoheinakajima/soft-to-rigid/commit/d9b2f535741c529149bedf391542899875bac75d): engine, catalogue, ledger, verifiers and first campaign plans; Claude Opus 5.5 trailer.
- [b1bc4aa3a71a309936be90f3f3a506b7d2bb53ec](https://github.com/yoheinakajima/soft-to-rigid/commit/b1bc4aa3a71a309936be90f3f3a506b7d2bb53ec): C00–C10 evidence pipeline, manuscript draft and site; the same tool label.
- [398766a985f71fc1f2b3e7012719041793eb481a](https://github.com/yoheinakajima/soft-to-rigid/commit/398766a985f71fc1f2b3e7012719041793eb481a): revisions explicitly attributed to Explore Science review, covering method details, budget counts, tuning limits, C14 scope and the post-hoc pilot check.
- [992db4b66e72282e469e1a57157ab59b396e98f1](https://github.com/yoheinakajima/soft-to-rigid/commit/992db4b66e72282e469e1a57157ab59b396e98f1) and other revision subjects describe review rounds and checks; those subjects alone do not establish who reviewed the work, exact review models or independent human validation.

The known role is substantive research/implementation/manuscript assistance, not merely spelling or formatting. [51ea7553af66f3f2472583e0beaf284a6d99fb45](https://github.com/yoheinakajima/soft-to-rigid/commit/51ea7553af66f3f2472583e0beaf284a6d99fb45) and the final PDF commit also document Claude-assisted arXiv source-bundle/metadata/PDF preparation; retained preparation evidence supports PDF checking without an exact model receipt. No private transcript or unrelated history is reproduced. Exact provider/API model identifiers, Claude Code runtime versions, complete prompts and per-operation model use were not preserved in the inspected source tree. The commit label is retained with that limit rather than invented as a verified runtime version. The numerical packing engines and saved-output scripts produce the experimental outcomes; language models are not experimental participants or packing-scoring subjects.

## Current preparation: Codex and software checks

The November journal preparation uses Codex (OpenAI), including a paper-specific worker configured as `gpt-6.1-sol` with high reasoning effort and manager AI review. The exact manager model/runtime is not established by this source record. Codex assisted manuscript drafting/revision, claim/citation/compatibility critique, verification-program development, metadata/declaration preparation, build and rendered-PDF QA.

The actual computational check route is `scripts/verify_joh_packet.py`: Python standard-library analysis of fixed saved evidence plus the separate native `verify.py` floating-point and `packing.certify` exact checkers on four explicitly enlarged witnesses. It reconstructs C10/C14/C15/C16 summaries and C06 boundaries, records the 639 fixed input hashes, and fails on a missing cache. Existing Tectonic compiles the editable sources; Poppler renders/checks the PDFs. No optimizer, new campaign, provider inference or ledger runtime is invoked by this route.

The verification program and its review were AI-assisted too. Distinct software checks and deterministic cross-checks must not be described as independent human verification. Preparation critique is not independent journal peer review. No claim is made that the author personally independently verified every derivation, reference or experimental record. Yohei Nakajima remains the sole human author responsible for approval and accountability for the submitted work.

## Disclosed relationships

The author-approved public affiliation and supporter are Untapped Capital. The author is its founder and general partner and directed the research/AI-assisted workflow; this is not an independent sponsor with no role. The [official Untapped site](https://untapped.vc/) lists Explore Science as a portfolio company, while the pinned revision history records feedback from that service. The [official ActiveGraph site](https://activegraph.ai/) identifies ActiveGraph as created by Yohei Nakajima; the study uses it to organize portions of its evidence. These roles are disclosed without inventing personal advisory positions, provider-specific credits, outside grants, private ownership details or independent endorsement.
