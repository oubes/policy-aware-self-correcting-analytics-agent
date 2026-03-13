# 🚀 Policy-Aware Self-Correcting Analytics Agent

**Policy-Aware Self-Correcting Analytics Agent** is a robust, production-ready AI agent that transforms natural language questions into executable **Pandas code**.  
It features a **self-correcting control loop**, a **security sandbox** to prevent malicious code execution, and a **policy enforcement layer** to ensure **data privacy and safe analytics**.

---

# 🖥️ User Interface

Below is a preview of the dashboard where users can interact with their data and monitor system performance.


---

# 🏗 System Architecture

The agent operates on a **state-based workflow** defined using **LangGraph**.  
It follows a **directed cyclic graph** to handle extraction, validation, execution, and automated retries.


---

# 1️⃣ Control Flow

| Node | Responsibility |
|-----|-----|
| `get_question` | Initializes the agent state and loads the dataset schema |
| `validate_code` | Scans generated code for forbidden syntax (imports, classes, etc.) |
| `extract_code` | Cleans LLM output, removing markdown fences and redundant imports |
| `run_code` | Executes the code in a restricted sandbox environment |
| `fix_code` | Sends error logs back to the LLM for automated debugging |

---

# 🔐 Security Policy

To maintain **data integrity and system safety**, the agent enforces strict **AST (Abstract Syntax Tree)** checks.

### Forbidden Nodes

- `Import`
- `With`
- `ClassDef`
- `FunctionDef`

### Forbidden Calls

- `open`
- `__import__`
- `eval`

### Data Access Policy

The agent **cannot return raw DataFrames**.  
Instead, it must return **aggregated results only**, such as:

- `sum`
- `mean`
- `count`
- `min`
- `max`

This prevents **data leakage** from the underlying dataset.

---

# 🛠 Key Features

### Autonomous Logic
Powered by **LangGraph** to enable complex decision-driven workflows.

### Security Sandbox
Uses **AST parsing** to block dangerous operations like filesystem access.

### Self-Healing Execution
If generated code fails, the agent automatically calls the **`fix_code` node** to repair and retry execution.

### Red-Team Ready
Includes an **evaluation suite** designed to test the system against **prompt injection attacks** and policy violations.

### Modern Web UI
A sleek **FastAPI-powered dashboard** allows users to interact with the analytics agent in real time.

---

## 📂 Project Structure

```bash
├── app
│   ├── agent          # LLM logic, prompts, and code cleaning
│   ├── api            # FastAPI routes and Pydantic schemas
│   ├── core           # Configuration and environment management
│   ├── execution      # Secure sandbox and code executor
│   ├── graph          # LangGraph nodes, edges, and state definitions
│   └── web            # Frontend (index.html)
├── data               # CSV datasets
├── evaluation         # Red-team test cases and metric calculators
└── main.py            # Application entry point
```

## 🚀 Getting Started
### 1. Prerequisites

Python 3.10+

OpenAI-compatible API Key (e.g., Qwen, GPT-4)

### 2. Installation
# Install dependencies
pip install fastapi uvicorn pandas numpy openai python-dotenv langgraph torch

# Setup environment variables
echo "DASHSCOPE_API_KEY=your_key_here" > .env
### 3. Running the Application
uvicorn main:app --reload

Navigate to http://localhost:8000
 to access the interactive dashboard.

## 📊 Evaluation & Red Teaming

The project includes an /evaluate endpoint that runs the agent against a suite of "Red Team" prompts designed to attempt breaking the system policies.
The system tracks Success Rate, Rejection Precision, and Repair Rate.
