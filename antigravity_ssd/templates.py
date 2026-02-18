"""
Templates - Nội dung template cho tất cả Skills, Workflows, Scripts, và Documents.
Mỗi function trả về string content cho file tương ứng.
"""

from datetime import datetime


def _today():
    return datetime.now().strftime("%Y-%m-%d")


# ============================================================================
# SKILL TEMPLATES - SKILL.md files
# ============================================================================

def skill_constitution():
    return '''---
name: speckit.constitution
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs: 
  - label: Build Specification
    agent: speckit.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Governance Architect**. Your role is to establish and maintain the project's "Source of Law"—the constitution. You ensure that all project principles, standards, and non-negotiables are clearly documented and kept in sync across all templates and workflows.

## Task

### Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy.
   - Ensure each Principle section: succinct name line, paragraph capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist:
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types.
   - Read any runtime guidance docs.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles
   - Added/Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending)
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language.

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message.
'''


def skill_specify():
    return '''---
name: speckit.specify
description: Create or update the feature specification from a natural language feature description.
handoffs: 
  - label: Build Technical Plan
    agent: speckit.plan
    prompt: Create a plan for the spec. I am building with...
  - label: Clarify Spec Requirements
    agent: speckit.clarify
    prompt: Clarify specification requirements
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Domain Scribe**. Your role is to translate natural language feature descriptions into highly structured, high-quality feature specifications (`spec.md`). You ensure clarity, testability, and alignment with the project's success criteria.

## Task

### Outline

Given a feature description, do this:

1. **Generate a concise short name** (2-4 words) for the branch:
   - action-noun format (e.g., "add-user-auth", "fix-payment-bug")
   - Preserve technical terms and acronyms

2. **Check for existing branches before creating new one**:
   a. Fetch remote branches: `git fetch --all --prune`
   b. Find the highest feature number across remote/local branches and specs directories
   c. Use N+1 for the new branch number
   d. Run `../scripts/bash/create-new-feature.sh --json "{{args}}"` with calculated number

3. Load `templates/spec-template.md` to understand required sections.

4. Follow this execution flow:
    1. Parse user description from Input
       If empty: ERROR "No feature description provided"
    2. Extract key concepts: actors, actions, data, constraints
    3. For unclear aspects:
       - Make informed guesses based on context and industry standards
       - Only mark with [NEEDS CLARIFICATION: specific question] if critical
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
    4. Fill User Scenarios & Testing section
    5. Generate Functional Requirements (each must be testable)
    6. Define Success Criteria (measurable, technology-agnostic)
    7. Identify Key Entities (if data involved)
    8. Return: SUCCESS (spec ready for planning)

5. Write the specification to SPEC_FILE using the template structure.

6. **Specification Quality Validation**: Validate against quality criteria
   - Create checklist at `FEATURE_DIR/checklists/requirements.md`
   - Run validation, iterate up to 3 times
   - Handle [NEEDS CLARIFICATION] markers with interactive Q&A

7. Report completion with branch name, spec file path, and readiness for next phase.

## Quick Guidelines

- Focus on **WHAT** users need and **WHY**.
- Avoid HOW to implement (no tech stack, APIs, code structure).
- Written for business stakeholders, not developers.

### Section Requirements
- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
1. **Make informed guesses**: Use context, industry standards, and common patterns to fill gaps
2. **Document assumptions**: Record reasonable defaults in the Assumptions section
3. **Limit clarifications**: Maximum 3 [NEEDS CLARIFICATION] markers
4. **Prioritize clarifications**: scope > security/privacy > user experience > technical details
5. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item

### Success Criteria Guidelines
Success criteria must be:
1. **Measurable**: Include specific metrics (time, percentage, count, rate)
2. **Technology-agnostic**: No mention of frameworks, languages, databases, or tools
3. **User-focused**: Describe outcomes from user/business perspective
4. **Verifiable**: Can be tested without knowing implementation details
'''


def skill_clarify():
    return '''---
name: speckit.clarify
description: Identify and resolve ambiguities in an existing feature specification through systematic analysis.
version: 1.0.0
depends-on:
  - speckit.specify
handoffs: 
  - label: Rebuild Plan
    agent: speckit.plan
    prompt: Rebuild the plan from the updated spec
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Clarity Engineer**. Your role is to systematically identify and resolve all ambiguities, gaps, and inconsistencies in feature specifications before they reach the planning or implementation phases.

## Task

### Outline

1. **Setup**: Load the feature spec from the active feature directory.

2. **Ambiguity Detection Pass**: Scan the spec for:
   - Vague language ("should", "might", "could", "etc.")
   - Missing boundary conditions
   - Undefined error handling
   - Implicit assumptions not documented
   - Missing edge cases
   - Conflicting requirements

3. **Categorize Issues** by severity:
   - 🔴 CRITICAL: Blocks implementation (scope ambiguity, conflicting requirements)
   - 🟡 IMPORTANT: May cause rework (missing edge cases, unclear validation)
   - 🟢 MINOR: Polish items (wording improvements, better examples)

4. **Interactive Resolution**:
   - For each CRITICAL issue: Present options to user, wait for decision
   - For each IMPORTANT issue: Suggest a default, ask for confirmation
   - For MINOR issues: Auto-fix with notification

5. **Update spec.md** with all resolutions.

6. **Report** changes made and remaining open items.
'''


