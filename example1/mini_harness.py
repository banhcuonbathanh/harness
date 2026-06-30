"""
mini_harness.py — a tiny example of how an agent "harness" works.

A harness is the program that runs AROUND the model. The model only
outputs text. The harness does everything else:

  1. THE LOOP        -> keep calling the model until it says "done"
  2. CONTEXT FEED-IN -> build the messages we send to the model each turn
  3. CONTEXT MGMT    -> trim/summarize history so it never grows too big
  4. TOOLS           -> run real actions the model asks for
  5. ENVIRONMENT     -> the "world" the tools act on (here: a fake file system)

We fake the model with a simple rule-based function so you can run this
file with NO API key and watch the whole machine work.
"""

# ----------------------------------------------------------------------
# 5. ENVIRONMENT — the world the agent can touch.
#    In real life: your repo, a shell, a database. Here: a dict.
# ----------------------------------------------------------------------
ENVIRONMENT = {
    "files": {"notes.txt": "buy milk"},
}


# ----------------------------------------------------------------------
# 4. TOOLS — real functions. The model can ONLY ask for these by name;
#    the harness is what actually executes them against the environment.
# ----------------------------------------------------------------------
def tool_read_file(name):
    return ENVIRONMENT["files"].get(name, f"(no file named {name})")

def tool_write_file(name, text):
    ENVIRONMENT["files"][name] = text
    return f"wrote {len(text)} chars to {name}"

TOOLS = {
    "read_file": tool_read_file,
    "write_file": tool_write_file,
}


# ----------------------------------------------------------------------
# THE "MODEL" — normally a network call to Claude. We fake it so the
# example runs offline. It looks at the latest context and returns either
#   - a tool request:  ("tool", name, args)
#   - a final answer:  ("final", text)
# ----------------------------------------------------------------------
def fake_model(context):
    last = context[-1]["content"]

    # If we were just given a tool result, we're done.
    if last.startswith("TOOL_RESULT"):
        return ("final", "Done! I updated notes.txt based on what I read.")

    # Otherwise this is the user's task -> decide to use a tool first.
    if "read" in last.lower():
        return ("tool", "read_file", {"name": "notes.txt"})
    return ("tool", "write_file", {"name": "notes.txt", "text": "buy milk and eggs"})


# ----------------------------------------------------------------------
# 3. CONTEXT MANAGEMENT — context has a size limit. When history gets
#    too long, we compact old turns into a short summary so we never
#    overflow. (Real harnesses summarize with the model; we just trim.)
# ----------------------------------------------------------------------
MAX_TURNS_KEPT = 6

def manage_context(context):
    if len(context) <= MAX_TURNS_KEPT:
        return context
    head = context[0]                       # keep the original task
    summary = {"role": "system",
               "content": f"[summary of {len(context) - 2} earlier turns]"}
    tail = context[-(MAX_TURNS_KEPT - 2):]  # keep the most recent turns
    return [head, summary] + tail


# ----------------------------------------------------------------------
# 1. THE LOOP  +  2. CONTEXT FEED-IN
#    This is the heart of the harness.
# ----------------------------------------------------------------------
def run(task, max_steps=5):
    # 2. CONTEXT FEED-IN: we start the context with the user's task.
    context = [{"role": "user", "content": task}]

    for step in range(1, max_steps + 1):
        print(f"\n--- step {step} ---")

        # 3. Keep context within limits before every model call.
        context = manage_context(context)

        # 2. Feed the current context to the model.
        kind, *payload = fake_model(context)

        if kind == "final":
            answer = payload[0]
            context.append({"role": "assistant", "content": answer})
            print("MODEL (final):", answer)
            return answer  # 1. loop exits when the model is done

        # kind == "tool": model asked us to run a tool.
        name, args = payload
        print(f"MODEL wants tool: {name}({args})")
        context.append({"role": "assistant", "content": f"CALL {name} {args}"})

        # 4. Harness executes the tool against the ENVIRONMENT.
        result = TOOLS[name](**args)
        print(f"TOOL result: {result}")

        # 2. Feed the result back into context for the next turn.
        context.append({"role": "tool", "content": f"TOOL_RESULT: {result}"})

    return "(stopped: hit max_steps safety limit)"


# ----------------------------------------------------------------------
# ENVIRONMENT RUN / TESTING — drive the harness and check the result.
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("BEFORE:", ENVIRONMENT["files"])
    final = run("Please update notes.txt to add eggs")
    print("\nAFTER :", ENVIRONMENT["files"])

    # a tiny test: did the environment actually change?
    assert "eggs" in ENVIRONMENT["files"]["notes.txt"], "tool did not run!"
    print("TEST PASSED ✅")
