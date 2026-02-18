"""
Registry - Định nghĩa tất cả Skills và Workflows cho Spec-Kit Antigravity.
Đây là nguồn sự thật duy nhất (Single Source of Truth) cho metadata.
"""

# ============================================================================
# SKILLS REGISTRY
# ============================================================================
SKILLS_REGISTRY = [
    {
        "name": "speckit.devops",
        "role": "DevOps Architect",
        "description": "Chuyên gia hạ tầng Docker & Security Hardening theo dải port 8900-8999.",
    },
    {
        "name": "speckit.identity",
        "role": "Persona Architect",
        "description": "Quản lý nhân cách và định hướng hành vi của AI cho dự án.",
    },
    {
        "name": "speckit.analyze",
        "description": "Consistency Checker - Phân tích tính nhất quán giữa spec, plan, tasks",
        "version": "1.0.0",
        "depends_on": ["speckit.tasks"],
        "role": "Antigravity Consistency Analyst",
        "handoffs": [
            {"label": "Fix Issues", "agent": "speckit.implement", "prompt": "Fix the consistency issues found"},
        ],
    },
    {
        "name": "speckit.checker",
        "description": "Static Analysis Aggregator - Chạy static analysis trên codebase",
        "version": "1.0.0",
        "depends_on": ["speckit.implement"],
        "role": "Antigravity Static Analyst",
        "handoffs": [
            {"label": "Fix Issues", "agent": "speckit.implement", "prompt": "Fix static analysis issues"},
        ],
    },
    {
        "name": "speckit.checklist",
        "description": "Requirements Validator - Tạo và validate checklist từ spec",
        "version": "1.0.0",
        "depends_on": ["speckit.specify"],
        "role": "Antigravity Requirements Auditor",
        "handoffs": [],
    },
    {
        "name": "speckit.clarify",
        "description": "Ambiguity Resolver - Phát hiện và giải quyết mơ hồ trong spec",
        "version": "1.0.0",
        "depends_on": ["speckit.specify"],
        "role": "Antigravity Clarity Engineer",
        "handoffs": [
            {"label": "Update Spec", "agent": "speckit.specify", "prompt": "Update spec with clarifications"},
        ],
    },
    {
        "name": "speckit.constitution",
        "description": "Governance Manager - Thiết lập & quản lý Constitution (Source of Law)",
        "version": "1.0.0",
        "depends_on": [],
        "role": "Antigravity Governance Architect",
        "handoffs": [
            {"label": "Build Specification", "agent": "speckit.specify", "prompt": "Implement the feature specification based on the updated constitution"},
        ],
    },
    {
        "name": "speckit.diff",
        "description": "Artifact Comparator - So sánh sự khác biệt giữa các artifacts",
        "version": "1.0.0",
        "depends_on": [],
        "role": "Antigravity Diff Analyst",
        "handoffs": [],
    },
    {
        "name": "speckit.implement",
        "description": "Code Builder (Anti-Regression) - Triển khai code theo tasks với IRONCLAD protocols",
        "version": "1.0.0",
        "depends_on": ["speckit.tasks"],
        "role": "Antigravity Master Builder",
        "handoffs": [
            {"label": "Run Tests", "agent": "speckit.tester", "prompt": "Run tests for implemented code"},
            {"label": "Review Code", "agent": "speckit.reviewer", "prompt": "Review the implementation"},
        ],
    },
    {
        "name": "speckit.migrate",
        "description": "Legacy Code Migrator - Chuyển đổi legacy code sang chuẩn mới",
        "version": "1.0.0",
        "depends_on": [],
        "role": "Antigravity Migration Specialist",
        "handoffs": [
            {"label": "Create Spec", "agent": "speckit.specify", "prompt": "Create spec from migrated codebase"},
        ],
    },
    {
        "name": "speckit.plan",
        "description": "Technical Planner - Tạo plan.md từ spec (data model, API contracts, research)",
        "version": "1.0.0",
        "depends_on": ["speckit.specify"],
        "role": "Antigravity System Architect",
        "handoffs": [
            {"label": "Create Tasks", "agent": "speckit.tasks", "prompt": "Break the plan into tasks"},
            {"label": "Create Checklist", "agent": "speckit.checklist", "prompt": "Create a checklist"},
        ],
    },
    {
        "name": "speckit.quizme",
        "description": "Logic Challenger (Red Team) - Đặt câu hỏi phản biện, tìm edge cases",
        "version": "1.0.0",
        "depends_on": ["speckit.specify"],
        "role": "Antigravity Red Team Analyst",
        "handoffs": [],
    },
    {
        "name": "speckit.reviewer",
        "description": "Code Reviewer - Review code theo spec và best practices",
        "version": "1.0.0",
        "depends_on": ["speckit.implement"],
        "role": "Antigravity Code Reviewer",
        "handoffs": [
            {"label": "Fix Issues", "agent": "speckit.implement", "prompt": "Fix review issues"},
        ],
    },
    {
        "name": "speckit.specify",
        "description": "Feature Definer - Tạo spec.md từ mô tả ngôn ngữ tự nhiên",
        "version": "1.0.0",
        "depends_on": [],
        "role": "Antigravity Domain Scribe",
        "handoffs": [
            {"label": "Build Technical Plan", "agent": "speckit.plan", "prompt": "Create a plan for the spec"},
            {"label": "Clarify Requirements", "agent": "speckit.clarify", "prompt": "Clarify specification requirements"},
        ],
    },
    {
        "name": "speckit.status",
        "description": "Progress Dashboard - Hiển thị trạng thái tiến độ project",
        "version": "1.0.0",
        "depends_on": ["speckit.tasks"],
        "role": "Antigravity Progress Tracker",
        "handoffs": [],
    },
    {
        "name": "speckit.tasks",
        "description": "Task Breaker - Tạo tasks.md atomic, có thứ tự dependency từ plan",
        "version": "1.0.0",
        "depends_on": ["speckit.plan"],
        "role": "Antigravity Execution Strategist",
        "handoffs": [
            {"label": "Analyze Consistency", "agent": "speckit.analyze", "prompt": "Run consistency analysis"},
            {"label": "Implement", "agent": "speckit.implement", "prompt": "Start the implementation"},
        ],
    },
    {
        "name": "speckit.taskstoissues",
        "description": "Issue Tracker Syncer - Đồng bộ tasks.md sang issue tracker",
        "version": "1.0.0",
        "depends_on": ["speckit.tasks"],
        "role": "Antigravity Issue Syncer",
        "handoffs": [],
    },
    {
        "name": "speckit.tester",
        "description": "Test Runner & Coverage - Chạy tests và báo cáo coverage",
        "version": "1.0.0",
        "depends_on": ["speckit.implement"],
        "role": "Antigravity Test Engineer",
        "handoffs": [
            {"label": "Fix Failures", "agent": "speckit.implement", "prompt": "Fix test failures"},
        ],
    },
    {
        "name": "speckit.validate",
        "description": "Implementation Validator - Validate implementation vs spec tổng thể",
        "version": "1.0.0",
        "depends_on": ["speckit.implement"],
        "role": "Antigravity Validation Oracle",
        "handoffs": [],
    },
]


