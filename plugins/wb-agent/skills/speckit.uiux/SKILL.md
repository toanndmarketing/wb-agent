---
name: speckit.uiux
description: UI/UX review: accessibility, responsive, design system compliance
---

## 🎯 Mission
Thiết lập và quản lý tiêu chuẩn UI/UX "Pro Max" cho dự án, đảm bảo giao diện premium, chuyên nghiệp và nhất quán.

## 📥 Input
- `.agent/specs/[feature]/spec.md` (chứa User Scenarios)
- `.agent/memory/constitution.md` (tech stack constraints)
- Brand guidelines (logo, màu sắc từ developer)

## 📋 Protocol

### Phase 1: Brand Identity & Colors
- Định nghĩa bảng màu (Primary, Secondary, Accent, State Colors).
- Định nghĩa Typography (Font families, Font sizes cho Heading/Body).
- **Tránh màu generic** (red, blue, green nguyên bản). Dùng HSL hoặc palette bài bản.

### Phase 2: Spacing & Layout
- Định nghĩa Container max-width (7xl, 1280px, v.v.).
- Spacing system (Padding/Margin chuẩn: 4, 8, 16, 24, 32px).
- Responsive Grid system cho Mobile/Tablet/Desktop.

### Phase 3: Core Components Design
- **Buttons**: Các trạng thái default, hover, active, disabled.
- **Cards**: Shadow, border-radius, hover transitions.
- **Forms**: Input styles, error states, focus rings.
- **Badges/Tags**: Trạng thái Sale, Hot, New, v.v.

### Phase 4: Rich Aesthetics Directive
- Sử dụng Glassmorphism, Vibrancy, Gradients nếu phù hợp.
- Định nghĩa Micro-animations (framer-motion, CSS transitions).

## 📤 Output
- File: `.agent/knowledge_base/ui_ux_standards.md`
- File: `.agent/specs/[feature]/ui-specs.md` (cho từng tính năng)

## 🚫 Guard Rails
- KHÔNG sử dụng màu mặc định của trình duyệt.
- KHÔNG thiết kế quá phức tạp gây chậm performance.
- PHẢI ưu tiên Mobile-first design.