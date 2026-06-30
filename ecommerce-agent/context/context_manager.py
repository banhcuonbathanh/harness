"""Quản lý context đưa vào LLM — KHÔNG nhồi nhét, có chọn lọc."""


class ContextManager:
    def __init__(self, max_competitors: int = 3, max_chars_per_item: int = 200):
        self.max_competitors = max_competitors      # rerank: chỉ giữ top N
        self.max_chars = max_chars_per_item          # compaction: cắt độ dài

    def build(self, product: dict, competitors: list[dict]) -> dict:
        """Trả về context tinh gọn để đưa vào prompt."""
        # 1. RERANK: sắp xếp competitor theo độ liên quan
        ranked = sorted(competitors, key=lambda c: c.get("relevance", 0), reverse=True)
        top = ranked[: self.max_competitors]

        # 2. COMPACTION: chỉ giữ thông tin cần thiết, cắt mô tả dài
        compact = [
            {
                "name": c["name"],
                "key_features": c["description"][: self.max_chars],
                "price_range": c.get("price_range", "N/A"),
            }
            for c in top
        ]

        return {
            "product": product,
            "competitors_summary": compact,
            "competitor_count_dropped": len(competitors) - len(top),
        }
