"""Entry point: gắn 8 primitive lại để chạy 1 job."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from context.context_manager import ContextManager
from tools.tools import TOOLS
from sandbox.sandbox import Sandbox
from state.durable_state import DurableState
from skills.seo_writer import SeoWriter
from skills.validator import Validator
from orchestrator.orchestrator import Orchestrator
from observability.logger import TraceLogger


def run_job(product: dict) -> dict:
    job_id = f"job_{product['id']}"

    # [1] Instruction — đọc từ file (sẽ truyền vào LLM khi gọi)
    instruction = Path("instructions/agent.md").read_text(encoding="utf-8")

    # [2] Context manager (rerank + compaction)
    ctx_mgr = ContextManager()

    # [3] Tools đã import sẵn ở TOOLS dict
    # [4] Sandbox bao quanh tool
    sandbox = Sandbox(max_calls=20, max_seconds_per_call=10)

    # [5] Durable state — sẽ tự load nếu job đã chạy dở
    state = DurableState(job_id)

    # [7] Sub-agents
    skills = {"seo_writer": SeoWriter(), "validator": Validator()}

    # [8] Observability
    logger = TraceLogger(trace_id=job_id)
    logger.log("START", product_id=product["id"], resume_from=state.current_step())

    # [6] Orchestrator điều phối tất cả
    orch = Orchestrator(state, sandbox, TOOLS, skills, logger)
    result = orch.run(product)

    logger.log("END", status=result.get("status"))
    print("\n=== SUMMARY ===")
    print(logger.summary())
    return result


if __name__ == "__main__":
    product = {
        "id": "P001",
        "name": "Tai nghe Bluetooth X1",
        "category": "Tai nghe Bluetooth",
        "specs": "Pin 20h, chống nước IPX5, ANC",
    }
    result = run_job(product)
    print("\n=== RESULT ===")
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
