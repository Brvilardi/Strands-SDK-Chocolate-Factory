import json

import boto3
from strands import Agent, tool
from strands_tools import retrieve, http_request




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
        client = boto3.client('bedrock-agentcore', region_name='us-west-2')
        payload = json.dumps({
            "input": {"prompt": "Explain machine learning in simple terms"}
        })

        response = client.invoke_agent_runtime(
            agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:954976331552:runtime/technical_questions_agent-8E6zMp2f2f',
            runtimeSessionId='dfmeoagmreaklgmrkleafremoigrmtesogmtrskhmtkrlshmt',  # Must be 33+ chars
            payload=payload,
            # qualifier="DEFAULT"  # Optional
        )
        response_body = response['response'].read()
        response_data = json.loads(response_body)
        print("Agent Response:", response_data)
        return str(b2c_agent(query))
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def technical_questions_assistant(query: str, session_id: str = "default_session") -> str:
    """
    Processa e responde a questões técnicas sobre produtos e serviços.

    Args:
    query: Query contendo questões técnicas sobre especificações, funcionalidades e características de produtos
    session_id: ID da sessão para manter

    Returns:
        Uma resposta detalhada sobre aspectos técnicos dos produtos ou serviços consultados
    """
    print("Tool 'technical_questions_assistant' was called")
    try:
        tech_agent = create_technical_questions_agent(session_id)
        return str(tech_agent(query))
    except Exception as e:
        return f"Error: {str(e)}"
