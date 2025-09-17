from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient

streamable_http_mcp_client = MCPClient(lambda: streamablehttp_client("http://localhost:8000/mcp"))

# ESCAPED_AGENT_ARN="arn%3Aaws%3Abedrock-agentcore%3Aus-east-1%3A954976331552%3Aruntime%2Fspecialized_agents_mcp_server-2UI3cEFr0j"
# streamable_http_mcp_client = MCPClient(lambda: streamablehttp_client(f"https://bedrock-agentcore.us-east-1.amazonaws.com/runtimes/${ESCAPED_AGENT_ARN}/invocations?qualifier=DEFAULT"))


ORQUESTRATOR_SYSTEM_PROMPT = """
Você é o orquestrador da Fábrica de Chocolates Willy Wonka. Analise a intenção do usuário e indique qual ferramenta usar:

- Para assuntos relacionados a vendas -> use a tool b2c_assistant
- Para dúvidas técnicas sobre produtos (ingredientes, composição, análises sensoriais, processos) -> use a tool technical_questions

Responda apenas com a ferramenta indicada. Não crie respostas ou resolva problemas, apenas utilize as ferramentas providenciadas. Caso a mensagem do usuário não tenha informações suficientes, apenas de uma saudação e pergunte como pode ajudar
"""


# Create an agent with MCP tools
with streamable_http_mcp_client:
    # Get the tools from the MCP server
    tools = streamable_http_mcp_client.list_tools_sync()

    # Create an agent with these tools
    agent = Agent(model="amazon.nova-micro-v1:0",
                  tools=tools,
                  system_prompt=ORQUESTRATOR_SYSTEM_PROMPT)

    resp = agent("Eu gostaria de comprar um chocolate")