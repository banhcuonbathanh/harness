# orchestration.md — PRIMITIVE 7: ORCHESTRATION

> Quản lý vòng đời công việc: các bước, retry, cổng duyệt, bàn giao cho người.
> Đây là "đường ray" mà mỗi yêu cầu viết content đi qua.

## Pipeline chuẩn cho 1 post

```
[1] INTAKE      Nhận brief (loại post, máy/chủ đề, mục tiêu)
      │
[2] PLAN        Đọc content-calendar + check_duplicate. Nếu trùng → đổi góc.
      │
[3] RETRIEVE    Nạp context theo ma trận (context-management.md).
      │         → sub-agent Researcher tóm tắt data nếu cần.
[4] DRAFT       Sub-agent Copywriter viết theo skill write-fb-post.md.
      │
[5] REVIEW      Sub-agent Reviewer chấm theo verification.md.
      │         FAIL → quay lại [4] (tối đa 2 vòng), vẫn fail → gắn cờ người xử lý.
[6] GATE ⛔     APPROVAL GATE: người duyệt xem draft + các [[CẦN XÁC NHẬN]].
      │         Chưa duyệt → KHÔNG sang [7].
[7] SCHEDULE    schedule_post (nếu bật) hoặc bàn giao bản copy-paste.
      │
[8] LOG         Ghi post-log.md + cập nhật status trong content-calendar.md.
```

## Cổng duyệt (approval gates)

- **Bắt buộc trước khi đăng public.** Đăng lên trang công ty là hành động khó thu
  hồi → luôn cần người bấm duyệt.
- Mọi `[[CẦN XÁC NHẬN: ...]]` phải được người điền/xóa TRƯỚC khi đăng.

## Retry & lỗi

- Draft fail review: retry tối đa 2 lần rồi escalate cho người (kèm lý do fail).
- Thiếu data sản phẩm/KM: KHÔNG bịa — trả về câu hỏi cho người vận hành.

## Bàn giao cho người (human handoff)

Khi escalate, agent xuất: brief gốc + draft hiện tại + danh sách [[CẦN XÁC NHẬN]]
+ lý do dừng. Người bổ sung rồi feed lại pipeline từ bước phù hợp.

## Nhịp chạy (tùy chọn)
- Có thể lên lịch chạy hàng ngày (vd sáng tạo draft cho ngày hôm đó) — nhưng
  bước GATE vẫn là con người.
