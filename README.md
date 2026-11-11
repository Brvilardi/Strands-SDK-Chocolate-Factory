# Willy Wonka Chocolate Factory - Multi-Agent System

A multi-agent customer service system for a fictional Willy Wonka Chocolate Factory, built with [Strands Agents](https://github.com/strands-agents/strands-agents), AWS Bedrock AgentCore, and Model Context Protocol (MCP).

## Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────┐     ┌──────────────────────┐
│   Frontend   │────▶│   Orchestrator   │────▶│  MCP Server │────▶│  Specialized Agents  │
│ Streamlit/   │◀────│   Agent          │◀────│  :8000      │◀────│  (Bedrock AgentCore) │
│ HTML         │     └──────────────────┘     └─────────────┘     └──────────────────────┘
└──────────────┘           │                                        ├─ B2C Agent
                     Amazon Nova Micro                              └─ Technical Questions Agent
```

1. **Orchestrator Agent** — Analyzes user intent and routes queries to the appropriate specialized agent via MCP tools.
2. **B2C Agent** — Handles product sales: collects customer name, product choice, and quantity.
3. **Technical Questions Agent** — Answers technical product questions (ingredients, composition, manufacturing) using a Bedrock Knowledge Base.
4. **MCP Server** — Exposes specialized agents as tools via the Model Context Protocol.

## Products

| Product | Name |
|---------|------|
| Chocolate ao Leite | Wonka Delícia Encantada |
| Chocolate Amargo | Wonka Mistério Profundo |
| Chocolate Branco | Wonka Nuvem Encantada |
| Jujuba | Wonka Arco-Íris Elástico |

## Project Structure

```
├── agents/
│   ├── orchestrator_agent.py              # Main routing agent
│   ├── requirements.txt
│   └── specialized_agents/
│       ├── b2c_agent/                     # Sales agent
│       │   ├── b2c_agent.py
│       │   ├── Dockerfile
│       │   └── .bedrock_agentcore.yaml
│       ├── technical_questions_agent/     # Technical info agent
│       │   ├── technical_questions_agent.py
│       │   ├── Dockerfile
│       │   └── .bedrock_agentcore.yaml
│       └── MCP/
│           ├── specialized_agents_mcp_server.py  # MCP server
│           └── client_sandbox.py
├── frontend/
│   └── index.html                         # Vanilla JS chat UI
├── streamlit_app.py                       # Streamlit chat UI
└── requirements_streamlit.txt
```

## Prerequisites

- Python 3.13+
- AWS account with Bedrock access (region: `us-east-1`)
- AWS credentials configured (via environment or AWS CLI)
- Specialized agents deployed to Bedrock AgentCore

## Setup

### 1. Install dependencies

```bash
# Orchestrator agent
pip install -r agents/requirements.txt

# Streamlit frontend
pip install -r requirements_streamlit.txt
```

### 2. Deploy specialized agents

Each specialized agent has a Dockerfile and `.bedrock_agentcore.yaml` for deployment to AWS Bedrock AgentCore. See the respective directories under `agents/specialized_agents/`.

### 3. Configure environment

The technical questions agent requires a `.env` file with:

```
BEDROCK_KNOWLEDGE_BASE_ID=<your_knowledge_base_id>
```

### 4. Start the MCP server

```bash
python agents/specialized_agents/MCP/specialized_agents_mcp_server.py
```

The server starts on port `8000`.

### 5. Run the application

**Streamlit UI:**

```bash
streamlit run streamlit_app.py
```

**HTML UI:**

Open `frontend/index.html` in a browser. Expects the orchestrator API at `http://localhost:8080/invocations`.

## Tech Stack

- **[Strands Agents](https://github.com/strands-agents/strands-agents)** — Agent orchestration framework
- **AWS Bedrock AgentCore** — Cloud runtime for specialized agents
- **Amazon Nova Micro v1.0** — LLM powering all agents
- **Model Context Protocol (MCP)** — Tool exposure layer between orchestrator and specialized agents
- **Streamlit** — Web UI
- **boto3** — AWS SDK
- **Docker** — Containerization for agent deployment
