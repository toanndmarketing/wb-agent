"""
Registry v2.0 — Project Types & Auto-Detection Logic.
Skills/Workflows đã được chuyển sang Global Plugin (speckit).
Registry giờ chỉ chịu trách nhiệm: Phân loại dự án + Auto-detect.
"""


# ============================================================================
# PROJECT TYPES (Simplified)
# ============================================================================
PROJECT_TYPES = {
    "web_public": {
        "label": "Web Public (B2C)",
        "description": "Blog, E-commerce, Landing Page — Cần SEO",
        "needs_seo": True,
        "needs_docker": True,
    },
    "web_saas": {
        "label": "Web SaaS (B2B)",
        "description": "Dashboard, Admin Panel, API Service",
        "needs_seo": False,
        "needs_docker": True,
    },
    "fullstack": {
        "label": "Full-stack (Web + API)",
        "description": "Frontend Public + Backend API — Cần SEO + DevOps",
        "needs_seo": True,
        "needs_docker": True,
    },
    "wordpress": {
        "label": "WordPress",
        "description": "WordPress Theme/Plugin Development",
        "needs_seo": True,
        "needs_docker": False,
    },
    "mobile_app": {
        "label": "Mobile App",
        "description": "iOS/Android — Không cần SEO",
        "needs_seo": False,
        "needs_docker": False,
    },
    "script": {
        "label": "Script / Automation",
        "description": "Python/Bash/JS scripts — Không Docker",
        "needs_seo": False,
        "needs_docker": False,
    },
}


def get_project_type_info(project_type: str) -> dict:
    """Lấy metadata của project type."""
    return PROJECT_TYPES.get(project_type, PROJECT_TYPES["fullstack"])


def auto_detect_project_type(scan_profile: dict) -> str | None:
    """
    Tự động xác định project type từ kết quả scan.
    Trả về None nếu không tự tin đủ → CLI sẽ hỏi user.
    """
    if not scan_profile or not scan_profile.get("has_existing_code"):
        return None

    tech = scan_profile.get("tech_stack", [])
    framework = scan_profile.get("framework")
    has_docker = scan_profile.get("docker", {}).get("has_compose", False)
    has_prisma = scan_profile.get("database", {}).get("has_prisma", False)
    pages = scan_profile.get("pages", [])
    api_routes = scan_profile.get("api", {}).get("routes", [])
    language = scan_profile.get("language")

    # WordPress detection
    if _has_file_pattern(scan_profile, ["wp-content", "functions.php", "style.css"]):
        return "wordpress"

    # Next.js + API + Prisma = fullstack
    if framework == "Next.js" and (has_prisma or api_routes) and has_docker:
        return "fullstack"

    # Next.js + pages (public facing) = web_public
    if framework == "Next.js" and pages and not api_routes:
        return "web_public"

    # NestJS / Express API only = web_saas
    if framework in ("NestJS", "Express.js", "FastAPI", "Django"):
        return "web_saas"

    # Pure React (no SSR pages) = web_saas
    if framework == "React" and not pages:
        return "web_saas"

    # Python without web framework = script
    if language == "Python" and framework is None:
        return "script"

    return None


def _has_file_pattern(scan_profile: dict, patterns: list) -> bool:
    """Check if source structure contains any of the patterns."""
    structure = scan_profile.get("source_structure", [])
    structure_str = " ".join(structure).lower()
    return any(p.lower() in structure_str for p in patterns)
