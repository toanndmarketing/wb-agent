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

from wb_agent import __version__
from wb_agent.generator import ProjectGenerator
from wb_agent.validators import validate_agent_structure
from wb_agent.registry import SKILLS_REGISTRY, WORKFLOWS_REGISTRY


def cmd_init(args):
    """Khởi tạo cấu trúc .agent/ cho project."""
    target = os.path.abspath(args.target or os.getcwd())
    name = args.name or os.path.basename(target)
    force = getattr(args, 'force', False)
    agent_dir = os.path.join(target, ".agent")

    print(f"\n⚡ WB-Agent v{__version__} - Spec-Driven Development")
    print(f"{'─' * 50}")
    print(f"  📁 Target:  {target}")
    print(f"  📛 Project: {name}")
    print(f"{'─' * 50}\n")

    # MIGRATION AUDIT LOGIC
    if os.path.exists(agent_dir) and not force:
        print("🔍 Đang quét cấu trúc .agent/ hiện có...")
        audit_report = _audit_existing_agent(agent_dir)
        
        if audit_report["is_legacy"]:
            print("\n⚠️  PHÁT HIỆN CẤU TRÚC CŨ (LEGACY AGENT)\n")
            print(f"  {'File/Folder':<25} {'Trạng thái':<15} {'Hướng xử lý'}")
            print(f"  {'─' * 23}   {'─' * 13}   {'─' * 18}")
            
            for item in audit_report["items"]:
                print(f"  {item['name']:<25} {item['status']:<15} {item['action']}")
            
            print("\n💡 Đề xuất tối ưu:")
            print("  - Nâng cấp core skills & workflows lên bản v1.0.0 (chuẩn ASF 3.3)")
            print("  - Thiết lập tầng Identity & Knowledge Base để 'gắn não' AI")
            print("  - Di chuyển hiến pháp cũ vào memory/constitution.md")
            
            response = input("\n🚀 Nâng cấp & Tối ưu hóa lên ASF 3.3 ngay? (y/N): ").strip().lower()
            if response != 'y':
                print("❌ Đã hủy.")
                return
        else:
            print("✅ Cấu trúc hiện tại đã đúng chuẩn ASF 3.3.")
            response = input("♻️  Bạn vẫn muốn cài đặt lại (Re-init)? (y/N): ").strip().lower()
            if response != 'y':
                print("❌ Đã hủy.")
                return

    generator = ProjectGenerator(target_dir=target, project_name=name)
    generator.generate()

    print(f"\n✅ Khởi tạo/Nâng cấp thành công!")
    print(f"  📂 .agent/ đã được tối ưu tại: {agent_dir}")
    print(f"  🎯 Skills:    {len(SKILLS_REGISTRY)} skills (ASF 3.3 Standard)")
    print(f"  🔄 Workflows: {len(WORKFLOWS_REGISTRY)} workflows")
    print(f"\n💡 Bước tiếp theo:")
    print(f"  1. Kiểm tra '.agent/identity/master-identity.md' để AI nhận diện dự án")
    print(f"  2. Chạy /01-speckit.constitution để cập nhật Tech Stack & Docker Ports")
    print(f"  3. Chạy @speckit.devops để tạo Docker environment chuẩn Security\n")


def _audit_existing_agent(agent_dir):
    """Quét và so sánh cấu trúc hiện có."""
    report = {"is_legacy": False, "items": []}
    
    # 1. Kiểm tra các thư mục mới (Chuẩn ASF 3.3)
    standard_dirs = ["identity", "knowledge_base", "memory", "scripts/bash"]
    for d in standard_dirs:
        path = os.path.join(agent_dir, d)
        if not os.path.exists(path):
            report["is_legacy"] = True
            report["items"].append({"name": d, "status": "THIẾU", "action": "Khởi tạo mới"})
        else:
            report["items"].append({"name": d, "status": "OK", "action": "Giữ lại"})

    # 2. Kiểm tra files lẻ/thừa không thuộc chuẩn mới
    # (Ví dụ: các file rules.md, sdd.md cũ thường nằm ở root .agent/)
    for item in os.listdir(agent_dir):
        if item in [".", "..", "skills", "workflows", "templates", "scripts", "identity", "knowledge_base", "memory", "README.md"]:
            continue
        report["is_legacy"] = True
        report["items"].append({"name": item, "status": "NON-STANDARD", "action": "Backup & Di chuyển"})

    # 3. Skills/Workflows luôn cần update core
    report["is_legacy"] = True
    report["items"].append({"name": "skills/", "status": "CẦN UPDATE", "action": "Nâng cấp Core"})
    report["items"].append({"name": "workflows/", "status": "CẦN UPDATE", "action": "Nâng cấp Core"})

    return report


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
