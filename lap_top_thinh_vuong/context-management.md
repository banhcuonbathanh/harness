# context-management.md — PRIMITIVE 3: CONTEXT MANAGEMENT

> Cửa sổ context hữu hạn → chỉ nạp đúng phần cần cho từng post, tránh nhiễu.
> Đây là quy tắc RETRIEVAL: viết loại post nào thì kéo file nào.

## Ma trận nạp context theo loại post

| Loại post | Luôn nạp | Nạp thêm | KHÔNG cần nạp |
|-----------|----------|----------|----------------|
| Bán 1 sản phẩm | agents.md, company.md | products.md (chỉ block máy đó), audience (nhóm liên quan) | toàn bộ products.md, promotions cũ |
| Khuyến mãi | agents.md, company.md | promotions.md (mục đang chạy), 2–3 máy hot | products.md đầy đủ |
| Tư vấn/education | agents.md, company.md | audience.md, 3–5 máy ví dụ | promotions.md |
| Caption ảnh/video | agents.md | 1 block máy | mọi thứ khác |

## Nguyên tắc

1. **Chỉ kéo block sản phẩm cần dùng**, không nhét cả catalog vào prompt.
2. **Tóm tắt trước khi nạp:** nếu products.md dài, dùng sub-agent Researcher
   (xem `agents/researcher.md`) trả về bản tóm tắt 5 dòng thay vì nguyên file.
3. **Compaction:** với chiến dịch dài nhiều post, không giữ toàn bộ lịch sử —
   chỉ giữ `state/content-calendar.md` (kế hoạch) + 3 post gần nhất để tránh lặp.
4. **Chống trùng lặp:** trước khi viết, đọc `state/post-log.md` xem máy/góc đó đã
   đăng chưa để không viết lại y hệt.
5. **Nguồn sự thật > trí nhớ:** giá/KM luôn đọc lại từ context file tại thời điểm
   viết, không tin số nhớ từ post trước.
