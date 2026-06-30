# harness

A tiny, runnable illustration of **harness engineering** — the system built
around an AI model that determines what the model sees, how it acts, what it
remembers, and how it recovers from failure.

The model is the "reasoning engine." The **harness** is the machinery that
turns a text-in/text-out model into a reliable agent inside a real workflow.

## What's here

| File | What it is |
|------|------------|
| [mini_harness.py](mini_harness.py) | A ~130-line, no-API-key example you can run and read. |
| [EXPLANATION.md](EXPLANATION.md) | A beginner walkthrough of the example's 5 core pieces. |
| [doc/component.md](doc/component.md) | The full picture: the key primitives of a production harness. |

## Run it

```bash
python3 mini_harness.py
```

The example fakes the model with a simple rule-based function so the whole
machine runs offline. It drives a fake file system, asks for a tool, executes
it, and asserts that the environment actually changed.

## The mental model

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

The example covers the foundational pieces (loop, context feed-in, context
management, tools, environment). [doc/component.md](doc/component.md) extends
that foundation to the primitives a real harness adds — execution
environments, durable state and orchestration, sub-agents and skills, and
verification and observability.

Ultimately, harness engineering is a shift from relying on "model smartness"
to building **dependable systems** where failures become infrastructure for
future improvement.