# ============================================================================
# WORKFLOWS REGISTRY
# ============================================================================
WORKFLOWS_REGISTRY = [
    {
        "command": "00-speckit.all",
        "description": "Full Pipeline (Specify → Clarify → Plan → Tasks → Analyze)",
        "skills": ["speckit.specify", "speckit.clarify", "speckit.plan", "speckit.tasks", "speckit.analyze"],
    },
    {
        "command": "01-speckit.constitution",
        "description": "Thiết lập/cập nhật Constitution (Source of Law)",
        "skills": ["speckit.constitution"],
    },
    {
        "command": "02-speckit.specify",
        "description": "Tạo Feature Specification (spec.md)",
        "skills": ["speckit.specify"],
    },
    {
        "command": "03-speckit.clarify",
        "description": "Giải quyết mơ hồ trong Specification",
        "skills": ["speckit.clarify"],
    },
    {
        "command": "04-speckit.plan",
        "description": "Tạo Technical Plan (plan.md)",
        "skills": ["speckit.plan"],
    },
    {
        "command": "05-speckit.tasks",
        "description": "Tạo Task Breakdown (tasks.md)",
        "skills": ["speckit.tasks"],
    },
    {
        "command": "06-speckit.analyze",
        "description": "Phân tích tính nhất quán giữa artifacts",
        "skills": ["speckit.analyze"],
    },
    {
        "command": "07-speckit.implement",
        "description": "Triển khai code theo tasks (Anti-Regression)",
        "skills": ["speckit.implement"],
    },
    {
        "command": "08-speckit.checker",
        "description": "Chạy Static Analysis",
        "skills": ["speckit.checker"],
    },
    {
        "command": "09-speckit.tester",
        "description": "Chạy Tests & Coverage",
        "skills": ["speckit.tester"],
    },
    {
        "command": "10-speckit.reviewer",
        "description": "Code Review",
        "skills": ["speckit.reviewer"],
    },
    {
        "command": "11-speckit.validate",
        "description": "Validate Implementation vs Spec",
        "skills": ["speckit.validate"],
    },
    {
        "command": "speckit.prepare",
        "description": "Prep Pipeline (Specify → Clarify → Plan → Tasks → Analyze)",
        "skills": ["speckit.specify", "speckit.clarify", "speckit.plan", "speckit.tasks", "speckit.analyze"],
    },
    {
        "command": "util-speckit.checklist",
        "description": "Tạo/validate Requirements Checklist",
        "skills": ["speckit.checklist"],
    },
    {
        "command": "util-speckit.diff",
        "description": "So sánh Artifacts (Spec vs Implementation)",
        "skills": ["speckit.diff"],
    },
    {
        "command": "util-speckit.migrate",
        "description": "Migrate Legacy Code",
        "skills": ["speckit.migrate"],
    },
    {
        "command": "util-speckit.quizme",
        "description": "Red Team - Đặt câu hỏi phản biện tìm edge cases",
        "skills": ["speckit.quizme"],
    },
    {
        "command": "util-speckit.status",
        "description": "Hiển thị Progress Dashboard",
        "skills": ["speckit.status"],
    },
    {
        "command": "util-speckit.taskstoissues",
        "description": "Sync tasks.md → Issue Tracker",
        "skills": ["speckit.taskstoissues"],
    },
]
