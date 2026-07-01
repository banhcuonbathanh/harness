# execution.md — PRIMITIVE 5: EXECUTION ENVIRONMENT

> Nơi tool thực sự chạy — biên giới an toàn của agent. Quản lý quyền, bí mật, mạng.

## Ranh giới

- **Vùng làm việc:** thư mục harness này (`lap top thinh vuong/`). Agent chỉ
  đọc/ghi trong đây (context/, state/, tools/).
- **Chỉ đọc:** `agents.md`, `context/*` (nội dung nguồn — sửa thủ công bởi người).
- **Được ghi:** `state/drafts/`, `state/post-log.md`, `state/content-calendar.md`.
- **Ngoài phạm vi:** không sửa file khác trong máy người dùng.

## Bí mật & quyền (KHÔNG bao giờ để lộ trong post/log)

- Token Facebook / Meta Graph API, khóa Zalo OA, mật khẩu → đặt ở biến môi
  trường / trình quản lý bí mật, KHÔNG commit vào repo.
- Agent không được in token ra output.

## Mạng

- Mặc định offline (chỉ thao tác file). `fetch_web` / `schedule_post` cần mạng →
  chỉ bật khi người vận hành cho phép.

## Cổng đăng bài (an toàn quan trọng nhất)

- Agent **KHÔNG tự đăng công khai**. Chỉ tạo draft.
- Việc đăng thật (public tới trang Facebook của công ty) là hành động khó thu hồi
  → luôn qua người duyệt (xem orchestration.md, approval gate).

## Môi trường triển khai gợi ý

- Thủ công: chạy trong Claude Code, draft ra file, người copy sang Facebook.
- Bán tự động: nối `schedule_post` với Meta Business Suite / Buffer / n8n qua MCP.
