#!/usr/bin/env python3
"""
⚡ WB-Agent v2.0 — Thin Agent CLI
Sinh cấu trúc .agents/ tối giản, kế thừa Global Rules.

    wb-agent init                           # Smart-detect project type
    wb-agent init --type fullstack          # Chỉ định type
    wb-agent init --target /path/to/project # Chỉ định target
    wb-agent validate                       # Validate cấu trúc .agents/
"""

import argparse
import sys
import os

from wb_agent import __version__
from wb_agent.generator import ProjectGenerator
from wb_agent.scanner import ProjectScanner
from wb_agent.registry import PROJECT_TYPES, auto_detect_project_type


def _ask_project_type():
    """Hỏi người dùng chọn loại dự án (chỉ khi auto-detect thất bại)."""
    print("\n🏗️  Không tự detect được loại dự án. Vui lòng chọn:")
    types_list = list(PROJECT_TYPES.items())
    for i, (key, info) in enumerate(types_list, 1):
        print(f"  [{i}] {info['label']} — {info['description']}")

    while True:
        try:
            choice = input(f"\n  Chọn (1-{len(types_list)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(types_list):
                return types_list[idx][0]
        except (ValueError, IndexError):
            pass
        print(f"  ⚠️  Vui lòng chọn số từ 1 đến {len(types_list)}")


def cmd_init(args):
    """Khởi tạo cấu trúc .agents/ cho project."""
    target = os.path.abspath(args.target or os.getcwd())
    name = args.name or os.path.basename(target)
    force = getattr(args, "force", False)
    explicit_type = getattr(args, "type", None)

    agents_dir = os.path.join(target, ".agents")

    print(f"\n⚡ WB-Agent v{__version__} — Thin Agent")
    print(f"{'─' * 50}")
    print(f"  📁 Target:  {target}")
    print(f"  📛 Project: {name}")
    print(f"{'─' * 50}\n")

    # Check existing
    if os.path.exists(agents_dir) and not force:
        response = input("⚠️  .agents/ đã tồn tại. Ghi đè? (y/N): ").strip().lower()
        if response != "y":
            print("❌ Đã hủy.")
            return

    # ─── SCAN CODEBASE ───
    print("🔬 Đang quét codebase...")
    scanner = ProjectScanner(target)
    scan_profile = scanner.scan()

    if scan_profile["has_existing_code"]:
        print(scanner.generate_report())
    else:
        print("  📭 Dự án trống — sử dụng template mặc định.\n")

    # ─── DETECT / SELECT PROJECT TYPE ───
    if explicit_type:
        project_type = explicit_type
        if project_type not in PROJECT_TYPES:
            print(f"❌ Type '{project_type}' không hợp lệ.")
            print(f"   Các type có sẵn: {', '.join(PROJECT_TYPES.keys())}")
            return
        print(f"  🏗️ Project Type: {PROJECT_TYPES[project_type]['label']} (user specified)")
    else:
        detected = auto_detect_project_type(scan_profile)
        if detected:
            print(f"  🤖 Auto-detected: {PROJECT_TYPES[detected]['label']}")
            confirm = input(f"  Đúng không? (Y/n): ").strip().lower()
            if confirm == "n":
                project_type = _ask_project_type()
            else:
                project_type = detected
        else:
            project_type = _ask_project_type()

    print(f"\n  ✅ Project Type: {PROJECT_TYPES[project_type]['label']}\n")

    # ─── GENERATE ───
    generator = ProjectGenerator(
        target_dir=target,
        project_name=name,
        project_type=project_type,
        scan_profile=scan_profile,
    )
    generator.generate()

    print(f"✅ Khởi tạo thành công! .agents/ tại: {agents_dir}")


def cmd_validate(args):
    """Validate cấu trúc .agents/ của project."""
    target = os.path.abspath(args.target or os.getcwd())
    agents_dir = os.path.join(target, ".agents")

    print(f"\n🔍 Validating .agents/ tại: {target}")
    print(f"{'─' * 50}\n")

    if not os.path.exists(agents_dir):
        print("❌ Không tìm thấy thư mục .agents/")
        print("💡 Chạy: wb-agent init để khởi tạo\n")
        return

    checks = [
        (".agents/", os.path.isdir(agents_dir)),
        (".agents/identity/master-identity.md", os.path.isfile(os.path.join(agents_dir, "identity", "master-identity.md"))),
        (".agents/memory/constitution.md", os.path.isfile(os.path.join(agents_dir, "memory", "constitution.md"))),
        (".agents/AGENTS.md", os.path.isfile(os.path.join(agents_dir, "AGENTS.md"))),
        (".agents/project.json", os.path.isfile(os.path.join(agents_dir, "project.json"))),
        (".agents/specs/", os.path.isdir(os.path.join(agents_dir, "specs"))),
        (".agents/skills/", os.path.isdir(os.path.join(agents_dir, "skills"))),
    ]

    all_passed = True
    for name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("✅ Tất cả kiểm tra đều PASSED!\n")
    else:
        print("❌ Một số file/thư mục thiếu. Chạy `wb-agent init` để tạo lại.\n")


def cmd_version(args):
    """Hiển thị version."""
    print(f"wb-agent v{__version__}")


def main():
    parser = argparse.ArgumentParser(
        prog="wb-agent",
        description="⚡ WB-Agent v2.0 — Thin Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  wb-agent init                              # Smart-detect project type
  wb-agent init --target /path/to/project    # Init tại thư mục chỉ định
  wb-agent init --name "My Project"          # Init với tên project
  wb-agent init --type fullstack             # Chỉ định project type
  wb-agent init --force                      # Ghi đè không hỏi
  wb-agent validate                          # Validate cấu trúc .agents/
  wb-agent version                           # Xem phiên bản

Loại dự án:
  web_public  — Blog, E-commerce, Landing Page (SEO)
  web_saas    — Dashboard, Admin, API Service
  fullstack   — Frontend + Backend API (SEO + DevOps)
  wordpress   — WordPress Theme/Plugin
  mobile_app       — iOS/Android
  script           — Python/Bash/JS scripts
  astro_cloudflare — Astro SSR on Cloudflare Pages
  astro_vps        — Astro SSR Node + SQLite on Docker VPS
        """,
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Lệnh cần thực thi")

    # init
    init_parser = subparsers.add_parser("init", help="Khởi tạo .agents/ cho project")
    init_parser.add_argument("--target", "-t", help="Thư mục đích")
    init_parser.add_argument("--name", "-n", help="Tên project")
    init_parser.add_argument(
        "--type",
        help=f"Loại dự án: {', '.join(PROJECT_TYPES.keys())}",
    )
    init_parser.add_argument(
        "--force", "-f", action="store_true", help="Ghi đè không hỏi"
    )

    # validate
    validate_parser = subparsers.add_parser("validate", help="Validate .agents/")
    validate_parser.add_argument("--target", "-t", help="Thư mục đích")

    # version
    subparsers.add_parser("version", help="Hiển thị phiên bản")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    commands = {
        "init": cmd_init,
        "validate": cmd_validate,
        "version": cmd_version,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
