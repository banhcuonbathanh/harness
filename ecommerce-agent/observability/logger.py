"""Structured logger. Mọi event ghi ra cả console và file JSON trace."""
import json
import time
from pathlib import Path


class TraceLogger:
    def __init__(self, trace_id: str, out_dir: str = "traces"):
        Path(out_dir).mkdir(exist_ok=True)
        self.trace_id = trace_id
        self.path = Path(out_dir) / f"{trace_id}.jsonl"
        self.events: list[dict] = []

    def log(self, message: str, **meta) -> None:
        event = {
            "ts": round(time.time(), 3),
            "trace_id": self.trace_id,
            "msg": message,
            **meta,
        }
        self.events.append(event)
        # In ra console cho dev xem realtime
        meta_str = " ".join(f"{k}={v}" for k, v in meta.items())
        print(f"[{self.trace_id}] {message} {meta_str}")
        # Append vào file (JSONL = 1 dòng = 1 event, dễ parse)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def summary(self) -> dict:
        """Tổng kết trace: số event, thời gian, lỗi."""
        if not self.events:
            return {}
        total_ms = int((self.events[-1]["ts"] - self.events[0]["ts"]) * 1000)
        errors = [e for e in self.events if "FAIL" in e["msg"] or "err" in e]
        return {
            "trace_id": self.trace_id,
            "events": len(self.events),
            "total_ms": total_ms,
            "errors": len(errors),
            "trace_file": str(self.path),
        }