def skill_plan():
    return '''---
name: speckit.plan
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
version: 1.0.0
depends-on:
  - speckit.specify
handoffs: 
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: speckit.checklist
    prompt: Create a checklist for the following domain...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity System Architect**. Your role is to bridge the gap between functional specifications and technical implementation. You design data models, define API contracts, and perform technical research to ensure a robust and scalable architecture.

## Task

### Outline

1. **Setup**: Run `../scripts/bash/setup-plan.sh --json` and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH.

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template from `templates/plan-template.md`.

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section
   - Evaluate gates (ERROR if violations unjustified)

### Phase 0: Outline & Research

1. Extract unknowns from Technical Context → research tasks
2. Generate and dispatch research agents
3. Consolidate findings in `research.md`

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. Extract entities from feature spec → `data-model.md`
2. Generate API contracts from functional requirements → `/contracts/`
3. Agent context update

**Output**: data-model.md, /contracts/*, quickstart.md

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
'''


def skill_tasks():
    return '''---
name: speckit.tasks
description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
version: 1.0.0
depends-on:
  - speckit.plan
handoffs: 
  - label: Analyze For Consistency
    agent: speckit.analyze
    prompt: Run a project analysis for consistency
    send: true
  - label: Implement Project
    agent: speckit.implement
    prompt: Start the implementation in phases
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Execution Strategist**. Your role is to deconstruct complex technical plans into atomic, dependency-ordered tasks. You organize work into user-story-driven phases to ensure incremental delivery and high observability.

## Task

### Outline

1. **Setup**: Run `../scripts/bash/check-prerequisites.sh --json` and parse FEATURE_DIR and AVAILABLE_DOCS.

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md, spec.md
   - **Optional**: data-model.md, contracts/, research.md, quickstart.md

3. **Execute task generation workflow**:
   - Extract tech stack and libraries from plan.md
   - Extract user stories with priorities from spec.md
   - Map entities, endpoints, decisions to user stories
   - Generate tasks organized by user story
   - Generate dependency graph
   - Validate task completeness

4. **Generate tasks.md** with:
   - Phase 1: Setup tasks
   - Phase 2: Foundational tasks
   - Phase 3+: One phase per user story (priority order)
   - Final Phase: Polish & cross-cutting concerns

5. **Report**: Output path and summary.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story for independent implementation.

### Checklist Format (REQUIRED)

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components**:
1. **Checkbox**: ALWAYS start with `- [ ]`
2. **Task ID**: Sequential (T001, T002...)
3. **[P] marker**: Only if parallelizable
4. **[Story] label**: REQUIRED for user story phases only ([US1], [US2]...)
5. **Description**: Clear action with exact file path

### Phase Structure
- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites)
- **Phase 3+**: User Stories in priority order
- **Final Phase**: Polish & Cross-Cutting Concerns
'''


def skill_analyze():
    return '''---
name: speckit.analyze
description: Perform a multi-pass consistency analysis across all specification artifacts to detect drift, gaps, and contradictions.
version: 1.0.0
depends-on:
  - speckit.tasks
handoffs: 
  - label: Fix Issues
    agent: speckit.implement
    prompt: Fix the consistency issues found
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Consistency Analyst**. Your role is to detect specification drift, gaps, and contradictions across all project artifacts (spec.md, plan.md, tasks.md, data-model.md, contracts/).

## Task

### Goal
Perform a comprehensive consistency analysis across all design artifacts and produce a compact analysis report.

### Operating Constraints
- Token-efficient analysis (minimize redundant reads)
- Progressive artifact disclosure (load only what's needed)
- Severity-based prioritization

### Steps

1. **Initialize Analysis Context**: Load feature directory and available docs.

2. **Load Artifacts** (Progressive Disclosure):
   - Always: spec.md, plan.md, tasks.md
   - If exists: data-model.md, contracts/, research.md

3. **Build Semantic Models**: Extract entities, requirements, tasks into comparable structures.

4. **Detection Passes** (Token-Efficient Analysis):
   - **Pass 1 - Requirement Coverage**: Every spec requirement → at least one task
   - **Pass 2 - Entity Consistency**: Data model entities match spec and plan references
   - **Pass 3 - Contract Alignment**: API contracts match spec user scenarios
   - **Pass 4 - Task Completeness**: Every plan section → at least one task
   - **Pass 5 - Dependency Validation**: Task dependencies are logically ordered

5. **Severity Assignment**:
   - 🔴 CRITICAL: Missing requirement coverage, conflicting definitions
   - 🟡 WARNING: Incomplete coverage, ambiguous references
   - 🟢 INFO: Style inconsistencies, naming suggestions

6. **Produce Compact Analysis Report**

7. **Provide Next Actions**: Specific remediation steps per issue.
'''


