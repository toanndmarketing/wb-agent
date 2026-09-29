"""
Generator v2.0 — "Thin Agent" engine.
Sinh output gọn: .agents/ chỉ ~8 files, 3 IDE rules.
Kế thừa Global Rules, chỉ giữ project-specific context.
"""

import os
import json
from datetime import datetime

from .registry import get_project_type_info
from .templates import (
    render_master_identity,
    render_constitution,
    render_agents_md,
    render_cursor_rules,
    render_claude_md,
)
from .scanner import ProjectScanner


class ProjectGenerator:
    """Sinh cấu trúc .agents/ v2.0 cho project."""

    def __init__(
        self,
        target_dir: str,
        project_name: str,
        project_type: str = "fullstack",
        scan_profile: dict = None,
    ):
        self.target_dir = target_dir
        self.project_name = project_name
        self.project_type = project_type
        self.scan_profile = scan_profile
        self.agents_dir = os.path.join(target_dir, ".agents")
        self.type_info = get_project_type_info(project_type)

        self.stats = {
            "files_created": 0,
            "dirs_created": 0,
        }

    def generate(self):
        """Thực thi toàn bộ quá trình sinh cấu trúc."""
        needs_docker = self.type_info.get("needs_docker", True)
        needs_seo = self.type_info.get("needs_seo", False)

        # ─── 1. Tạo thư mục ───
        print("📁 Tạo cấu trúc .agents/ (v2.0 Thin Agent)...")
        self._create_directories()

        # ─── 2. Master Identity ───
        print("🧠 Tạo Master Identity...")
        scan_context = self._build_scan_context()
        self._write_file(
            os.path.join(self.agents_dir, "identity", "master-identity.md"),
            render_master_identity(self.project_name, self.type_info["label"], scan_context),
        )

        # ─── 3. Constitution ───
        print("📜 Tạo Constitution...")
        self._write_file(
            os.path.join(self.agents_dir, "memory", "constitution.md"),
            render_constitution(self.project_name, needs_docker, self.project_type),
        )

        # ─── 4. Project-scoped AGENTS.md (auto-loaded by Antigravity) ───
        print("📋 Tạo Project Rules (.agents/AGENTS.md)...")
        self._write_file(
            os.path.join(self.agents_dir, "AGENTS.md"),
            render_agents_md(self.project_name, needs_docker, needs_seo),
        )

        # ─── 5. Project config ───
        self._write_project_config()

        # ─── 6. IDE Rules (3 IDE only) ───
        print("🖥️  Tạo IDE Rules (Antigravity + Cursor + Claude Code)...")
        self._create_ide_rules(needs_docker, needs_seo)

        # ─── 7. Scan output tóm tắt ───
        if self.scan_profile and self.scan_profile.get("has_existing_code"):
            scanner = ProjectScanner(self.target_dir)
            scanner.profile = self.scan_profile
            print(scanner.generate_report())

        self._print_summary()

    def _create_directories(self):
        """Tạo cấu trúc thư mục .agents/ tối giản."""
        dirs = [
            ".agents/identity",
            ".agents/memory",
            ".agents/specs",
            ".agents/skills",
        ]
        for d in dirs:
            full_path = os.path.join(self.target_dir, d)
            os.makedirs(full_path, exist_ok=True)
            self.stats["dirs_created"] += 1

    def _create_ide_rules(self, needs_docker: bool, needs_seo: bool):
        """Tạo rules cho 3 IDE: Antigravity, Cursor, Claude Code."""
        name = self.project_name

        # 1. Antigravity — .agents/AGENTS.md (đã tạo ở bước 4)
        print("  ✅ Antigravity  → .agents/AGENTS.md")

        # 2. Cursor — .cursor/rules/wb-agent.mdc
        cursor_dir = os.path.join(self.target_dir, ".cursor", "rules")
        os.makedirs(cursor_dir, exist_ok=True)
        self._write_file(
            os.path.join(cursor_dir, "wb-agent.mdc"),
            render_cursor_rules(name, needs_docker),
        )
        print("  ✅ Cursor       → .cursor/rules/wb-agent.mdc")

        # 3. Claude Code — CLAUDE.md (root)
        self._write_file(
            os.path.join(self.target_dir, "CLAUDE.md"),
            render_claude_md(name, needs_docker),
        )
        print("  ✅ Claude Code  → CLAUDE.md")

    def _build_scan_context(self) -> str:
        """Gộp scan data vào 1 string cho master-identity.md."""
        if not self.scan_profile or not self.scan_profile.get("has_existing_code"):
            return ""

        p = self.scan_profile
        parts = []

        if p.get("framework"):
            parts.append(f"- **Framework**: {p['framework']}")
        if p.get("language"):
            parts.append(f"- **Language**: {p['language']}")
        if p.get("tech_stack"):
            parts.append(f"- **Tech Stack**: {', '.join(p['tech_stack'])}")
        if p.get("package_manager"):
            parts.append(f"- **Package Manager**: {p['package_manager']}")

        # Database
        db = p.get("database", {})
        if db.get("has_prisma"):
            models = db.get("models", [])
            model_names = [m["name"] for m in models[:10]]
            parts.append(f"- **Database**: {db.get('type', 'Unknown')} ({len(models)} models: {', '.join(model_names)})")

        # Docker
        docker = p.get("docker", {})
        if docker.get("has_compose"):
            services = docker.get("services", [])
            ports = docker.get("ports", [])
            parts.append(f"- **Docker Services**: {', '.join(services)}")
            if ports:
                parts.append(f"- **Port Mapping**:")
                for port in ports:
                    parts.append(f"  - {port}")

        # API Routes
        api = p.get("api", {})
        if api.get("routes"):
            routes = api["routes"]
            parts.append(f"- **API Routes** ({len(routes)}): {', '.join(routes[:8])}")

        # Pages
        if p.get("pages"):
            pages = p["pages"]
            parts.append(f"- **Pages** ({len(pages)}): {', '.join(pages[:8])}")

        # ENV
        if p.get("env_vars"):
            parts.append(f"- **ENV Variables**: {', '.join(p['env_vars'][:10])}")

        # Source structure
        if p.get("source_structure"):
            parts.append(f"- **Structure**:")
            for item in p["source_structure"][:15]:
                parts.append(f"  - {item}")

        return "\n".join(parts)

    def _write_project_config(self):
        """Lưu metadata vào .agents/project.json."""
        config = {
            "project_name": self.project_name,
            "project_type": self.project_type,
            "wb_agent_version": "2.0.0",
            "created_at": datetime.now().isoformat(),
        }
        self._write_file(
            os.path.join(self.agents_dir, "project.json"),
            json.dumps(config, indent=2, ensure_ascii=False),
        )

    def _write_file(self, filepath: str, content: str):
        """Ghi file, tạo thư mục cha nếu cần."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        self.stats["files_created"] += 1

    def _print_summary(self):
        """In thống kê kết quả."""
        print(f"\n{'─' * 50}")
        print(f"📊 wb-agent v2.0 — Thin Agent Output:")
        print(f"  📁 Directories: {self.stats['dirs_created']}")
        print(f"  📄 Files:       {self.stats['files_created']}")
        print(f"  🏗️ Type:        {self.type_info['label']}")
        print(f"{'─' * 50}")
        print()
        print("💡 Bước tiếp theo:")
        print("  1. Điền thông tin vào .agents/identity/master-identity.md")
        print("  2. Cập nhật constitution tại .agents/memory/constitution.md")
        print("  3. Bắt đầu: /02-speckit.specify 'Mô tả feature...'")
        print()
