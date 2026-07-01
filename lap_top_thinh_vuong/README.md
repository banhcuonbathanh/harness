# Harness viết Content Facebook — Laptop Thịnh Vượng (laptoptv.vn)

Harness biến model từ "máy sinh chữ" thành hệ thống agentic đáng tin để sản xuất
nội dung Facebook cho Laptop Thịnh Vượng. Xây theo **10 primitives** của harness
engineering — mỗi primitive là một file/thư mục cụ thể.

## Bản đồ 10 primitives → file

| # | Primitive | File / thư mục | Vai trò |
|---|-----------|----------------|---------|
| 1 | Instruction | `agents.md` | Identity, brand voice, hard constraints |
| 2 | Context Delivery | `context/` | company, products, promotions, audience |
| 3 | Context Management | `context-management.md` | Ma trận nạp context, chống nhiễu/trùng |
| 4 | Tool Interface | `tools/tools.md` | get_product, save_draft, schedule_post... |
| 5 | Execution Environment | `execution.md` | Ranh giới ghi file, bí mật, cổng đăng bài |
| 6 | Durable State | `state/` | content-calendar, post-log, drafts/ |
| 7 | Orchestration | `orchestration.md` | Pipeline, retry, approval gate, handoff |
| 8 | Sub-agents | `agents/` | researcher, copywriter, reviewer |
| 9 | Skills | `skills/write-fb-post.md` | Playbook viết 1 post |
| 10 | Verification | `verification.md` | Checklist + receipts trước khi đăng |

## Luồng chạy (tóm tắt)

```
Brief → PLAN (chống trùng) → RETRIEVE (Researcher) → DRAFT (Copywriter)
      → REVIEW (Reviewer + verification.md) → ⛔ APPROVAL GATE (người)
      → SCHEDULE/bàn giao → LOG
```

## Cách dùng nhanh

1. **Nạp dữ liệu thật** vào `context/products.md` và `context/promotions.md`
   (thay data mẫu; xóa/điền các `[[CẦN XÁC NHẬN]]`).
2. Ra brief, ví dụ:
   > "Viết post bán Dell Latitude 5420 cho nhóm nhân viên văn phòng."
3. Agent chạy pipeline trong `orchestration.md`, xuất **draft** vào `state/drafts/`.
4. Người duyệt điền nốt `[[CẦN XÁC NHẬN]]`, đối chiếu `verification.md`, rồi đăng.

## Nguyên tắc an toàn cốt lõi

- **Không bịa** giá / cấu hình / KM / review — chỉ dùng `context/`.
- **Agent không tự đăng public** — luôn qua approval gate (đăng là hành động khó thu hồi).
- **Bí mật** (token FB/Zalo) không nằm trong repo.

## Nguồn dữ liệu công ty
Trích từ https://laptoptv.vn (ngày 2026-07-01). Khi web đổi → cập nhật `context/`.
```
71 Thiên Hiền, Mỹ Đình 1, Nam Từ Liêm, Hà Nội · Hotline 0928.939.666
```