def skill_implement():
    return '''---
name: speckit.implement
description: Execute the implementation plan with precision, processing tasks from tasks.md with IRONCLAD anti-regression protocols.
version: 1.0.0
depends-on:
  - speckit.tasks
handoffs: 
  - label: Run Tests
    agent: speckit.tester
    prompt: Run tests for implemented code
    send: true
  - label: Review Code
    agent: speckit.reviewer
    prompt: Review the implementation
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Master Builder**. Your role is to execute the implementation plan with precision, processing tasks from `tasks.md` and ensuring that the final codebase aligns perfectly with the specification, plan, and quality standards.

**CORE OBJECTIVE:** Fix bugs and implement features with **ZERO REGRESSION**.
**YOUR MOTTO:** "Measure twice, cut once. If you can't prove it's broken, don't fix it."

---

## 🛡️ IRONCLAD PROTOCOLS (Non-Negotiable)

### Protocol 1: Blast Radius Analysis
**BEFORE** writing any production code modification, you MUST:
1. **Read**: Read target file(s) to understand current implementation
2. **Trace**: Find ALL other files importing/using the function/class you intend to modify
3. **Report**: Output blast radius with risk level (LOW/MEDIUM/HIGH)
4. **Decide**: If >2 files affected, trigger Protocol 2 (Strangler Pattern)

### Protocol 2: Strangler Pattern (Immutable Core)
If file is critical or has high dependencies (>2 affected files):
1. DO NOT EDIT the existing function
2. CREATE a new file/module (e.g., `feature_v2.ts`)
3. IMPLEMENT improved logic there
4. SWITCH imports one by one

### Protocol 3: Reproduction Script First (TDD)
**FORBIDDEN** to fix/implement without evidence:
1. Create `repro_task_[id]` script
2. Run it to confirm current state (should FAIL)
3. ONLY THEN implement the fix/feature
4. Run script again to prove it passes

### Protocol 4: Context Anchoring
At start and after every 3 modifications:
1. Run `tree -L 2` to visualize file structure
2. Update ARCHITECTURE.md

---

## Task Execution

### Outline

1. Run prerequisites check and parse FEATURE_DIR.
2. Check checklists status (if exists).
3. Load implementation context (tasks.md, plan.md, data-model.md, contracts/).
4. Context Anchoring (Protocol 4).
5. Project Setup Verification (ignore files).
6. Parse tasks.md and extract phases, dependencies, execution flow.
7. Execute implementation with Ironclad Protocols for EACH task.
8. Progress tracking and error handling.
9. Context Re-anchoring (every 3 tasks).
10. Completion validation.

## 🚫 Anti-Hallucination Rules

1. **No Magic Imports:** Never import a library without checking first.
2. **Strict Diff-Only:** Minimal edits when modifying existing files.
3. **Stop & Ask:** If editing >3 files for a "simple fix", STOP. You are likely cascading a regression.
'''


def skill_checker():
    return '''---
name: speckit.checker
description: Run comprehensive static analysis across the codebase and aggregate results into actionable findings.
version: 1.0.0
depends-on:
  - speckit.implement
handoffs: 
  - label: Fix Issues
    agent: speckit.implement
    prompt: Fix the static analysis issues found
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Static Analyst**. Your role is to run all available static analysis tools and aggregate their findings into a unified, actionable report.

## Task

### Outline

1. **Detect project stack**: Identify languages and tools from package.json, requirements.txt, go.mod, etc.

2. **Run analysis tools** based on detected stack:
   - **TypeScript/JavaScript**: `tsc --noEmit`, `eslint`, `prettier --check`
   - **Python**: `mypy`, `ruff`, `black --check`
   - **Go**: `go vet`, `golangci-lint`
   - **Rust**: `cargo clippy`, `cargo check`
   - General: dependency audit, security scan

3. **Aggregate results** into unified report:
   - Group by severity (ERROR, WARNING, INFO)
   - Group by file/module
   - Identify patterns (repeated issue types)

4. **Produce actionable summary**:
   - Critical blockers (must fix before merge)
   - Warnings (should fix)
   - Suggestions (nice to have)
   - Auto-fix commands where available
'''


def skill_tester():
    return '''---
name: speckit.tester
description: Execute test suites, analyze results, and report coverage metrics with actionable insights.
version: 1.0.0
depends-on:
  - speckit.implement
handoffs: 
  - label: Fix Failures
    agent: speckit.implement
    prompt: Fix the test failures found
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Test Engineer**. Your role is to execute test suites, analyze results, measure coverage, and provide actionable insights for improving test quality.

## Task

### Outline

1. **Detect test framework**: Identify from project config (jest, pytest, go test, cargo test, etc.)

2. **Run test suites**:
   - Unit tests
   - Integration tests (if available)
   - E2E tests (if available)

3. **Collect metrics**:
   - Pass/Fail counts
   - Coverage percentage
   - Execution time
   - Flaky test detection

4. **Analyze failures**:
   - Categorize: Logic error, Setup issue, External dependency, Flaky
   - Provide root cause analysis for each failure
   - Suggest fixes

5. **Report**:
   - Summary table
   - Coverage heatmap (which modules are under-tested)
   - Recommendations for new tests
'''


def skill_reviewer():
    return '''---
name: speckit.reviewer
description: Perform comprehensive code review against specification, plan, and best practices.
version: 1.0.0
depends-on:
  - speckit.implement
handoffs: 
  - label: Fix Issues
    agent: speckit.implement
    prompt: Fix the review issues found
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Code Reviewer**. Your role is to perform thorough code review ensuring alignment with the specification, plan, and coding best practices.

## Task

### Outline

1. **Load context**: Read spec.md, plan.md, and constitution.md for review criteria.

2. **Review dimensions**:
   - **Spec Compliance**: Does each requirement have corresponding implementation?
   - **Architecture**: Does code follow the planned structure?
   - **Security**: Input validation, auth checks, data sanitization
   - **Performance**: N+1 queries, unnecessary re-renders, memory leaks
   - **Code Quality**: DRY, SOLID, naming conventions, error handling
   - **Testing**: Are critical paths tested?

3. **Issue categorization**:
   - 🔴 BLOCKER: Security vulnerability, data loss risk, spec violation
   - 🟡 SUGGESTION: Improvement, refactoring opportunity
   - 🟢 NIT: Style, naming, minor cleanup

4. **Report** with specific file:line references and suggested fixes.
'''


