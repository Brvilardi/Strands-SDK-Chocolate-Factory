from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands.session import FileSessionManager

from agents.agents_as_tools import b2c_assistant, technical_questions_assistant

ORQUESTRATOR_SYSTEM_PROMPT = """
Você é o orquestrador da Fábrica de Chocolates Willy Wonka. Analise a intenção do usuário e indique qual ferramenta usar:

- Para vendas relacionadas a pessoa física -> use a tool b2c_assistant
- Para dúvidas técnicas sobre produtos (ingredientes, composição, análises sensoriais, processos) -> use a tool technical_questions

Responda apenas com a ferramenta indicada. Não crie respostas ou resolva problemas, apenas utilize as ferramentas providenciadas. Caso a mensagem do usuário não tenha informações suficientes, apenas de uma saudação e pergunte como pode ajudar
"""


app = BedrockAgentCoreApp()




@app.entrypoint
def invoke(payload):
    """Process user input and return a response"""
    session_id = payload.get("session_id", "default_session")
    user_message = payload.get("prompt", "Hello")
    orchestrator_agent = Agent(
        model="amazon.nova-micro-v1:0",
        system_prompt=ORQUESTRATOR_SYSTEM_PROMPT,
        callback_handler=None,
        tools=[b2c_assistant, technical_questions_assistant],
        session_manager=FileSessionManager(session_id=session_id)
    )
    result = orchestrator_agent(user_message)


    return {"result": str(result)}

if __name__ == "__main__":
    app.run()