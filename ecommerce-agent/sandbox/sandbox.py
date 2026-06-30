"""Wrapper bao quanh tool: timeout + budget + error capture.
Tool nào gọi qua sandbox này mới được chạy trong production.
"""
import time
import signal
from contextlib import contextmanager


class BudgetExceeded(Exception):
    pass


@contextmanager
def time_limit(seconds: int):
    """Raise TimeoutError nếu chạy quá `seconds`."""
    def handler(signum, frame):
        raise TimeoutError(f"Tool vượt quá {seconds}s")
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class Sandbox:
    def __init__(self, max_calls: int = 20, max_seconds_per_call: int = 10):
        self.max_calls = max_calls                 # tổng số call cho 1 job
        self.max_sec = max_seconds_per_call        # timeout từng call
        self.call_count = 0

    def run(self, tool_fn, **kwargs) -> dict:
        """Chạy tool trong điều kiện kiểm soát. Trả về dict {ok, result, error, latency_ms}."""
        if self.call_count >= self.max_calls:
            raise BudgetExceeded(f"Đã dùng hết {self.max_calls} call")

        self.call_count += 1
        t0 = time.time()
        try:
            with time_limit(self.max_sec):
                result = tool_fn(**kwargs)
            return {"ok": True, "result": result, "error": None,
                    "latency_ms": int((time.time() - t0) * 1000)}
        except Exception as e:
            return {"ok": False, "result": None, "error": str(e),
                    "latency_ms": int((time.time() - t0) * 1000)}