def skill_validate():
    return '''---
name: speckit.validate
description: Perform end-to-end validation of the implementation against the original specification.
version: 1.0.0
depends-on:
  - speckit.implement
handoffs: []
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Validation Oracle**. Your role is to perform the final validation pass, ensuring the implementation faithfully realizes the specification.

## Task

### Outline

1. **Load all artifacts**: spec.md, plan.md, tasks.md, and the actual codebase.

2. **Requirement-by-requirement validation**:
   - For each functional requirement in spec.md:
     - Locate the implementing code
     - Verify behavior matches specification
     - Check edge cases are handled
     - Verify success criteria are met

3. **Gap analysis**:
   - Requirements without implementation
   - Implementation without requirements (scope creep)
   - Partial implementations

4. **Final verdict**:
   - ✅ PASS: All requirements met, no gaps
   - ⚠️ CONDITIONAL PASS: Minor gaps, documented deviations
   - ❌ FAIL: Critical requirements missing or broken

5. **Report** with specific requirement-to-code mapping.
'''


def skill_checklist():
    return '''---
name: speckit.checklist
description: Generate and validate requirement checklists from specification artifacts.
version: 1.0.0
depends-on:
  - speckit.specify
handoffs: []
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Requirements Auditor**. Your role is to create comprehensive, traceable checklists from specifications that can be used to verify implementation completeness.

## Task

### Outline

1. **Load spec.md** from the active feature directory.

2. **Extract checkable items** from:
   - Functional requirements → verification checklist
   - Success criteria → acceptance checklist
   - User scenarios → test scenario checklist
   - Constraints → constraint compliance checklist

3. **Generate checklist file** at `FEATURE_DIR/checklists/`:
   - Each item must be a `- [ ]` checkbox
   - Include reference to source section
   - Group by category

4. **Cross-reference** with existing checklists to avoid duplication.
'''


def skill_diff():
    return '''---
name: speckit.diff
description: Compare specification artifacts to detect drift between design and implementation.
version: 1.0.0
depends-on: []
handoffs: []
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Diff Analyst**. Your role is to compare different versions of specification artifacts or compare specs against implementation to detect semantic drift.

## Task

### Outline

1. **Determine comparison mode**:
   - Spec vs Spec (version comparison)
   - Spec vs Implementation (drift detection)
   - Plan vs Tasks (completeness check)

2. **Load artifacts** for comparison.

3. **Perform semantic diff**:
   - Added items (new requirements, features)
   - Removed items (dropped requirements)
   - Modified items (changed behavior)
   - Moved items (reorganized structure)

4. **Impact analysis**: For each change, assess impact on downstream artifacts.

5. **Report** with clear before/after comparisons and recommended actions.
'''


def skill_migrate():
    return '''---
name: speckit.migrate
description: Analyze and migrate legacy codebases into the Spec-Kit specification format.
version: 1.0.0
depends-on: []
handoffs: 
  - label: Create Spec
    agent: speckit.specify
    prompt: Create spec from the migrated analysis
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Migration Specialist**. Your role is to reverse-engineer existing codebases into structured specifications, enabling them to benefit from the Spec-Kit workflow.

## Task

### Outline

1. **Analyze existing codebase**:
   - Detect languages, frameworks, project structure
   - Identify core entities and data models
   - Map routes/endpoints to features
   - Document existing tests and coverage

2. **Generate spec artifacts**:
   - Create initial spec.md from discovered features
   - Create initial plan.md from architecture analysis
   - Create initial tasks.md with migration tasks

3. **Assessment report**:
   - Technical debt inventory
   - Migration risk assessment
   - Recommended migration sequence
   - Estimated effort per feature
'''


def skill_quizme():
    return '''---
name: speckit.quizme
description: Challenge the specification with adversarial "what-if" scenarios to uncover edge cases and gaps.
version: 1.0.0
depends-on:
  - speckit.specify
handoffs: []
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Red Team Analyst**. Your role is to adversarially challenge specifications by asking penetrating "what-if" questions that expose edge cases, security gaps, and logical inconsistencies.

## Task

### Outline

1. **Load spec.md** from active feature.

2. **Generate adversarial scenarios** across categories:
   - **Edge Cases**: Boundary values, empty states, maximum limits
   - **Failure Modes**: Network failures, timeout, concurrent access
   - **Security**: Injection, privilege escalation, data leakage
   - **Scale**: High volume, rapid succession, resource exhaustion
   - **User Behavior**: Unexpected input, rapid clicking, browser back button

3. **Present as quiz** format:
   - Q1: "What happens when [scenario]?"
   - Expected: [what spec says should happen]
   - Gap: [what's actually unspecified]

4. **Scoring**: Rate spec robustness (0-100%).

5. **Recommendations**: Specific spec updates to address each gap.
'''


def skill_status():
    return '''---
name: speckit.status
description: Display a comprehensive progress dashboard for the current feature implementation.
version: 1.0.0
depends-on:
  - speckit.tasks
handoffs: []
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Progress Tracker**. Your role is to provide a clear, at-a-glance view of the current feature's progress across all specification artifacts.

## Task

### Outline

1. **Load all artifacts** from active feature directory.

2. **Compute metrics**:
   - Tasks: Total / Done / In Progress / Blocked
   - Checklists: Pass rate per checklist
   - Coverage: Spec requirements with implementation
   - Quality: Analysis issues open/closed

3. **Display dashboard**:
   ```
   ┌─────────────────────────────────────────┐
   │  📊 Feature: [NAME] - Progress Report   │
   ├─────────────────────────────────────────┤
   │  Tasks:     ████████░░ 80% (16/20)      │
   │  Checklists: ██████████ 100% (3/3 pass) │
   │  Coverage:  ███████░░░ 70% (7/10 reqs)  │
   │  Issues:    ██████████ 0 open            │
   ├─────────────────────────────────────────┤
   │  Phase: Implementation (Phase 3/5)       │
   │  Next: T017 - Create UserService         │
   └─────────────────────────────────────────┘
   ```

4. **Blockers & risks**: Highlight any blocked tasks or critical issues.
'''


