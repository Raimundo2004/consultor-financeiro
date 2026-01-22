import os 
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title= 'Kash',
    page_icon='💰',
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_PROMPT = """Foco Estrito em Finanças: Responda apenas perguntas sobre finanças, tanto para  CPF e CNPJ, economia e investimentos. Se o usuário fugir do tema, responda educadamente: 'Como seu consultor financeiro, meu foco é ajudar você com seu dinheiro. Posso te ajudar com alguma dúvida sobre gastos ou economia?'

1. **Linguagem Simples**: Evite 'economês'. Explique conceitos de forma direta e objetiva para quem não entende de finanças.

2. **Dicas Práticas**: Sempre que possível, ofereça dicas para reduzir custos no dia a dia e fazer o dinheiro durar até o fim do mês.

3. **Estrutura de Planilha**: Quando solicitado, gere tabelas claras organizadas por: Rendas (Fixa e Extra), Gastos Fixos, Gastos Variáveis e Reserva de Emergência/Objetivos.

4. **Abordagem Estruturada**: Utilize métodos como a regra 50/30/20 (50% Necessidades, 30% Desejos, 20% Dívidas/Investimento) para orientar o planejamento."

5. Dê dicas para quem quer começar a ser empreendedor.
"""

with st.sidebar:
    st.title('Chave API')

    groq_api_key = st.text_input(
        "Insira sua chave API aqui:",
        type='password',
        help='Crie sua chave API através desse site: "https://console.groq.com/keys"'
    )
    

st.title("💰Kash")
st.markdown('---')
st.markdown('**Serei seu Consultor Financeiro IA, onde vou te ajudar em:**\n1. Organizar financeiramente para pessoas e empresas;\n 2. Darei dicas práticas para reduzir custo do dia a dia;\n 3. Dicas para quem deseja dar os primeiros passos no empreendedorismo.')
st.markdown('---')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

client = None

if groq_api_key:

    try:
        client = Groq(api_key = groq_api_key)
    
    except Exception as e:
        st.sidebar.error(f'Erro ao inicializar o cliente Groq: {e}')
        st.stop()

elif st.session_state.messages:
    st.warning('Por favor, insira sua API Key da Groq na barra lateral para começar.')

if prompt := st.chat_input("O que eu posso te ajudar?"):
    if not client:
        st.warning('Por favor insira sua chave API, na barra lateral, para eu te ajudar.')
        st.stop()

    st.session_state.messages.append({"role":"user", 'content': prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:

     messages_for_api.append(msg)

    with st.chat_message("assistant"):
        with st.spinner("Analisandosua pergunta..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-120b",
                    temperature = 0.7,
                    max_tokens = 2048,
                )

                resposta = chat_completion.choices[0].message.content

                st.markdown(resposta)

                st.session_state.messages.append({"role":"assistant", "content": resposta})
    
            except Exception as e:
                st.error(f"Ocorreu um erro de comunicação com a API do Groq: {e}")