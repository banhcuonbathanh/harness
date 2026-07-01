# verification.md — PRIMITIVE 10: VERIFICATION

> "Bằng chứng, không phải lời hứa." Content chỉ được coi là DONE khi qua checklist
> này. Reviewer chấm mục này. Không có [[CẦN XÁC NHẬN]] còn sót = điều kiện đăng.

## Checklist bắt buộc (tất cả phải ✅)

### A. Sự thật (chống bịa)
- [ ] Mọi cấu hình đối chiếu đúng với `context/products.md`.
- [ ] Mọi giá/% giảm đối chiếu đúng `context/products.md` + `context/promotions.md`.
- [ ] KM nhắc tới đang nằm trong mục "Đang chạy" của promotions.md.
- [ ] Không còn `[[CẦN XÁC NHẬN: ...]]` nào (hoặc đã được người điền).
- [ ] Không có review/đánh giá khách bịa, không có "bán chạy nhất" vô căn cứ.

### B. Thương hiệu & liên hệ
- [ ] Đúng brand voice (thân thiện, trung thực) theo `agents.md`.
- [ ] SĐT/địa chỉ/email khớp `context/company.md` (nguyên văn).
- [ ] Tình trạng máy (New / Likenew 99%) ghi rõ, không gây hiểu nhầm.

### C. Cấu trúc & định dạng
- [ ] Có hook mở bài.
- [ ] Có CTA rõ ràng.
- [ ] Có hashtag `#LaptopThinhVuong #laptoptv` + 1–4 hashtag liên quan.
- [ ] Độ dài đúng loại post (bán hàng 80–150 từ; caption 20–40 từ).
- [ ] Emoji 3–6, không spam.

### D. Chính sách & rủi ro
- [ ] Tuân thủ chính sách quảng cáo Facebook (không click-bait/hứa hẹn phi thực tế).
- [ ] Không hạ thấp đối thủ đích danh.
- [ ] Không trùng lặp với post gần đây (đã `check_duplicate`).

## "Receipts" cần đính kèm khi bàn giao
1. Draft cuối cùng.
2. Kết quả Reviewer: **PASS**.
3. Nguồn số liệu: id sản phẩm + mục KM đã dùng (để người duyệt truy vết).
4. Ảnh/video kèm (nếu là post có media) — hoặc ghi chú "cần thiết kế media".

> Nếu bất kỳ ô nào chưa ✅ → trạng thái = FAIL, quay lại pipeline (orchestration.md).
