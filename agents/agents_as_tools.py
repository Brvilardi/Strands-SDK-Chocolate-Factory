from strands import Agent, tool
from strands_tools import retrieve, http_request

from agents.specialized_agents.b2c_agent import create_b2c_agent


@tool
def b2c_assistant(query: str, session_id: str = "default_session") -> str:
    """
    Processa e responde a consultas relacionadas a vendas a pessoas físicas (B2C).

    Args:
    query: Query para o assistente B2C que pode incluir dúvidas sobre produtos, preços, disponibilidade, formas de pagamento e outras questões relacionadas a vendas para consumidores finais
    session_id: ID da sessão para manter contexto entre interações

    Returns:
        Uma resposta detalhada sobre vendas B2C, que pode incluir solicitação de informações adicionais do cliente ou confirmação de dados fornecidos
    """
    print("Tool 'b2c_assistant' was called")
    try:
        b2c_agent = create_b2c_agent(session_id)
        return str(b2c_agent(query))
    except Exception as e:
        return f"Error: {str(e)}"