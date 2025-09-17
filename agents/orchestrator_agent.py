from bedrock_agentcore.runtime import BedrockAgentCoreApp
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.session import FileSessionManager
from strands.tools.mcp import MCPClient
import logging

logging.basicConfig(level=logging.ERROR)


ORQUESTRATOR_SYSTEM_PROMPT = """
Você é o orquestrador da Fábrica de Chocolates Willy Wonka. Analise a intenção do usuário e indique qual ferramenta usar:

- Para vendas relacionadas a pessoa física -> use a tool b2c_assistant
- Para dúvidas técnicas sobre produtos (ingredientes, composição, análises sensoriais, processos) -> use a tool technical_questions
    - se necessário, execute mais de uma vez essa tool. Exemplo: se o cliente quiser saber algo de todos os produtos, chame essa tool individualmente para cada produto. 

Caso o cliente queira saber sobre produtos, consulte a tool b2c_assistant para ver quais produtos estão disponíveis


Não crie respostas ou resolva problemas, apenas utilize as ferramentas providenciadas. Caso a mensagem do usuário não tenha informações suficientes, apenas de uma saudação e pergunte como pode ajudar
"""


app = BedrockAgentCoreApp()




@app.entrypoint
def invoke(payload):
    """Process user input and return a response"""
    try:
        print(f"Payload recebido: {payload}")
        session_id = payload.get("session_id", "default_session_1111111111111111111")
        user_message = payload.get("prompt", "Hello")
        print(f"Session ID extraído: {session_id}")

        streamable_http_mcp_client = MCPClient(lambda: streamablehttp_client("http://localhost:8000/mcp"))
        with streamable_http_mcp_client:
            # Get the tools from the MCP server
            tools = streamable_http_mcp_client.list_tools_sync()

            print(f"Tools carregadas: {tools}")


            print(f"Mensagem recebida: {user_message}")
            # Criar ferramentas customizadas que incluem o session_id
            custom_tools = []
            for tool in tools:
                if hasattr(tool, 'name'):
                    # Criar wrapper que inclui session_id automaticamente
                    def create_tool_wrapper(original_tool, sid):
                        def wrapper_func(**kwargs):
                            # Adicionar session_id aos argumentos
                            kwargs['session_id'] = sid
                            return streamable_http_mcp_client.call_tool_sync(
                                tool_use_id=f"tool-{sid}",
                                name=original_tool.name,
                                arguments=kwargs
                            )
                        
                        # Copiar metadados da ferramenta original
                        wrapper_func.__name__ = original_tool.name
                        wrapper_func.__doc__ = getattr(original_tool, 'description', '')
                        return wrapper_func
                    
                    custom_tools.append(create_tool_wrapper(tool, session_id))
                else:
                    custom_tools.append(tool)
            
            orchestrator_agent = Agent(
                model="amazon.nova-micro-v1:0",
                system_prompt=ORQUESTRATOR_SYSTEM_PROMPT,
                callback_handler=None,
                tools=custom_tools,
                session_manager=FileSessionManager(session_id=session_id)
            )
            
            print(f"Session ID configurado: {session_id}")
            # Passar session_id no contexto da mensagem
            context_message = f"[SESSION_ID: {session_id}] {user_message}"
            result = orchestrator_agent(context_message)
            print(f"Resultado da agent: {result} \n\nMétricas de Tool: {result.metrics.tool_metrics} \n\nMétricas de usage: {result.metrics.accumulated_usage} \n\nState: {result.state}")
            # Limpar o prefixo do session_id da resposta se presente
            if isinstance(result, str) and result.startswith(f"[SESSION_ID: {session_id}]"):
                result = result.replace(f"[SESSION_ID: {session_id}] ", "")
    except  Exception as e:
        print(f"Erro ao processar a mensagem: {e}")
        result = f"Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente mais tarde.\n{e}"



    return {"result": str(result)}

if __name__ == "__main__":
    app.run()