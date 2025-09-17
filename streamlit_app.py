import streamlit as st
import sys
import os
import uuid
import time

# Adicionar o diretório agents ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# Importar o orchestrator agent
from agents.orchestrator_agent import invoke

def generate_session_id():
    """Gera um ID de sessão único com pelo menos 33 caracteres"""
    timestamp = str(int(time.time() * 1000))
    unique_id = str(uuid.uuid4()).replace('-', '')
    return f"session_{timestamp}_{unique_id}"

# Configuração da páginas
st.set_page_config(
    page_title="Fábrica de Chocolates Willy Wonka",
    page_icon="🍫",
    layout="wide"
)

# Título da aplicação
st.title("🍫 Fábrica de Chocolates Willy Wonka")
st.markdown("Chat com o orquestrador da fábrica")

# Inicializar sessões se não existir
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "active_session" not in st.session_state:
    st.session_state.active_session = None

# Sidebar para gerenciar sessões
st.sidebar.header("Gerenciar Sessões")

# Botão para criar nova sessão
if st.sidebar.button("➕ Nova Sessão"):
    new_session_id = generate_session_id()
    st.session_state.sessions[new_session_id] = []
    st.session_state.active_session = new_session_id
    st.rerun()

# Dropdown para selecionar sessão ativa
if st.session_state.sessions:
    session_options = list(st.session_state.sessions.keys())
    current_index = 0
    if st.session_state.active_session in session_options:
        current_index = session_options.index(st.session_state.active_session)
    
    selected_session = st.sidebar.selectbox(
        "Sessão Ativa",
        session_options,
        index=current_index,
        format_func=lambda x: f"Sessão {x.split('_')[1][-8:]}"
    )
    st.session_state.active_session = selected_session
else:
    # Criar primeira sessão automaticamente
    first_session_id = generate_session_id()
    st.session_state.sessions[first_session_id] = []
    st.session_state.active_session = first_session_id

# Botão para deletar sessão atual
if len(st.session_state.sessions) > 1 and st.sidebar.button("🗑️ Deletar Sessão Atual"):
    if st.session_state.active_session in st.session_state.sessions:
        del st.session_state.sessions[st.session_state.active_session]
        st.session_state.active_session = list(st.session_state.sessions.keys())[0]
        st.rerun()

# Mostrar ID da sessão atual
if st.session_state.active_session:
    st.sidebar.text_area(
        "Session ID Atual",
        value=st.session_state.active_session,
        height=100,
        disabled=True
    )

# Área principal
st.header("Chat com o Orquestrador")

# Obter mensagens da sessão ativa
current_messages = st.session_state.sessions.get(st.session_state.active_session, [])

# Exibir histórico de mensagens da sessão ativa
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adicionar mensagem do usuário ao histórico da sessão ativa
    st.session_state.sessions[st.session_state.active_session].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Invocar o orchestrator agent diretamente
    try:
        with st.chat_message("assistant"):
            with st.spinner("Processando..."):
                payload = {
                    "session_id": st.session_state.active_session,
                    "prompt": prompt
                }
                
                result = invoke(payload)
                assistant_response = result.get("result", "Resposta não encontrada")
                
                st.markdown(assistant_response)
                st.session_state.sessions[st.session_state.active_session].append({"role": "assistant", "content": assistant_response})
    
    except Exception as e:
        error_msg = f"Erro ao processar: {str(e)}"
        st.error(error_msg)
        st.session_state.sessions[st.session_state.active_session].append({"role": "assistant", "content": error_msg})

# Botão para limpar histórico da sessão atual
if st.sidebar.button("🧹 Limpar Histórico da Sessão"):
    if st.session_state.active_session in st.session_state.sessions:
        st.session_state.sessions[st.session_state.active_session] = []
        st.rerun()

# Status do agente
st.sidebar.markdown("---")
st.sidebar.subheader("Status")
st.sidebar.success("✅ Orquestrador Ativo")