def skill_taskstoissues():
    return '''---
name: speckit.taskstoissues
description: Synchronize tasks.md entries to GitHub Issues or other issue trackers.
version: 1.0.0
depends-on:
  - speckit.tasks
handoffs: []
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **Antigravity Issue Syncer**. Your role is to bridge the gap between the spec-kit task system and external issue trackers (GitHub Issues, Jira, Linear, etc.).

## Task

### Outline

1. **Load tasks.md** from active feature.

2. **Parse tasks** into structured format:
   - Task ID, Description, Phase, Dependencies
   - Story mapping ([US1], [US2]...)
   - Parallel markers [P]

3. **Detect issue tracker**:
   - GitHub: Check for `.github/` directory or `git remote`
   - Jira: Check for `.jira/` config
   - Linear: Check for `.linear/` config
   - If none detected, generate GitHub-compatible markdown

4. **Generate issues**:
   - One issue per task
   - Labels: phase, priority, story
   - Dependencies as "blocked by #XX" references
   - Milestone: Feature name

5. **Report**: Summary of created/updated issues with links.
'''


# ============================================================================
# Mapping: skill name → template function
# ============================================================================
SKILL_TEMPLATE_MAP = {
    "speckit.constitution": skill_constitution,
    "speckit.specify": skill_specify,
    "speckit.clarify": skill_clarify,
    "speckit.plan": skill_plan,
    "speckit.tasks": skill_tasks,
    "speckit.analyze": skill_analyze,
    "speckit.implement": skill_implement,
    "speckit.checker": skill_checker,
    "speckit.tester": skill_tester,
    "speckit.reviewer": skill_reviewer,
    "speckit.validate": skill_validate,
    "speckit.checklist": skill_checklist,
    "speckit.diff": skill_diff,
    "speckit.migrate": skill_migrate,
    "speckit.quizme": skill_quizme,
    "speckit.status": skill_status,
    "speckit.taskstoissues": skill_taskstoissues,
}


# ============================================================================
# WORKFLOW TEMPLATES
# ============================================================================

def workflow_all():
    return '''---
description: Run the full speckit pipeline from specification to analysis in one command.
---

# Workflow: speckit.all

This meta-workflow orchestrates the complete specification pipeline.

## Pipeline Steps

1. **Specify** (`/speckit.specify`):
   - Use the `view_file` tool to read: `.agent/skills/speckit.specify/SKILL.md`
   - Execute with user's feature description
   - Creates: `spec.md`

2. **Clarify** (`/speckit.clarify`):
   - Use the `view_file` tool to read: `.agent/skills/speckit.clarify/SKILL.md`
   - Execute to resolve ambiguities
   - Updates: `spec.md`

3. **Plan** (`/speckit.plan`):
   - Use the `view_file` tool to read: `.agent/skills/speckit.plan/SKILL.md`
   - Execute to create technical design
   - Creates: `plan.md`

4. **Tasks** (`/speckit.tasks`):
   - Use the `view_file` tool to read: `.agent/skills/speckit.tasks/SKILL.md`
   - Execute to generate task breakdown
   - Creates: `tasks.md`

5. **Analyze** (`/speckit.analyze`):
   - Use the `view_file` tool to read: `.agent/skills/speckit.analyze/SKILL.md`
   - Execute to validate consistency
   - Output: Analysis report

## Usage

```
/speckit.all "Build a user authentication system with OAuth2 support"
```

## On Error

If any step fails, stop the pipeline and report:
- Which step failed
- The error message
- Suggested remediation
'''


def workflow_numbered(number, skill_name, description, skill_file):
    """Generate a numbered workflow that delegates to a skill."""
    return f'''---
description: {description}
---

# Workflow: {number}-speckit.{skill_name.replace("speckit.", "")}

## Execution

1. **Load Skill**: Use the `view_file` tool to read: `.agent/skills/{skill_name}/SKILL.md`
2. **Execute**: Follow the skill instructions with the user's input.

## Usage

```
/{number}-speckit.{skill_name.replace("speckit.", "")} "your input here"
```
'''


def workflow_prepare():
    return '''---
description: Execute the full preparation pipeline (Specify -> Clarify -> Plan -> Tasks -> Analyze) in sequence.
---

# Workflow: speckit.prepare

This workflow orchestrates the sequential execution of the Speckit preparation phase skills (02-06).

1. **Step 1: Specify (Skill 02)**
   - Goal: Create or update the `spec.md` based on user input.
   - Action: Read and execute `.agent/skills/speckit.specify/SKILL.md`.

2. **Step 2: Clarify (Skill 03)**
   - Goal: Refine the `spec.md` by identifying and resolving ambiguities.
   - Action: Read and execute `.agent/skills/speckit.clarify/SKILL.md`.

3. **Step 3: Plan (Skill 04)**
   - Goal: Generate `plan.md` from the finalized spec.
   - Action: Read and execute `.agent/skills/speckit.plan/SKILL.md`.

4. **Step 4: Tasks (Skill 05)**
   - Goal: Generate actionable `tasks.md` from the plan.
   - Action: Read and execute `.agent/skills/speckit.tasks/SKILL.md`.

5. **Step 5: Analyze (Skill 06)**
   - Goal: Validate consistency across all design artifacts (spec, plan, tasks).
   - Action: Read and execute `.agent/skills/speckit.analyze/SKILL.md`.
'''


