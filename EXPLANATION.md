# What is a Harness? (Simple Explanation)

This explains the 5 core ideas behind an AI agent **harness**, using the
runnable example in [mini_harness.py](mini_harness.py).

---

## The big idea

A **model** (like Claude) does only ONE thing: it reads text and writes text.

- It cannot open files.
- It cannot run code.
- It cannot remember anything between calls.

The **harness** is the program wrapped *around* the model that gives it
hands, memory, and a heartbeat.

```
        ┌──────────────────────────────┐
        │           HARNESS            │
        │  loop · context · tools ·    │
        │      environment             │
        │   ┌──────────────────┐       │
        │   │      MODEL       │       │
        │   │ text in→text out │       │
        │   └──────────────────┘       │
        └──────────────────────────────┘
```

That's all "harness" means: the code that turns a text-in/text-out model
into something that can actually *do* tasks.

---

## The 5 pieces

### 1. The Loop
*(see `run()` in [mini_harness.py](mini_harness.py))*

The harness calls the model over and over:

```
model speaks → harness acts → model speaks again → ...
```

It keeps looping until either:
- the model says **"I'm done"** (a final answer), or
- a **safety limit** (`max_steps`) stops it so it can never run forever.

---

### 2. Context feed-in

The model has no memory. So **every** turn, the harness hands it the
*entire* conversation so far:

- the original task
- what the model said on each turn
- what the tools returned

That bundle of messages **is the model's whole world** for that turn.
Nothing outside the context exists to the model.

---

### 3. Context management

Context has a **size limit** — it cannot grow forever.

So when the conversation gets long, the harness **trims or summarizes**
old turns:
- keep the original task
- keep the most recent turns
- replace the middle with a short summary

This keeps the model from "overflowing" while preserving what matters.

---

### 4. Tools

Tools are **real functions** (e.g. `read_file`, `write_file`).

Important: the model **cannot run them itself**. It can only *ask* for one
by name. The harness then:
1. validates the request,
2. runs the function,
3. feeds the result back into the context.

This is the bridge between "just text" and "actually doing something."

---

### 5. Environment (and testing)

The **environment** is the world the tools act on.

- In the example: a fake dictionary of files.
- In real life: your actual folder, shell, database, or git repo.

**Testing** means: run the harness against the environment, then check
that it really changed.
In the example, an `assert` confirms the file actually got updated.

---

## How one turn flows

```
task ──▶ [feed context to model] ──▶ model: "run write_file"
                  ▲                              │
                  │                              ▼
        [add result to context] ◀── harness runs tool on environment
                  │
                  └──▶ loop again ──▶ model: "done" ──▶ exit
```

---

## Try it yourself

Run the example:

```bash
python3 mini_harness.py
```

Then experiment:
- Change the task to `"read notes.txt"` and re-run — the loop will pick
  the `read_file` tool instead of `write_file`.
- Lower `MAX_TURNS_KEPT` to see context management kick in sooner.
- Replace the `fake_model` function with a real Claude API call to let the
  actual model drive the same loop.

---

## One-line summary of each piece

| Piece | What it does | In the code |
|-------|--------------|-------------|
| **Loop** | Calls the model until it's done | `run()` |
| **Context feed-in** | Sends the whole history each turn | `context` list |
| **Context management** | Trims/summarizes when too long | `manage_context()` |
| **Tools** | Real actions the model can request | `TOOLS` |
| **Environment** | The world tools act on; what tests check | `ENVIRONMENT` |
