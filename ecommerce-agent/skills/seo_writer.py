"""Sub-agent chuyên viết. Trong thực tế: gọi LLM với prompt riêng.
Ở demo này mock kết quả để chạy được offline.
"""


class SeoWriter:
    BANNED_WORDS = {"tốt nhất", "số 1", "rẻ nhất thị trường"}

    def write(self, product: dict, competitors: list[dict]) -> dict:
        # Trong thực tế: gọi anthropic API với prompt = instruction + context
        # Ở đây mock để demo flow
        comp_names = ", ".join(c["name"] for c in competitors[:2])
        desc = (
            f"{product['name']} là lựa chọn đáng cân nhắc trong phân khúc "
            f"{product['category']}. So với {comp_names}, sản phẩm này nổi bật "
            f"với {product.get('specs', 'thông số ổn định')}. Phù hợp cho người "
            f"dùng cần thiết bị bền bỉ, hoạt động tốt trong nhiều điều kiện. "
            f"Trải nghiệm dễ chịu, thiết lập đơn giản, hỗ trợ kết nối nhanh. "
            f"Một giải pháp cân bằng giữa giá và chất lượng cho người dùng phổ thông."
        ) * 2  # nhân đôi cho đủ ~150 từ

        # Tự kiểm từ cấm ngay tại sub-agent (defense in depth)
        for w in self.BANNED_WORDS:
            if w in desc.lower():
                desc = desc.replace(w, "")

        return {
            "title": f"{product['name']} - Chính hãng",
            "description": desc,
            "keywords": [product["name"], product["category"], "chính hãng"],
        }