def workflow_util(util_name, skill_name, description):
    """Generate a utility workflow."""
    return f'''---
description: {description}
---

# Workflow: util-speckit.{util_name}

## Execution

1. **Load Skill**: Use the `view_file` tool to read: `.agent/skills/{skill_name}/SKILL.md`
2. **Execute**: Follow the skill instructions with the user's input.

## Usage

```
/util-speckit.{util_name} "your input here"
```
'''


# ============================================================================
# DOCUMENT TEMPLATES
# ============================================================================

def template_spec():
    return '''# Feature Specification: [FEATURE_NAME]

> **Branch**: `[BRANCH_NAME]`
> **Created**: [DATE]
> **Status**: Draft | In Review | Approved
> **Author**: [AUTHOR]

## 1. Overview

### 1.1 Problem Statement
[What problem does this feature solve?]

### 1.2 Proposed Solution
[High-level description of the solution]

### 1.3 Success Criteria
[Measurable, technology-agnostic outcomes]

## 2. User Scenarios

### 2.1 Primary Flow
**As a** [user type]
**I want to** [action]
**So that** [benefit]

#### Steps:
1. [Step 1]
2. [Step 2]
3. [Step 3]

### 2.2 Alternative Flows
[Other user paths]

### 2.3 Edge Cases
[Boundary conditions and error scenarios]

## 3. Functional Requirements

### 3.1 Core Requirements (Mandatory)

| ID | Requirement | Acceptance Criteria | Priority |
|----|-------------|---------------------|----------|
| FR-001 | [Requirement] | [Testable criteria] | P1 |
| FR-002 | [Requirement] | [Testable criteria] | P1 |

### 3.2 Optional Requirements

| ID | Requirement | Acceptance Criteria | Priority |
|----|-------------|---------------------|----------|
| FR-OPT-001 | [Requirement] | [Testable criteria] | P2 |

## 4. Non-Functional Requirements (Optional)

| Category | Requirement |
|----------|-------------|
| Performance | [e.g., Page load < 2s] |
| Security | [e.g., All inputs sanitized] |
| Accessibility | [e.g., WCAG 2.1 AA] |

## 5. Key Entities (Optional)

| Entity | Description | Key Attributes |
|--------|-------------|----------------|
| [Entity] | [What it represents] | [Important fields] |

## 6. Assumptions

- [Assumption 1]
- [Assumption 2]

## 7. Out of Scope

- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

## 8. Dependencies

- [External dependency 1]
- [External dependency 2]
'''


def template_plan():
    return '''# Implementation Plan: [FEATURE_NAME]

> **Branch**: `[BRANCH_NAME]`
> **Spec**: `[SPEC_FILE]`
> **Created**: [DATE]
> **Status**: Draft | Approved

## 1. Technical Context

### 1.1 Tech Stack
| Component | Technology | Version |
|-----------|-----------|---------|
| Language | [e.g., TypeScript] | [e.g., 5.x] |
| Framework | [e.g., Next.js] | [e.g., 15.x] |
| Database | [e.g., PostgreSQL] | [e.g., 16] |
| ORM | [e.g., Prisma] | [e.g., 6.x] |

### 1.2 Existing Architecture
[Description of current system architecture relevant to this feature]

### 1.3 Constitution Check
| Principle | Status | Notes |
|-----------|--------|-------|
| [Principle 1] | ✅ Compliant | [Notes] |
| [Principle 2] | ⚠️ Needs Work | [What needs to change] |

## 2. Research Findings

### 2.1 Decisions Made
| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| [Decision 1] | [Why] | [What else was considered] |

## 3. Data Model

### 3.1 Entities
[Reference to data-model.md or inline entity definitions]

### 3.2 Relationships
[Entity relationship descriptions]

## 4. API Contracts

### 4.1 Endpoints
[Reference to contracts/ directory or inline endpoint definitions]

## 5. Project Structure

```
src/
├── [module]/
│   ├── components/
│   ├── services/
│   ├── models/
│   └── utils/
```

## 6. Implementation Strategy

### 6.1 Phase Approach
1. **Phase 1**: [Foundation - what gets built first]
2. **Phase 2**: [Core features]
3. **Phase 3**: [Advanced features]

### 6.2 Risk Mitigation
| Risk | Mitigation |
|------|------------|
| [Risk 1] | [Strategy] |

## 7. Testing Strategy

- Unit tests for: [areas]
- Integration tests for: [areas]
- E2E tests for: [critical paths]
'''


def template_tasks():
    return '''# 📋 Tasks: [FEATURE_NAME]

> **Branch**: `[BRANCH_NAME]`
> **Plan**: `[PLAN_FILE]`
> **Generated**: [DATE]
> **Status**: ⬜ Todo | 🔄 In Progress | ✅ Done | ⏸️ Blocked

## Progress Overview

| Phase | Total | Done | In Progress | Remaining |
|-------|-------|------|-------------|-----------|
| Phase 1: Setup | 0 | 0 | 0 | 0 |
| Phase 2: Foundation | 0 | 0 | 0 | 0 |
| Phase 3: US1 | 0 | 0 | 0 | 0 |
| Phase N: Polish | 0 | 0 | 0 | 0 |

---

## Phase 1: Setup

**Goal**: Initialize project structure and tooling.

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Configure development environment
- [ ] T003 Setup version control and branch strategy

## Phase 2: Foundation

**Goal**: Build blocking prerequisites for all user stories.

- [ ] T004 [P] Setup database schema
- [ ] T005 [P] Configure authentication middleware

## Phase 3: User Story 1 - [US1_TITLE]

**Goal**: [User story 1 objective]
**Independent Test**: [How to verify this story works independently]

- [ ] T006 [US1] Create [Entity] model in src/models/[entity].py
- [ ] T007 [US1] Implement [Entity]Service in src/services/[entity]_service.py
- [ ] T008 [US1] Create API endpoint in src/routes/[entity].py

## Phase N: Polish & Cross-Cutting

**Goal**: Final polish and cross-cutting concerns.

- [ ] T0XX Documentation update
- [ ] T0XX Performance optimization review
- [ ] T0XX Security audit

---

## Dependencies

```
T001 → T004, T005 (Setup before Foundation)
T004, T005 → T006 (Foundation before US1)
```

## Implementation Strategy

- **MVP**: Complete Phase 1-3 (Setup + Foundation + US1)
- **Incremental**: Add user stories one at a time
- **Parallel**: Tasks marked [P] can run concurrently
'''


