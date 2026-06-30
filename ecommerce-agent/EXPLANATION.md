# Ecommerce Agent — Giải thích dự án

Một **AI agent demo** tự động viết mô tả SEO cho sản phẩm trên sàn thương mại điện tử tiếng Việt. Dự án không nhằm chạy production mà để **minh họa 8 "primitive" (khối nền tảng) tạo nên một agent đáng tin cậy**: hướng dẫn, context, tool, sandbox, state bền vững, orchestrator, sub-agent, và observability.

Hiện tại các bước gọi LLM được **mock** để chạy được offline — bạn thay phần mock bằng lệnh gọi Anthropic API thật là dùng được.

---

## Agent làm gì (flow tổng quát)

Với mỗi sản phẩm, agent chạy 4 bước tuần tự, có checkpoint và retry:

```
research  →  draft  →  validate  →  save
(tìm đối   (viết mô   (kiểm rule   (lưu vào
 thủ)       tả SEO)    + chống      DB)
                       trùng)
```

- **research** — tìm sản phẩm cạnh tranh cùng danh mục.
- **draft** — sub-agent `SeoWriter` viết tiêu đề + mô tả + keyword.
- **validate** — sub-agent `Validator` kiểm tra rule cứng (độ dài, từ cấm, số keyword), rồi kiểm tra mô tả không trùng.
- **save** — lưu kết quả đã duyệt vào "database".

Nếu một bước fail 3 lần liên tiếp → agent dừng và trả về `needs_human` (human gate) thay vì cố sai tiếp.

---

## 8 primitive & file tương ứng

| # | Primitive | File | Vai trò |
|---|-----------|------|---------|
| 1 | **Instruction** | [instructions/agent.md](instructions/agent.md) | "Hiến pháp" của agent: vai trò, phong cách, rule cứng, format output. Đọc từ file để chỉnh không cần sửa code. |
| 2 | **Context Manager** | [context/context_manager.py](context/context_manager.py) | Chọn lọc context đưa vào prompt: **rerank** (giữ top N đối thủ liên quan nhất) + **compaction** (cắt mô tả dài). Tránh nhồi nhét token. |
| 3 | **Tools** | [tools/tools.py](tools/tools.py) | "Menu" hành động duy nhất agent được phép gọi: `search_competitors`, `check_duplicate`, `save_to_database`. Tool ngoài menu → không gọi được. |
| 4 | **Sandbox** | [sandbox/sandbox.py](sandbox/sandbox.py) | Bao quanh mỗi tool call: **timeout** (SIGALRM) + **budget** (giới hạn số call/job) + bắt lỗi. Trả về `{ok, result, error, latency_ms}`. |
| 5 | **Durable State** | [state/durable_state.py](state/durable_state.py) | Lưu tiến độ ra file JSON sau mỗi bước (ghi atomic: viết `.tmp` rồi `os.replace`). Crash giữa chừng → chạy lại sẽ **resume** đúng chỗ. |
| 6 | **Orchestrator** | [orchestrator/orchestrator.py](orchestrator/orchestrator.py) | Bộ não điều phối vòng đời job: chạy 4 bước, skip bước đã checkpoint, retry tối đa 3 lần, fail thì mở **human gate**. |
| 7 | **Sub-agents (Skills)** | [skills/seo_writer.py](skills/seo_writer.py), [skills/validator.py](skills/validator.py) | Agent con chuyên trách: `SeoWriter` (viết — thực tế gọi LLM), `Validator` (kiểm rule — thuần logic, deterministic, dễ test). |
| 8 | **Observability** | [observability/logger.py](observability/logger.py) | `TraceLogger` ghi mọi event ra console + file JSONL (`traces/<job_id>.jsonl`), kèm `summary()` tổng kết số event / thời gian / lỗi. |

Điểm gắn kết tất cả: [main.py](main.py) — `run_job()` khởi tạo 8 primitive rồi giao cho Orchestrator chạy.

---

## Sơ đồ kiến trúc

### 1. Bức tranh tổng thể — ai gọi ai

`main.py` lắp ráp 8 primitive, rồi **Orchestrator** đứng giữa điều phối mọi thứ. Mũi tên là chiều phụ thuộc/gọi.

```
┌──────────────────────────────────────────────────────────────────────┐
│                              main.py                                   │
│                run_job(product): khởi tạo & lắp ráp                     │
└───────────────┬──────────────────────────────────────────────────────┘
                │ tạo & tiêm (dependency injection)
                ▼
        ┌───────────────────────────────────────────────┐
        │              Orchestrator  [6]                 │
        │   vòng đời job: research→draft→validate→save   │
        │   + retry(3) + skip-checkpoint + human-gate    │
        └──┬─────────┬──────────┬──────────┬─────────┬───┘
           │         │          │          │         │
   đọc rule │   ghi/đọc │   gọi qua │   gọi   │   ghi log
           │  tiến độ │  sandbox │  skill  │
           ▼         ▼          ▼          ▼         ▼
   ┌────────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐
   │Instruction │ │Durable │ │Sandbox │ │ Skills │ │TraceLogger │
   │  agent.md  │ │ State  │ │  [4]   │ │  [7]   │ │    [8]     │
   │    [1]     │ │  [5]   │ │timeout │ │ ┌────┐ │ │ console +  │
   └────────────┘ │states/ │ │+budget │ │ │SEO │ │ │ traces/    │
                  │ *.json │ └───┬────┘ │ │Writer│ │ │ *.jsonl   │
                  └────────┘     │      │ └────┘ │ └────────────┘
                                 │ bọc  │ ┌────┐ │
                                 ▼      │ │Vali│ │
                            ┌─────────┐ │ │dator│ │
                            │ Tools[3]│ │ └────┘ │
                            │search_  │ └────────┘
                            │competi- │
                            │tors /   │   ┌──────────────────┐
                            │check_dup│   │ ContextManager[2]│
                            │/save_db │   │ rerank+compaction │
                            └─────────┘   └──────────────────┘
```

