"""
Generator - Core logic tạo cấu trúc .agent/ chuẩn ASF 3.3.
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
)


class ProjectGenerator:
    """Sinh cấu trúc .agent/ cho project theo chuẩn Spec-Kit & ASF 3.3."""

    def __init__(self, target_dir: str, project_name: str):
        self.target_dir = target_dir
        self.project_name = project_name
        self.agent_dir = os.path.join(target_dir, ".agent")
        self.stats = {
            "skills": 0,
            "workflows": 0,
            "templates": 0,
            "scripts": 0,
            "directories": 0,
            "identity": 0,
            "knowledge": 0
        }

    def generate(self):
        """Thực thi toàn bộ quá trình sinh cấu trúc."""
        print("📁 Tạo cấu trúc thư mục (ASF 3.3 Standard)...")
        self._create_directories()

        print("🎭 Thiết lập Identity & Soul...")
        self._create_identity()

        print("🧠 Khởi tạo Knowledge Base...")
        self._create_knowledge_base()

        print("🛠️ Tạo Skills (@mentions)...")
        self._create_skills()

        print("🔄 Tạo Workflows (/commands)...")
        self._create_workflows()

        print("📄 Tạo Templates & Memory...")
        self._create_templates()
        self._create_memory()

        print("🔧 Tạo Bash Scripts...")
        self._create_scripts()

        self._create_agent_readme()
        self._print_stats()

    def _create_directories(self):
        """Tạo cấu trúc thư mục .agent/ theo chuẩn ASF 3.3."""
        dirs = [
            ".agent/identity",       # Tầng nhân cách
            ".agent/knowledge_base", # Tầng tri thức dự án
            ".agent/skills",         # Tầng kỹ năng (@skill)
            ".agent/workflows",      # Tầng điều hướng (/command)
            ".agent/scripts/bash",   # Tầng hạ tầng
            ".agent/templates",      # Tầng khuôn mẫu
            ".agent/memory",         # Tầng lưu trữ Constitution
        ]

        for d in dirs:
            full_path = os.path.join(self.target_dir, d)
            os.makedirs(full_path, exist_ok=True)
            self.stats["directories"] += 1

    def _create_identity(self):
        """Tạo Master Identity chuẩn nhân cách AI."""
        filepath = os.path.join(self.agent_dir, "identity", "master-identity.md")
        template_fn = DOCUMENT_TEMPLATE_MAP.get("identity-template.md")
        content = template_fn()
        self._write_file(filepath, content)
        self.stats["identity"] += 1

    def _create_knowledge_base(self):
        """Tạo các file tri thức nền tảng."""
        base_path = os.path.join(self.agent_dir, "knowledge_base")
        
        # Infra file from template
        infra_path = os.path.join(base_path, "infrastructure.md")
        infra_template = DOCUMENT_TEMPLATE_MAP.get("infrastructure-template.md")
        self._write_file(infra_path, infra_template())

        files = {
            "business_logic.md": "# Business Logic\n\nĐịnh nghĩa logic nghiệp vụ cốt lõi tại đây.",
            "data_schema.md": "# Data Schema\n\nĐịnh nghĩa cấu trúc database, quan hệ thực thể tại đây.",
            "api_standards.md": "# API Standards\n\nQuy tắc thiết kế API, error codes, auth headers.",
        }
        for name, content in files.items():
            self._write_file(os.path.join(base_path, name), content)
            self.stats["knowledge"] += 1

    def _create_skills(self):
        """Tạo SKILL.md cho mỗi skill."""
        for skill in SKILLS_REGISTRY:
            skill_name = skill["name"]
            skill_dir = os.path.join(self.agent_dir, "skills", skill_name)
            os.makedirs(skill_dir, exist_ok=True)
            skill_file = os.path.join(skill_dir, "SKILL.md")

            template_fn = SKILL_TEMPLATE_MAP.get(skill_name)
            if template_fn:
                content = template_fn()
            else:
                content = self._generate_basic_skill(skill)

            self._write_file(skill_file, content)
            self.stats["skills"] += 1

    def _generate_basic_skill(self, skill):
        return f"""---
name: {skill['name']}
description: {skill['description']}
role: {skill['role']}
---

## Role
Bạn là **{skill['role']}**. 

## Task
{skill['description']}

## Execution Outline
1. Load context from `.agent/identity/master-identity.md`.
2. Check `.agent/memory/constitution.md` for rules.
3. Perform the primary task.
4. Report results.
"""

    def _create_workflows(self):
        """Tạo workflow .md files."""
        for wf in WORKFLOWS_REGISTRY:
            cmd = wf["command"]
            filepath = os.path.join(self.agent_dir, "workflows", f"{cmd}.md")
            
            # Simplified workflow generation for demo
            content = f"---\ndescription: {wf['description']}\n---\n\n# Workflow: {cmd}\n\n1. Run @{wf['skills'][0] if wf['skills'] else 'speckit.tasks'}"
            if cmd == "00-speckit.all":
                content = workflow_all()
            
            self._write_file(filepath, content)
            self.stats["workflows"] += 1

    def _create_templates(self):
        for filename, template_fn in DOCUMENT_TEMPLATE_MAP.items():
            if filename == "identity-template.md": continue
            filepath = os.path.join(self.agent_dir, "templates", filename)
            self._write_file(filepath, template_fn())
            self.stats["templates"] += 1

    def _create_memory(self):
        filepath = os.path.join(self.agent_dir, "memory", "constitution.md")
        template_fn = DOCUMENT_TEMPLATE_MAP.get("constitution-template.md")
        self._write_file(filepath, template_fn())

    def _create_scripts(self):
        for filename, script_fn in SCRIPT_TEMPLATE_MAP.items():
            filepath = os.path.join(self.agent_dir, "scripts", "bash", filename)
            self._write_file(filepath, script_fn())
            try:
                os.chmod(filepath, os.stat(filepath).st_mode | stat.S_IEXEC)
            except: pass
            self.stats["scripts"] += 1

    def _create_agent_readme(self):
        today = datetime.now().strftime("%Y-%m-%d")
        content = f"""# 🤖 WB-Agent Configuration (ASF 3.3)

> **Project**: {self.project_name}
> **Generated**: {today}

## 🏗️ Architecture

- `.agent/identity/`: Định nghĩa Persona & Soul của AI.
- `.agent/knowledge_base/`: Kho tri thức về Business, Data, API.
- `.agent/skills/`: Các kỹ năng AI chuyên biệt (@mentions).
- `.agent/workflows/`: Các quy trình tự động hóa (/commands).
- `.agent/memory/`: Project Constitution (Luật dự án).

## 🚀 Quick Start
1. Run `/01-speckit.constitution` để thiết lập luật dự án.
2. Run `@speckit.identity` để tinh chỉnh Persona của AI.
3. Run `/02-speckit.specify` để bắt đầu tính năng mới.
"""
        self._write_file(os.path.join(self.agent_dir, "README.md"), content)

    def _write_file(self, filepath, content):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def _print_stats(self):
        print(f"\n{'─' * 50}")
        print(f"📊 Thống kê khởi tạo (ASF 3.3):")
        print(f"  🎭 Identity:  {self.stats['identity']}")
        print(f"  🧠 Knowledge: {self.stats['knowledge']}")
        print(f"  🛠️ Skills:    {self.stats['skills']}")
        print(f"  🔄 Workflows: {self.stats['workflows']}")
        print(f"  📄 Templates: {self.stats['templates']}")
        print(f"{'─' * 50}\n")
