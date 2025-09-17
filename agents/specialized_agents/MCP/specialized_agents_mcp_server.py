import json

import boto3
from mcp.server import FastMCP

# Create an MCP server
mcp = FastMCP("Specialized Agents Server")

@mcp.tool(description="Lista todos os produtos disponíveis")
def list_products() -> str:
    return "Lista de produtos: Chocolate Amargo Wonka Mistério Profundo, Chocolate ao Leite Wonka Delícia Encantada, Chocolate Branco Wonka Nuvem Encantada, Jujuba Wonka Arco-Íris Elástico"


# Define a tool
@mcp.tool(description="Processa e responde a dúvidas técnicas relacionadas aos produtos da fábrica do Willy Wonka")
def technical_questions(query: str, session_id: str = "default_session_1111111111111111111") -> str:
    try:
        client = boto3.client('bedrock-agentcore', region_name='us-east-1')

        payload = json.dumps({
            "prompt": query,
            "session_id": session_id
        })

        print("Payload: ", payload)

        response = client.invoke_agent_runtime(
            agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:954976331552:runtime/technical_questions_agent-8E6zMp2f2f',
            runtimeSessionId=session_id,  # Must be 33+ chars
            payload=payload,
            qualifier="DEFAULT"  # Optional
        )
        print("Full response: ", response)
        response_body = response['response'].read()
        response_data = json.loads(response_body)
        print("Agent Response:", response_data)
        return str(response_data['result'])
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"


# Define a tool
@mcp.tool(description="Processa e responde a consultas relacionadas a vendas a pessoas físicas (B2C).")
def b2c_assistant(query: str, session_id: str = "default_session_1111111111111111111") -> str:
    try:
        client = boto3.client('bedrock-agentcore', region_name='us-east-1')

        payload = json.dumps({
            "prompt": query,
            "session_id": session_id
        })

        print("Payload: ", payload)

        response = client.invoke_agent_runtime(
            agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:954976331552:runtime/b2c_agent-b0sJMG86aM',
            runtimeSessionId=session_id,  # Must be 33+ chars
            payload=payload,
            qualifier="DEFAULT"  # Optional
        )
        print("Full response: ", response)
        response_body = response['response'].read()
        response_data = json.loads(response_body)
        print("Agent Response:", response_data)
        return str(response_data['result'])
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"

mcp.run(transport="streamable-http")