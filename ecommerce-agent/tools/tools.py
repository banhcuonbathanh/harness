"""Các tool agent được phép gọi. Schema kiểu function-calling."""


def search_competitors(category: str, limit: int = 5) -> list[dict]:
    """Tìm sản phẩm cạnh tranh cùng danh mục.
    Args:
        category: Danh mục sản phẩm (vd 'Tai nghe Bluetooth')
        limit: Số lượng tối đa trả về
    """
    # Mock data — thực tế sẽ query Elasticsearch hoặc gọi API
    fake_db = [
        {"name": "Tai nghe X-Pro", "description": "Pin 30h, ANC, IPX5", "relevance": 0.92, "price_range": "1-2tr"},
        {"name": "Tai nghe Y-Lite", "description": "Pin 15h, gọn nhẹ", "relevance": 0.75, "price_range": "500-800k"},
        {"name": "Tai nghe Z-Sport", "description": "Chống nước, gym", "relevance": 0.68, "price_range": "800k-1tr"},
    ]
    return fake_db[:limit]


def check_duplicate(description: str) -> dict:
    """Kiểm tra mô tả có trùng với sản phẩm khác không (chống SEO penalty)."""
    # Thực tế: tính hash hoặc embedding similarity vs DB
    is_dup = "copy" in description.lower()  # mock
    return {"is_duplicate": is_dup, "similarity_score": 0.15}


def save_to_database(product_id: str, payload: dict) -> dict:
    """Lưu mô tả đã duyệt vào DB sản phẩm."""
    # Thực tế: INSERT INTO products...
    return {"saved": True, "product_id": product_id, "rows_affected": 1}


# TOOL REGISTRY — đây là "menu" duy nhất LLM nhìn thấy.
# Tool nào không có trong đây thì LLM KHÔNG được gọi.
TOOLS = {
    "search_competitors": search_competitors,
    "check_duplicate": check_duplicate,
    "save_to_database": save_to_database,
}
