# MANIFEST - file -> RLS form field

The platform ingests these files FROM THE PUSHED BRANCH (`publish.py`, SKILL.md step 8.5), not from the form: open https://studio.mercor.com/ and create a task in your domain to read off its 8-character id, publish under that id, then click magic-star -> STEM Software Runner for the Taiga eval. The table below is the field map - what ships, and where each artifact lands - so you can CHECK the ingested task; it is not an upload checklist, and nothing here travels one-file-per-field.

> **After Taiga runs the task, run `submission-check` on the runs before trusting the result** - don't skip it.

## Grading

> **MISSING FILES - this task is NOT submittable:** `solution.md`

(string answer - no numeric [grader:] directive; grade by exact, case-insensitive match per grading_guide.md)

_Direction: **inverse**._

| File | RLS field | Type |
|---|---|---|
| `problem.md` | **User Prompt** | text - paste contents |
| `oracle/oracle.py` | **Oracle File** | ships under `oracle/` (inverse only) - the file the harness invokes. For a native oracle this is the fixed wrapper; its authored sibling ships beside it and needs no row. |
| `solution/main.py` | **Verification Code / Solution Files** | file upload |
| `golden/expected.json -> answer` | **Golden Response** | text (bare value the model submits) |
| `golden/expected.json -> [grader:] directive` | **Grading Guidance** | text - paste the [grader: tolerance=[...], type=[...]] line (below) together with the golden answer and grading_guide.md into the ONE Grading Guidance field |
| `grader/grading_guide.md` | **Grading Guidance** | text - near-miss table + acceptance prose (same field as above) |
| `(legacy numeric Tolerance field)` | **Tolerance** | numeric - LEAVE BLANK when using the [grader:] directive; single-value tasks only |
| `reasoning_trap.md` | **Reasoning Trap** | text |
| `requirements.txt` | **Required Packages** | text |
| `config.yaml -> domain` | **Domain** | dropdown |
| `config.yaml -> sub_domain` | **Subdomain** | text |
| `config.yaml -> direction` | **Directionality** | Forward / Inverse |
| `config.yaml -> simulator` | **Required Tool** | text |
| `solution.md` | **Explanation/Context** | text - paste contents: the writer's own step-by-step solution |

**Never shipped (stays on your machine):** `solution/shortcut.*`, `BRIEF.md`, `STATE.md`, `MANIFEST.md`, `runs/*`, `raw_solution_content.md`, `oracle/*.bin`, `oracle/*.o`, `oracle/*.mod`, `oracle/*.so`, `oracle/.build/*`
