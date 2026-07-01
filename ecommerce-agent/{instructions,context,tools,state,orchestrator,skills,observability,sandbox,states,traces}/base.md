In the context of harness engineering, data flows through a series of "primitives" that transform an AI model from a simple text generator into a dependable agentic system. Below is the progression of these 10 primitives as described in the sources:

### 1. **Instruction**
The first layer defines the agent's identity, tone, and constraints. This primitive includes **system prompts**, **repository rules**, or files like `agents.md`, which provide repeated guidance to the model so the user doesn't have to.

### 2. **Context Delivery**
This primitive provides the model with the specific materials it needs to work, such as **source files, failing tests, or stack traces**. Without this, a model is forced to guess, leading to hallucinations.

### 3. **Context Management**
Because a model has a finite context window, this layer decides what data is relevant at any given moment. It uses techniques like **RAG (Retrieval-Augmented Generation)**, **summarization**, and **compaction** to protect the model's attention from becoming "noisier" with irrelevant data.

### 4. **Tool Interface**
Tools allow the agent to **act** rather than just talk. This primitive involves structured protocols (like **MCP** or function calling) where a tool has a name, description, and schema, allowing the model to request specific actions.

### 5. **Execution Environment**
This is the bounded reality where tools actually run, such as a **sandbox, container, or browser session**. The harness uses this primitive to manage security, secrets, and network access, ensuring the model's actions are isolated and controlled.

### 6. **Durable State**
Acting as a "workbench," durable state preserves progress—such as **plan files, checkpoints, and task logs**—outside of the model's immediate context window. This ensures that if a system crashes or pauses, the agent can resume from where it left off rather than starting from scratch.

### 7. **Orchestration**
This primitive manages the **lifecycle of the work**. It handles the "busy work" of the workflow, such as retries, approval gates, heartbeats, and human handoffs, directing how the work moves from one step to the next.

### 8. **Sub-agents**
When a task is too complex for one stream of attention, the harness delegates work to **specialized sub-agents**. These sub-agents have narrower jobs and contexts (e.g., one reviews code while another researches), preventing the main agent's context from becoming crowded.

### 9. **Skills and Procedures**
Skills are **reusable playbooks or checklists** for recurring tasks, such as how to review a pull request or perform a browser check. They encode repeated expertise into named capabilities that the harness can invoke, making the agent's work more repeatable.

### 10. **Verification**
The final primitive in this sequence requires the agent to provide **receipts or evidence** that the work was successful. Instead of trusting a model's confident claim that it is "done," the harness demands verification through **passing tests, builds, or visual screenshots**.