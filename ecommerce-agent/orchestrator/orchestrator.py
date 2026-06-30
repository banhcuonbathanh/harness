"""Vòng đời job: research -> draft -> validate -> save.
Có retry tối đa 3 lần. Fail liên tục -> yêu cầu human approval.
"""


class Orchestrator:
    def __init__(self, state, sandbox, tools, skills, logger, max_retries: int = 3):
        self.state = state
        self.sandbox = sandbox
        self.tools = tools
        self.skills = skills
        self.logger = logger
        self.max_retries = max_retries

    def run(self, product: dict) -> dict:
        # Mỗi bước = (tên, hàm xử lý). Resume sẽ skip các bước đã xong.
        steps = [
            ("research", self._research),
            ("draft",    self._draft),
            ("validate", self._validate),
            ("save",     self._save),
        ]
        done_steps = {cp["step"] for cp in self.state.data["checkpoints"]}

        for name, fn in steps:
            if name in done_steps:
                self.logger.log(f"skip:{name} (đã xong từ run trước)")
                continue

            # Retry loop
            for attempt in range(1, self.max_retries + 1):
                self.logger.log(f"step:{name} attempt:{attempt}")
                try:
                    result = fn(product)
                    self.state.checkpoint(name, result)
                    break
                except Exception as e:
                    self.logger.log(f"FAIL step:{name} attempt:{attempt} err:{e}")
                    if attempt == self.max_retries:
                        return self._human_gate(name, str(e))
        return {"status": "done", "draft": self.state.get_draft()}

    # --- Các bước cụ thể ---
    def _research(self, product):
        call = self.sandbox.run(self.tools["search_competitors"],
                                category=product["category"], limit=5)
        if not call["ok"]:
            raise RuntimeError(call["error"])
        return call["result"]

    def _draft(self, product):
        # Lấy kết quả research từ checkpoint trước
        competitors = self.state.data["checkpoints"][-1]["payload"]
        draft = self.skills["seo_writer"].write(product, competitors)
        self.state.set_draft(draft)
        return {"draft_words": len(draft["description"].split())}

    def _validate(self, _product):
        draft = self.state.get_draft()
        self.skills["validator"].check(draft)            # raise nếu fail
        dup = self.sandbox.run(self.tools["check_duplicate"],
                               description=draft["description"])
        if dup["result"]["is_duplicate"]:
            raise ValueError("Mô tả trùng với sản phẩm có sẵn")
        return {"validated": True}

    def _save(self, product):
        call = self.sandbox.run(self.tools["save_to_database"],
                                product_id=product["id"],
                                payload=self.state.get_draft())
        return call["result"]

    def _human_gate(self, step, err):
        self.logger.log(f"HUMAN_GATE step:{step} err:{err}")
        return {"status": "needs_human", "stuck_at": step, "error": err}
