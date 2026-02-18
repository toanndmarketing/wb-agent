"""
Generator - Core logic tạo cấu trúc .agent/ cho project.
"""

import os
import stat
from datetime import datetime

from .registry import SKILLS_REGISTRY, WORKFLOWS_REGISTRY
from .templates import (
    SKILL_TEMPLATE_MAP,
    SCRIPT_TEMPLATE_MAP,
    DOCUMENT_TEMPLATE_MAP,
    workflow_all,
    workflow_numbered,
    workflow_prepare,
    workflow_util,
)


class ProjectGenerator:
    """Sinh cấu trúc .agent/ cho project theo chuẩn Spec-Kit Antigravity."""

    def __init__(self, target_dir: str, project_name: str):
        self.target_dir = target_dir
        self.project_name = project_name
        self.agent_dir = os.path.join(target_dir, ".agent")
        self.stats = {
            "skills_created": 0,
            "workflows_created": 0,
            "scripts_created": 0,
            "templates_created": 0,
            "directories_created": 0,
        }

    def generate(self):
        """Thực thi toàn bộ quá trình sinh cấu trúc."""
        print("📁 Tạo cấu trúc thư mục...")
        self._create_directories()

        print("🧠 Tạo Skills (SKILL.md)...")
        self._create_skills()

        print("🔄 Tạo Workflows...")
        self._create_workflows()

        print("📄 Tạo Templates...")
        self._create_templates()

        print("🔧 Tạo Scripts...")
        self._create_scripts()

        print("📝 Tạo Memory (Constitution)...")
        self._create_memory()

        print("📊 Tạo README.md cho .agent/...")
        self._create_agent_readme()

        self._print_stats()

    def _create_directories(self):
        """Tạo cấu trúc thư mục .agent/."""
        dirs = [
            ".agent/skills",
            ".agent/workflows",
            ".agent/scripts/bash",
            ".agent/templates",
            ".agent/memory",
        ]

        # Tạo thư mục cho mỗi skill
        for skill in SKILLS_REGISTRY:
            dirs.append(f".agent/skills/{skill['name']}")

        for d in dirs:
            full_path = os.path.join(self.target_dir, d)
            os.makedirs(full_path, exist_ok=True)
            self.stats["directories_created"] += 1

    def _create_skills(self):
        """Tạo SKILL.md cho mỗi skill."""
        for skill in SKILLS_REGISTRY:
            skill_name = skill["name"]
            skill_dir = os.path.join(self.agent_dir, "skills", skill_name)
            skill_file = os.path.join(skill_dir, "SKILL.md")

            # Lấy template từ map
            template_fn = SKILL_TEMPLATE_MAP.get(skill_name)
            if template_fn:
                content = template_fn()
            else:
                # Fallback: tạo basic SKILL.md từ registry metadata
                content = self._generate_basic_skill(skill)

            self._write_file(skill_file, content)
            self.stats["skills_created"] += 1

    def _generate_basic_skill(self, skill: dict) -> str:
        """Tạo SKILL.md cơ bản từ registry metadata."""
        handoffs_yaml = ""
        for h in skill.get("handoffs", []):
            handoffs_yaml += f"""  - label: {h['label']}
    agent: {h['agent']}
    prompt: {h['prompt']}
    send: true
"""

        depends = ""
        for dep in skill.get("depends_on", []):
            depends += f"  - {dep}\n"

        return f"""---
name: {skill['name']}
description: {skill['description']}
version: {skill.get('version', '1.0.0')}
{f"depends-on:\\n{depends}" if depends else ""}handoffs:
{handoffs_yaml if handoffs_yaml else "  []"}
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role
You are the **{skill['role']}**. {skill['description']}

## Task

### Outline

1. **Setup**: Load context from the active feature directory.
2. **Execute**: Perform the primary task described above.
3. **Report**: Output results and next steps.
"""

    def _create_workflows(self):
        """Tạo workflow .md files."""
        for wf in WORKFLOWS_REGISTRY:
            cmd = wf["command"]
            desc = wf["description"]
            filepath = os.path.join(self.agent_dir, "workflows", f"{cmd}.md")

            if cmd == "00-speckit.all":
                content = workflow_all()
            elif cmd == "speckit.prepare":
                content = workflow_prepare()
            elif cmd.startswith("util-speckit."):
                util_name = cmd.replace("util-speckit.", "")
                skill_name = f"speckit.{util_name}"
                content = workflow_util(util_name, skill_name, desc)
            elif cmd[0:2].isdigit():
                number = cmd.split("-")[0]
                skill_name = wf["skills"][0] if wf["skills"] else cmd
                content = workflow_numbered(number, skill_name, desc, f"speckit.{skill_name}")
            else:
                content = workflow_numbered("", cmd, desc, cmd)

            self._write_file(filepath, content)
            self.stats["workflows_created"] += 1

    def _create_templates(self):
        """Tạo document templates (spec, plan, tasks, constitution)."""
        for filename, template_fn in DOCUMENT_TEMPLATE_MAP.items():
            filepath = os.path.join(self.agent_dir, "templates", filename)
            content = template_fn()
            self._write_file(filepath, content)
            self.stats["templates_created"] += 1

    def _create_scripts(self):
        """Tạo bash scripts."""
        for filename, script_fn in SCRIPT_TEMPLATE_MAP.items():
            filepath = os.path.join(self.agent_dir, "scripts", "bash", filename)
            content = script_fn()
            self._write_file(filepath, content)

            # Make script executable (Unix)
            try:
                st = os.stat(filepath)
                os.chmod(filepath, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
            except Exception:
                pass  # Windows doesn't support chmod the same way

            self.stats["scripts_created"] += 1

    def _create_memory(self):
        """Tạo initial constitution file trong memory/."""
        filepath = os.path.join(self.agent_dir, "memory", "constitution.md")
        today = datetime.now().strftime("%Y-%m-%d")

        content = f"""# 📜 Project Constitution: {self.project_name}

> **Version**: 1.0.0
> **Ratified**: {today}
> **Last Amended**: {today}

## Preamble

This Constitution establishes the non-negotiable principles, standards, and governance rules for the **{self.project_name}** project. All agents, contributors, and automated systems MUST comply with this document.

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
2. Update version according to SemVer
3. Update `LAST_AMENDED_DATE`
4. Propagate changes to affected templates

### Compliance Review

- Every feature MUST be checked against this Constitution during planning
- Violations MUST be documented and justified or resolved before implementation

---

> 💡 Run `/01-speckit.constitution` to fill in the placeholders above interactively.
"""
        self._write_file(filepath, content)

    def _create_agent_readme(self):
        """Tạo README.md cho .agent/ directory."""
        today = datetime.now().strftime("%Y-%m-%d")

        content = f"""# 🤖 Antigravity Agent Configuration

> **Project**: {self.project_name}
> **Generated**: {today}
> **Generator**: Antigravity SSD (Spec-Driven Development)

## Structure

```
.agent/
├── skills/          # @ Mentions (17 agentic capabilities)
├── workflows/       # / Slash Commands (19 orchestration workflows)
├── templates/       # Document templates (spec, plan, tasks, constitution)
├── scripts/bash/    # Shared utility scripts
└── memory/          # Project constitution & context
```

## Quick Start

1. **Set up Constitution**: `/01-speckit.constitution`
2. **Create Feature Spec**: `/02-speckit.specify "Your feature description"`
3. **Create Plan**: `/04-speckit.plan`
4. **Break into Tasks**: `/05-speckit.tasks`
5. **Implement**: `/07-speckit.implement`

Or run the full pipeline: `/00-speckit.all "Your feature description"`

## Skills (@ Mentions)

| Skill | Description |
|-------|-------------|
"""
        for skill in SKILLS_REGISTRY:
            content += f"| `@{skill['name']}` | {skill['description']} |\n"

        content += f"""
## Workflows (/ Commands)

| Command | Description |
|---------|-------------|
"""
        for wf in WORKFLOWS_REGISTRY:
            content += f"| `/{wf['command']}` | {wf['description']} |\n"

        content += """
## Pipeline Flow

```
Constitution → Specify → Clarify → Plan → Tasks → Analyze → Implement → Test → Review → Validate
     01          02        03       04      05       06         07        09     10       11
```

## Best Practices

1. **Never skip Constitution** - It's the anchor that prevents AI hallucination
2. **Layered Defense** - Each step validates the previous one
3. **15-Minute Rule** - Tasks should be completable in ≤15 minutes
4. **Refine, Don't Rewind** - Build incrementally, never start over
"""
        filepath = os.path.join(self.agent_dir, "README.md")
        self._write_file(filepath, content)

    def _write_file(self, filepath: str, content: str):
        """Ghi nội dung vào file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def _print_stats(self):
        """In thống kê tạo file."""
        print(f"\n{'─' * 50}")
        print(f"  📊 Thống kê:")
        print(f"     📁 Thư mục:   {self.stats['directories_created']}")
        print(f"     🧠 Skills:    {self.stats['skills_created']}")
        print(f"     🔄 Workflows: {self.stats['workflows_created']}")
        print(f"     📄 Templates: {self.stats['templates_created']}")
        print(f"     🔧 Scripts:   {self.stats['scripts_created']}")
        print(f"{'─' * 50}")
