import streamlit as st
import time

st.set_page_config(page_title="Desafio de Turing")

#banco de dados dos textos

questoes = [
    {
        "texto": "A mente humana é um labirinto onde o próprio arquiteto se perde tentando encontrar a saída.",
        "origem": "ia",
        "autor": "ChatGPT"

    },
    {
        "texto": "Chove lá fora, mas aqui dentro a tela ilumina meu rosto com dados frios e calculados.",
        "origem": "ia",
        "autor": "Gemini"
    },
    {
        "texto": "O essencial é invisível aos olhos, e só se pode ver bem com o coração.",
        "origem": "humano",
        "autor": "Antoine de Saint-Exupéry"
    },
    {
        "texto": "Tinha uma pedra no meio do caminho, no meio do caminho tinha uma pedra.",
        "origem": "humano",
        "autor": "Carlos Drummond de Andrade"
    },
]

#memória do jogo - saber onde o streamlit 
#vai lembrar em qual questão e quantos pontos

if 'indice' not in st.session_state:
    st.session_state.indice = 0
if 'pontos' not in st.session_state:
    st.session_state.pontos = 0
if 'fim_de_jogo' not in st.session_state:
    st.session_state.fim_de_jogo = False


#função do jogo

def verificar_resposta(escolha):
    questao_atual = questoes[st.session_state.indice]

    if escolha == questao_atual['origem']:
        st.toast(f"ACERTOU! Era {questao_atual['autor']}.")
        st.session_state.pontos += 1
    else:
        st.toast(f"ERROU! Na verdade era {questao_atual['autor']}.")
    
    time.sleep(1.5)

    if st.session_state.indice < len(questoes) - 1:
        st.session_state.indice +=1
    else:
        st.session_state.fim_de_jogo = True

#interface

st.title("Humano ou IA?")
st.write("Leia o texto e tente adivinhar quem escreveu!")
st.divider()

if not st.session_state.fim_de_jogo:
    questao_atual = questoes[st.session_state.indice]

    st.info(f"\"{questao_atual['texto']}\"")

    #botoes
    coluna1, coluna2 = st.columns(2)

    with coluna1:
        if st.button("Humano", use_container_width=True):
            verificar_resposta("humano")
            st.rerun()
    with coluna2:
        if st.button("Inteligência Artificial", use_container_width=True):
            verificar_resposta("ia")
            st.rerun()
    
    #progresso

    progresso = st.session_state.indice / len(questoes)
    st.progress(progresso)

else:
    st.success("FIM DE JOGO!!")
    st.metric(label="Sua Pontuação Final", value=f"{st.session_state.pontos} de {len(questoes)}")

    if st.session_state.pontos == len(questoes):
        st.balloons() #frescurinha
        st.write("Fera demais! Tunring tá orgulhoso de vc bb!!")

    if st.button("Jogar Novamente"):
        st.session_state.indice = 0
        st.session_state.pontos = 0
        st.session_state.fim_de_jogo = False
        st.rerun()