def template_constitution():
    return '''# 📜 Project Constitution: [PROJECT_NAME]

> **Version**: [CONSTITUTION_VERSION]
> **Ratified**: [RATIFICATION_DATE]
> **Last Amended**: [LAST_AMENDED_DATE]

## Preamble

This Constitution establishes the non-negotiable principles, standards, and governance rules for the **[PROJECT_NAME]** project. All agents, contributors, and automated systems MUST comply with this document.

---

## Principles

### Principle 1: [PRINCIPLE_1_NAME]

[PRINCIPLE_1_DESCRIPTION]

**Rationale**: [PRINCIPLE_1_RATIONALE]

### Principle 2: [PRINCIPLE_2_NAME]

[PRINCIPLE_2_DESCRIPTION]

**Rationale**: [PRINCIPLE_2_RATIONALE]

### Principle 3: [PRINCIPLE_3_NAME]

[PRINCIPLE_3_DESCRIPTION]

**Rationale**: [PRINCIPLE_3_RATIONALE]

---

## Technology Standards

| Category | Standard | Justification |
|----------|----------|---------------|
| Language | [LANGUAGE] | [WHY] |
| Framework | [FRAMEWORK] | [WHY] |
| Testing | [TEST_FRAMEWORK] | [WHY] |
| Linting | [LINT_TOOL] | [WHY] |

---

## Governance

### Amendment Process

1. Propose change via conversation or PR
2. Update version according to SemVer:
   - **MAJOR**: Backward incompatible changes
   - **MINOR**: New principles or expanded guidance
   - **PATCH**: Clarifications, typo fixes
3. Update `LAST_AMENDED_DATE`
4. Propagate changes to affected templates

### Compliance Review

- Every feature MUST be checked against this Constitution during planning (see plan-template.md Constitution Check)
- Violations MUST be documented and justified or resolved before implementation
'''


# ============================================================================
# SCRIPT TEMPLATES
# ============================================================================

def script_create_new_feature():
    return '''#!/usr/bin/env bash
# create-new-feature.sh - Create a new feature branch and spec directory
# Usage: ./create-new-feature.sh [--json] "feature description" [--number N] [--short-name "name"]

set -euo pipefail

JSON_OUTPUT=false
FEATURE_DESC=""
FEATURE_NUM=""
SHORT_NAME=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --json) JSON_OUTPUT=true; shift ;;
        --number) FEATURE_NUM="$2"; shift 2 ;;
        --short-name) SHORT_NAME="$2"; shift 2 ;;
        *) FEATURE_DESC="$1"; shift ;;
    esac
done

if [ -z "$FEATURE_DESC" ]; then
    echo "ERROR: No feature description provided" >&2
    exit 1
fi

# Auto-generate short name if not provided
if [ -z "$SHORT_NAME" ]; then
    SHORT_NAME=$(echo "$FEATURE_DESC" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]//g' | tr ' ' '-' | cut -c1-30)
fi

# Auto-detect next number if not provided
if [ -z "$FEATURE_NUM" ]; then
    FEATURE_NUM=1
    # Check existing branches
    EXISTING=$(git branch -a 2>/dev/null | grep -oP '\\d+(?=-'"$SHORT_NAME"')' | sort -n | tail -1)
    if [ -n "$EXISTING" ]; then
        FEATURE_NUM=$((EXISTING + 1))
    fi
fi

BRANCH_NAME="${FEATURE_NUM}-${SHORT_NAME}"
SPECS_DIR="specs/${BRANCH_NAME}"
SPEC_FILE="${SPECS_DIR}/spec.md"

# Create directory structure
mkdir -p "$SPECS_DIR"
mkdir -p "${SPECS_DIR}/checklists"
mkdir -p "${SPECS_DIR}/contracts"

# Create and checkout branch
git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"

# Output
if [ "$JSON_OUTPUT" = true ]; then
    cat <<EOF
{
    "BRANCH_NAME": "$BRANCH_NAME",
    "FEATURE_NUM": $FEATURE_NUM,
    "SHORT_NAME": "$SHORT_NAME",
    "SPECS_DIR": "$(pwd)/$SPECS_DIR",
    "SPEC_FILE": "$(pwd)/$SPEC_FILE",
    "FEATURE_DESC": "$FEATURE_DESC"
}
EOF
else
    echo "Created branch: $BRANCH_NAME"
    echo "Specs dir: $SPECS_DIR"
    echo "Spec file: $SPEC_FILE"
fi
'''


