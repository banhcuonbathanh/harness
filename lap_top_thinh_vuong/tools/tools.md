# tools/tools.md — PRIMITIVE 4: TOOL INTERFACE

> Cho agent "hành động" chứ không chỉ "nói". Mỗi tool có: name, description,
> input schema, output. Đây là hợp đồng — agent gọi đúng schema, harness thực thi.
>
> Tùy môi trường mà tool được nối vào MCP / function-calling / script. Ở mức tối
> thiểu, các tool này có thể là thao tác đọc-ghi file trong repo harness này.

## get_product
- **description:** Lấy 1 block sản phẩm từ context/products.md theo id hoặc tên.
- **input:** `{ "query": "DELL-5420-i5G11" }`
- **output:** block sản phẩm dạng markdown, hoặc `not_found`.

## list_active_promotions
- **description:** Trả về các KM đang chạy từ context/promotions.md.
- **input:** `{}`
- **output:** danh sách KM đang hiệu lực (bỏ mục "Đã kết thúc").

## check_duplicate
- **description:** Kiểm tra máy/góc content đã đăng gần đây chưa (đọc state/post-log.md).
- **input:** `{ "product_id": "...", "angle": "..." }`
- **output:** `{ "duplicate": true|false, "last_posted": "YYYY-MM-DD" }`

## save_draft
- **description:** Ghi 1 bản nháp post vào state/drafts/ và thêm dòng vào post-log.
- **input:** `{ "id": "...", "type": "ban_hang|km|tu_van|caption", "content": "..." }`
- **output:** đường dẫn file draft.

## schedule_post  (tùy chọn, cần môi trường có quyền)
- **description:** Đưa post vào lịch (Meta Business Suite / Buffer / n8n).
- **input:** `{ "draft_id": "...", "publish_at": "ISO-8601" }`
- **output:** `{ "scheduled": true, "provider_ref": "..." }`
- **note:** Yêu cầu approval gate (xem orchestration.md). Không tự đăng public.

## fetch_web  (tùy chọn)
- **description:** Lấy thông số sản phẩm từ trang hãng khi cần đối chiếu.
- **input:** `{ "url": "..." }`
- **note:** Chỉ để tham khảo cấu hình kỹ thuật, KHÔNG lấy giá để đưa vào post.

---

### Quy tắc dùng tool
- Cần dữ liệu sản phẩm/KM → **gọi tool, không nhớ từ đầu**.
- Trước khi `save_draft` phải `check_duplicate`.
- `schedule_post` chỉ chạy sau khi content PASS `verification.md` và được người duyệt.
