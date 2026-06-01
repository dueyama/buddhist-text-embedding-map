# Local Project Memory

This file records local project changes for the Okyou experiments. Times are JST.

## 2026-06-01 17:33 JST

- Summary: Initialized local project governance files for git-managed research work.
- Files:
  - `AGENTS.md`
  - `.gitignore`
  - `memory.md`
- Verification:
  - Confirmed this directory was not previously a git repository.
  - Confirmed `.env` exists and must remain untracked.
  - Confirmed legacy notebooks/scripts contain hardcoded API keys and must not be staged.
- Commit: `183a5f88e30101fc28a63aee37895715876eb02d`

## 2026-06-01 17:35 JST

- Summary: Added planning documents for the Japanese Kanbun style map and sect-based sutra map.
- Files:
  - `docs/kanbun-style-map-plan.md`
  - `docs/sect-sutra-map-plan.md`
- Verification:
  - Checked planned commit files for hardcoded API key patterns.
  - Confirmed staged files before committing.
- Commit: `f37b02dda979138c8ba821916543de4b8f03a914`

## 2026-06-01 17:35 JST

- Summary: Added the initial results note for the Amitabha Sutra two-translation comparison.
- Files:
  - `docs/results.md`
- Verification:
  - Read `experiments/amida_compare/outputs/summary.json` and copied the key metrics into the results note.
  - Checked planned commit files for hardcoded API key patterns.
  - Confirmed staged files before committing.
- Commit: `6c0a0439df63b8753bc5d2c45ed56ff64fd43fec`

## 2026-06-01 17:36 JST

- Summary: Recorded the actual commit hash for the initial results-note commit.
- Files:
  - `memory.md`
- Verification:
  - Read `git rev-parse HEAD` after the results-note commit.
- Commit: this entry is committed by the next memory-only commit; its hash is reported in the assistant summary to avoid an infinite self-reference.
