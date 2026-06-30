"""State được persist ra file JSON. Sau crash, đọc file là biết đã làm tới đâu."""
import json
import os
from pathlib import Path


class DurableState:
    def __init__(self, job_id: str, base_dir: str = "states"):
        Path(base_dir).mkdir(exist_ok=True)
        self.path = Path(base_dir) / f"{job_id}.json"
        self.data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            return json.loads(self.path.read_text(encoding="utf-8"))
        return {"step": "init", "checkpoints": [], "draft": None, "attempts": {}}

    def checkpoint(self, step: str, payload: dict) -> None:
        """Đánh dấu hoàn thành 1 bước + lưu xuống disk NGAY (không buffer)."""
        self.data["step"] = step
        self.data["checkpoints"].append({"step": step, "payload": payload})
        self._flush()

    def set_draft(self, draft: dict) -> None:
        self.data["draft"] = draft
        self._flush()

    def get_draft(self) -> dict | None:
        return self.data.get("draft")

    def current_step(self) -> str:
        return self.data["step"]

    def _flush(self) -> None:
        # Ghi atomically — viết file tạm rồi rename, tránh hỏng file giữa chừng
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, self.path)