> `ContextManager [2]` là primitive sẵn sàng dùng để tinh gọn context đối thủ trước khi đưa vào prompt LLM thật; trong bản mock hiện tại `SeoWriter` chưa nối vào nó.

### 2. Luồng chạy một job (sequence)

Thứ tự gọi thực tế khi `python main.py` chạy thành công:

```
main        Orchestrator      Sandbox        Tools          Skills        State        Logger
 │  run()        │                │             │              │             │            │
 ├──────────────►│                │             │              │             │            │
 │               │ research ──────┼────────────►│search_compet.│             │            │
 │               │◄───────────────┼─────────────┤ [đối thủ]    │             │            │
 │               │ checkpoint("research") ───────────────────────────────────►│ flush JSON │
 │               │                │             │              │             │            │
 │               │ draft ─────────┼─────────────┼─────────────►│SeoWriter    │            │
 │               │◄───────────────┼─────────────┼──────────────┤ [draft]     │            │
 │               │ set_draft() + checkpoint("draft") ──────────────────────►│ flush JSON │
 │               │                │             │              │             │            │
 │               │ validate ──────┼─────────────┼─────────────►│Validator    │            │
 │               │  (raise nếu vi phạm rule)     │              │ check()     │            │
 │               │ check_duplicate┼────────────►│check_duplicate│             │            │
 │               │ checkpoint("validate") ────────────────────────────────►│ flush JSON │
 │               │                │             │              │             │            │
 │               │ save ──────────┼────────────►│save_to_db    │             │            │
 │               │ checkpoint("save") ────────────────────────────────────►│ flush JSON │
 │◄──────────────┤ {status:"done", draft}        │              │             │            │
 │               │                │             │              │  mọi step → log() ───────►│
```

### 3. Cơ chế retry, resume & human-gate

Logic vòng lặp trong `Orchestrator.run()` — điểm tạo nên độ tin cậy:

```
        ┌─────────────────────────────┐
        │ Với mỗi step trong 4 step:  │
        └──────────────┬──────────────┘
                       ▼
            ┌──────────────────────┐      có
            │ step đã có checkpoint?├───────────► skip (resume sau crash)
            └──────────┬───────────┘
                       │ chưa
                       ▼
            ┌──────────────────────┐
        ┌──►│ chạy fn(product)     │
        │   └──────────┬───────────┘
        │              ▼
        │        ┌───────────┐  ok    ┌────────────────────┐
        │        │ kết quả?  ├───────►│ checkpoint() + next│
        │        └─────┬─────┘        └────────────────────┘
        │              │ raise lỗi
        │              ▼
        │     ┌─────────────────┐  attempt < 3
        └─────┤ tăng attempt    │
              └────────┬────────┘
                       │ attempt == 3 (hết retry)
                       ▼
              ┌─────────────────────────────────┐
              │ _human_gate() →                 │
              │ {status:"needs_human",          │
              │  stuck_at, error}               │
              └─────────────────────────────────┘
```

**Đọc sơ đồ:** mỗi bước được thử tối đa 3 lần; thành công thì **checkpoint xuống disk ngay** (nên lần chạy sau sẽ *skip*); thất bại hết 3 lần thì mở **human-gate** thay vì làm bừa.

---

## Các ý tưởng thiết kế đáng chú ý

- **Defense in depth (phòng thủ nhiều lớp).** Từ cấm theo Luật quảng cáo VN được chặn ở *3 nơi*: instruction (dặn LLM), `SeoWriter` (tự lọc khi viết), và `Validator` (chặn cứng khi duyệt).
- **Resume sau crash.** `Orchestrator.run()` đọc các checkpoint đã có trong state và bỏ qua bước đã xong → không làm lại việc đã xong, không tốn tiền gọi LLM lần hai.
- **Verification tách khỏi generation.** `Validator` không gọi LLM, chỉ là rule thuần → nhanh, ổn định, kiểm thử được. Đây là "verification primitive".
- **Mọi tool đi qua sandbox.** Orchestrator không gọi thẳng hàm tool mà luôn qua `sandbox.run(...)`, nên timeout/budget/lỗi được kiểm soát đồng nhất.
- **Human-in-the-loop.** Hết retry không tự ý "nhắm mắt làm liều" mà trả `needs_human` — kèm `stuck_at` và `error` để người xử lý biết kẹt ở đâu.

---

## Cách chạy

```bash
cd ecommerce-agent
python main.py
```

Chạy xong sẽ tạo:
- `states/job_P001.json` — state bền vững của job (xóa file này để chạy lại từ đầu).
- `traces/job_P001.jsonl` — trace log từng event.

Sản phẩm demo (`P001 — Tai nghe Bluetooth X1`) được hard-code ở cuối [main.py](main.py); đổi dict `product` để thử sản phẩm khác.

> **Lưu ý môi trường:** sandbox dùng `signal.SIGALRM`, chỉ chạy trên Unix/macOS (không hỗ trợ Windows native) và phải ở main thread.

---

## Từ demo → production

| Thành phần | Hiện tại (mock) | Production |
|------------|-----------------|------------|
| `SeoWriter.write` | trả chuỗi ghép sẵn | gọi Anthropic API với prompt = instruction + context |
| `search_competitors` | fake_db tĩnh | query Elasticsearch / API thật |
| `check_duplicate` | check chuỗi `"copy"` | so khớp embedding similarity với DB |
| `save_to_database` | trả dict giả | `INSERT INTO products ...` thật |
