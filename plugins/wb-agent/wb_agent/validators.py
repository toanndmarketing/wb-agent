"""
Validators v2.0 — Kiểm tra cấu trúc .agents/ theo chuẩn Thin Agent.
"""

import os


def validate_agent_structure(agents_dir: str) -> list:
    """Validate cấu trúc .agents/ v2.0."""
    results = []

    # 1. Core directory
    results.append(_check_exists(agents_dir, ".agents/", is_dir=True))

    # 2. Identity
    results.append(_check_exists(
        os.path.join(agents_dir, "identity", "master-identity.md"),
        "identity/master-identity.md",
    ))

    # 3. Constitution
    results.append(_check_exists(
        os.path.join(agents_dir, "memory", "constitution.md"),
        "memory/constitution.md",
    ))

    # 4. AGENTS.md (project-scoped rules)
    results.append(_check_exists(
        os.path.join(agents_dir, "AGENTS.md"),
        "AGENTS.md",
    ))

    # 5. project.json
    results.append(_check_exists(
        os.path.join(agents_dir, "project.json"),
        "project.json",
    ))

    # 6. specs directory
    results.append(_check_exists(
        os.path.join(agents_dir, "specs"),
        "specs/",
        is_dir=True,
    ))

    # 7. skills directory
    results.append(_check_exists(
        os.path.join(agents_dir, "skills"),
        "skills/",
        is_dir=True,
    ))

    # 8. Content quality check: master-identity.md > 100 bytes
    identity_path = os.path.join(agents_dir, "identity", "master-identity.md")
    if os.path.isfile(identity_path):
        size = os.path.getsize(identity_path)
        results.append({
            "name": "master-identity.md content quality",
            "passed": size > 100,
            "details": [] if size > 100 else [f"File quá nhỏ ({size} bytes). Cần điền thông tin dự án."],
        })

    return results


def _check_exists(path: str, name: str, is_dir: bool = False) -> dict:
    """Check file/dir tồn tại."""
    if is_dir:
        exists = os.path.isdir(path)
    else:
        exists = os.path.isfile(path)

    return {
        "name": name,
        "passed": exists,
        "details": [] if exists else [f"Không tìm thấy: {name}"],
    }
