#!/usr/bin/env python3
"""
⚡ WB-Agent - Spec-Driven Development CLI
Entry point cho console script `wb-agent`.

Cài đặt global:
    pip install antigravity-ssd
    wb-agent init --name "My Project"

Hoặc chạy trực tiếp:
    python -m antigravity_ssd init --name "My Project"
"""

import argparse
import sys
import os

from antigravity_ssd import __version__
from antigravity_ssd.generator import ProjectGenerator
from antigravity_ssd.validators import validate_agent_structure
from antigravity_ssd.registry import SKILLS_REGISTRY, WORKFLOWS_REGISTRY


def cmd_init(args):
    """Khởi tạo cấu trúc .agent/ cho project."""
    target = os.path.abspath(args.target or os.getcwd())
    name = args.name or os.path.basename(target)
    force = getattr(args, 'force', False)

    print(f"\n⚡ WB-Agent v{__version__} - Spec-Driven Development")
    print(f"{'─' * 50}")
    print(f"  📁 Target:  {target}")
    print(f"  📛 Project: {name}")
    print(f"{'─' * 50}\n")

    # Kiểm tra nếu .agent/ đã tồn tại
    agent_dir = os.path.join(target, ".agent")
    if os.path.exists(agent_dir) and not force:
        response = input("⚠️  Thư mục .agent/ đã tồn tại. Ghi đè? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Đã hủy.")
            return

    generator = ProjectGenerator(target_dir=target, project_name=name)
    generator.generate()

    print(f"\n✅ Khởi tạo thành công!")
    print(f"  📂 .agent/ đã được tạo tại: {agent_dir}")
    print(f"  🎯 Skills:    {len(SKILLS_REGISTRY)} skills")
    print(f"  🔄 Workflows: {len(WORKFLOWS_REGISTRY)} workflows")
    print(f"\n💡 Tiếp theo:")
    print(f"  1. Mở project trong Antigravity IDE")
    print(f"  2. Chạy /01-speckit.constitution để thiết lập Constitution")
    print(f"  3. Chạy /02-speckit.specify <mô tả feature> để bắt đầu\n")


def cmd_list_skills(args):
    """Liệt kê tất cả skills."""
    print(f"\n🧠 WB-Agent - Skills Registry ({len(SKILLS_REGISTRY)} skills)")
    print(f"{'─' * 70}")
    print(f"  {'Skill':<30} {'Description'}")
    print(f"  {'─' * 28}   {'─' * 38}")

    for skill in SKILLS_REGISTRY:
        print(f"  @{skill['name']:<28} {skill['description']}")

    print(f"\n💡 Sử dụng: @speckit.<name> trong Antigravity để gọi skill\n")


def cmd_list_workflows(args):
    """Liệt kê tất cả workflows."""
    print(f"\n🔄 WB-Agent - Workflows Registry ({len(WORKFLOWS_REGISTRY)} workflows)")
    print(f"{'─' * 70}")
    print(f"  {'Command':<35} {'Description'}")
    print(f"  {'─' * 33}   {'─' * 33}")

    for wf in WORKFLOWS_REGISTRY:
        print(f"  /{wf['command']:<33} {wf['description']}")

    print(f"\n💡 Sử dụng: /<command> trong Antigravity để chạy workflow\n")


def cmd_validate(args):
    """Validate cấu trúc .agent/ của project."""
    target = os.path.abspath(args.target or os.getcwd())
    agent_dir = os.path.join(target, ".agent")

    print(f"\n🔍 Validating .agent/ tại: {target}")
    print(f"{'─' * 50}\n")

    if not os.path.exists(agent_dir):
        print("❌ Không tìm thấy thư mục .agent/")
        print("💡 Chạy: wb-agent init để khởi tạo\n")
        return

    results = validate_agent_structure(agent_dir)

    all_passed = True
    for check in results:
        status = "✅" if check["passed"] else "❌"
        print(f"  {status} {check['name']}")
        if not check["passed"]:
            all_passed = False
            for detail in check.get("details", []):
                print(f"     ⚠️  {detail}")

    print()
    if all_passed:
        print("✅ Tất cả kiểm tra đều PASSED!\n")
    else:
        print("❌ Một số kiểm tra FAILED. Xem chi tiết ở trên.\n")


def cmd_version(args):
    """Hiển thị version."""
    print(f"wb-agent v{__version__}")


def main():
    parser = argparse.ArgumentParser(
        prog="wb-agent",
        description="⚡ WB-Agent - Spec-Driven Development CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  wb-agent init                              # Init tại thư mục hiện tại
  wb-agent init --target /path/to/project    # Init tại thư mục chỉ định
  wb-agent init --name "My Project"          # Init với tên project
  wb-agent init --force                      # Init và ghi đè không hỏi
  wb-agent list-skills                       # Xem danh sách skills
  wb-agent list-workflows                    # Xem danh sách workflows
  wb-agent validate                          # Validate cấu trúc .agent/
  wb-agent version                           # Xem phiên bản

Quy trình dự án MỚI:
  wb-agent init → /01-speckit.constitution → /02-speckit.specify → /04-speckit.plan → /05-speckit.tasks → /07-speckit.implement

Quy trình dự án CÓ SẴN:
  wb-agent init → /01-speckit.constitution → /util-speckit.migrate → /02-speckit.specify → /04-speckit.plan → /07-speckit.implement
        """
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Lệnh cần thực thi")

    # init
    init_parser = subparsers.add_parser("init", help="Khởi tạo cấu trúc .agent/ cho project")
    init_parser.add_argument("--target", "-t", help="Thư mục đích (mặc định: thư mục hiện tại)")
    init_parser.add_argument("--name", "-n", help="Tên project (mặc định: tên thư mục)")
    init_parser.add_argument("--force", "-f", action="store_true", help="Ghi đè .agent/ nếu đã tồn tại")

    # list-skills
    subparsers.add_parser("list-skills", help="Liệt kê tất cả skills")

    # list-workflows
    subparsers.add_parser("list-workflows", help="Liệt kê tất cả workflows")

    # validate
    validate_parser = subparsers.add_parser("validate", help="Validate cấu trúc .agent/")
    validate_parser.add_argument("--target", "-t", help="Thư mục đích (mặc định: thư mục hiện tại)")

    # version
    subparsers.add_parser("version", help="Hiển thị phiên bản")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    commands = {
        "init": cmd_init,
        "list-skills": cmd_list_skills,
        "list-workflows": cmd_list_workflows,
        "validate": cmd_validate,
        "version": cmd_version,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