def script_setup_plan():
    return '''#!/usr/bin/env bash
# setup-plan.sh - Setup plan directory and locate feature spec
# Usage: ./setup-plan.sh [--json]

set -euo pipefail

JSON_OUTPUT=false
[ "${1:-}" = "--json" ] && JSON_OUTPUT=true

# Detect current feature branch
BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
SPECS_DIR="specs/$BRANCH"
SPEC_FILE="$SPECS_DIR/spec.md"
PLAN_FILE="$SPECS_DIR/plan.md"

if [ ! -f "$SPEC_FILE" ]; then
    echo "ERROR: No spec.md found at $SPEC_FILE" >&2
    echo "Run /speckit.specify first to create a specification." >&2
    exit 1
fi

if [ "$JSON_OUTPUT" = true ]; then
    cat <<EOF
{
    "BRANCH": "$BRANCH",
    "SPECS_DIR": "$(pwd)/$SPECS_DIR",
    "FEATURE_SPEC": "$(pwd)/$SPEC_FILE",
    "IMPL_PLAN": "$(pwd)/$PLAN_FILE"
}
EOF
else
    echo "Branch: $BRANCH"
    echo "Spec: $SPEC_FILE"
    echo "Plan: $PLAN_FILE"
fi
'''


def script_check_prerequisites():
    return '''#!/usr/bin/env bash
# check-prerequisites.sh - Verify all prerequisite artifacts exist
# Usage: ./check-prerequisites.sh [--json] [--require-tasks] [--include-tasks]

set -euo pipefail

JSON_OUTPUT=false
REQUIRE_TASKS=false
INCLUDE_TASKS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --json) JSON_OUTPUT=true; shift ;;
        --require-tasks) REQUIRE_TASKS=true; shift ;;
        --include-tasks) INCLUDE_TASKS=true; shift ;;
        *) shift ;;
    esac
done

BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
FEATURE_DIR="specs/$BRANCH"

AVAILABLE_DOCS=()

# Check required docs
[ -f "$FEATURE_DIR/spec.md" ] && AVAILABLE_DOCS+=("spec.md")
[ -f "$FEATURE_DIR/plan.md" ] && AVAILABLE_DOCS+=("plan.md")
[ -f "$FEATURE_DIR/tasks.md" ] && AVAILABLE_DOCS+=("tasks.md")
[ -f "$FEATURE_DIR/data-model.md" ] && AVAILABLE_DOCS+=("data-model.md")
[ -f "$FEATURE_DIR/research.md" ] && AVAILABLE_DOCS+=("research.md")
[ -f "$FEATURE_DIR/quickstart.md" ] && AVAILABLE_DOCS+=("quickstart.md")
[ -d "$FEATURE_DIR/contracts" ] && AVAILABLE_DOCS+=("contracts/")
[ -d "$FEATURE_DIR/checklists" ] && AVAILABLE_DOCS+=("checklists/")

if [ "$REQUIRE_TASKS" = true ] && [ ! -f "$FEATURE_DIR/tasks.md" ]; then
    echo "ERROR: tasks.md required but not found. Run /speckit.tasks first." >&2
    exit 1
fi

if [ "$JSON_OUTPUT" = true ]; then
    DOCS_JSON=$(printf '"%s",' "${AVAILABLE_DOCS[@]}" | sed 's/,$//')
    cat <<EOF
{
    "BRANCH": "$BRANCH",
    "FEATURE_DIR": "$(pwd)/$FEATURE_DIR",
    "AVAILABLE_DOCS": [$DOCS_JSON]
}
EOF
else
    echo "Branch: $BRANCH"
    echo "Feature Dir: $FEATURE_DIR"
    echo "Available: ${AVAILABLE_DOCS[*]}"
fi
'''


def script_update_agent_context():
    return '''#!/usr/bin/env bash
# update-agent-context.sh - Update agent-specific context files
# Usage: ./update-agent-context.sh [agent_type]

set -euo pipefail

AGENT_TYPE="${1:-antigravity}"

echo "Updating agent context for: $AGENT_TYPE"

BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
FEATURE_DIR="specs/$BRANCH"
CONTEXT_FILE=".agent/memory/${AGENT_TYPE}-context.md"

mkdir -p "$(dirname "$CONTEXT_FILE")"

# Generate context from current feature artifacts
{
    echo "# Agent Context: $AGENT_TYPE"
    echo ""
    echo "> Auto-generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "> Feature: $BRANCH"
    echo ""
    
    if [ -f "$FEATURE_DIR/plan.md" ]; then
        echo "## Tech Stack (from plan.md)"
        grep -A 20 "Tech Stack" "$FEATURE_DIR/plan.md" 2>/dev/null || echo "N/A"
        echo ""
    fi
    
    if [ -f "$FEATURE_DIR/data-model.md" ]; then
        echo "## Data Model Summary"
        head -30 "$FEATURE_DIR/data-model.md" 2>/dev/null
        echo ""
    fi
    
    echo "## Available Artifacts"
    ls -1 "$FEATURE_DIR/" 2>/dev/null || echo "None"
} > "$CONTEXT_FILE"

echo "Context written to: $CONTEXT_FILE"
'''


# ============================================================================
# Mapping: script name → template function
# ============================================================================
SCRIPT_TEMPLATE_MAP = {
    "create-new-feature.sh": script_create_new_feature,
    "setup-plan.sh": script_setup_plan,
    "check-prerequisites.sh": script_check_prerequisites,
    "update-agent-context.sh": script_update_agent_context,
}

DOCUMENT_TEMPLATE_MAP = {
    "spec-template.md": template_spec,
    "plan-template.md": template_plan,
    "tasks-template.md": template_tasks,
    "constitution-template.md": template_constitution,
}
