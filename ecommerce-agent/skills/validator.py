"""Sub-agent chuyên kiểm tra rule. KHÔNG gọi LLM — chỉ logic rule-based,
nhanh, deterministic, dễ test.
"""


class Validator:
    BANNED_WORDS = {"tốt nhất", "số 1", "rẻ nhất thị trường"}
    MIN_WORDS = 150
    MAX_WORDS = 300

    def check(self, draft: dict) -> None:
        """Raise ValueError nếu vi phạm. Đây chính là VERIFICATION primitive."""
        desc = draft.get("description", "")
        words = len(desc.split())

        if words < self.MIN_WORDS:
            raise ValueError(f"Mô tả quá ngắn: {words}<{self.MIN_WORDS} từ")
        if words > self.MAX_WORDS:
            raise ValueError(f"Mô tả quá dài: {words}>{self.MAX_WORDS} từ")

        for w in self.BANNED_WORDS:
            if w in desc.lower():
                raise ValueError(f"Có từ cấm: '{w}'")

        if not draft.get("keywords") or len(draft["keywords"]) < 3:
            raise ValueError("Cần tối thiểu 3 keyword")

        title_len = len(draft.get("title", ""))
        if not (40 <= title_len <= 80):
            raise ValueError(f"Tiêu đề {title_len} ký tự, cần 40–80")
