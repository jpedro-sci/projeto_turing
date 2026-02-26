import streamlit as st
import google.generativeai as genai
import random
import time

st.set_page_config(page_title="Desafio de Turing", layout="centered")

with st.sidebar:
    st.image("ufpb_logo.png", width=120)
    st.title("Sobre o Projeto")
    st.write("Simulação do Teste de Turing.")
    st.divider()

    st.subheader("Equipe")
    st.write("- João Pedro da Silva Araújo")
    st.write("- Társis Lima Gomes da Silva")
    st.write("- Alefe Brito Monteiro")
    st.write("- Gabriel Henrique Cavalcante de Sousa ")
    st.write("- Antônio Jose Batista Salazar")


    st.divider()
    st.caption("Desenvolvido por João Pedro")
    st.caption("Powered by Google Gemini API & Streamlit")

#configuração da API

try:
    CHAVE_API = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=CHAVE_API)
    model = genai.GenerativeModel('gemini-2.5-flash')
    api_funcionando = True

except Exception as e:
    api_funcionando = False
    st.error("AVISO: Chave da API não encontrada. Rodando no modo offline (textos fixos).")  

#banco de textos

textos_humanos = [
    {"texto": "A inteligência é a capacidade de se adaptar ás mudanças.", "autor": "Stephen Hawking"},
    {"texto": "A natureza tem hábitos, não leis eternas.", "autor": "Rupert Sheldrake"},
    {"texto": "Só a verdade nos pode libertar das teias da ilusão." , "autor": "Mário Ferreira dos Santos"},
    {"texto": "A alegria não chega apenas no encontro do achado, mas faz parte do processo da busca.", "autor": "Clarice Lispector"},
    {"texto": "O essencial é invisível aos olhos, e só se pode ver bem com o coração.", "autor": "Antoine de Saint-Exupéry"},
    {"texto": "Tinha uma pedra no meio do caminho, no meio do caminho tinha uma pedra.", "autor": "Carlos Drummond de Andrade"},
    {"texto": "Toda a nossa ciência, comparada com a realidade, é primitiva e infantil." , "autor": "Albert Einstein"},
    {"texto": "Onde não há imaginação não há horror." , "autor": "Arthur Conan Doyle"},
    {"texto": "Penso, logo existo.", "autor": "René Descartes"},
    {"texto": "A mente humana é como um paraquedas: só funciona se estiver aberta.", "autor": "Frank Zappa"}
]

#memoria

if 'pontos' not in st.session_state:
    st.session_state.pontos = 0
if 'rodada' not in st.session_state:
    st.session_state.rodada = 1
if 'questao_atual' not in st.session_state:
    st.session_state.questao_atual = None
if 'textos_usados' not in st.session_state:
    st.session_state.textos_usados = []

#funções

def gerar_texto_ia():
    temas = ["os labirintos da mente humana", "a imensidão do universo cósmico", "a essência de um café arábica perfeito", "o fluxo incontrolável do tempo", "a evolução da sociedade"]
    tema = random.choice(temas)
    prompt = f"Escreva uma única frase poética e filosófica (máximo de 15 palavras) sobre {tema}. Não use aspas, emojis, nem hashtags. Pareça um pensador clássico e seja muito direto."

    try:
        resposta = model.generate_content(prompt, generation_config={"temperature": 0.4})
        return {"texto": resposta.text.strip(), "origem": "ia", "autor": "Gemini"}
    except Exception as e:
        st.error(f"Erro ao conectar com o Google: {e}") 
        return {"texto": "O silêncio das máquinas ecoa no vazio do servidor desconectado.", "origem": "ia", "autor": "IA (Offline)"}


def preparar_rodada():
    with st.spinner("Analisando os textos para a proxima rodada..."):
        if random.choice([True, False]) and api_funcionando:
            st.session_state.questao_atual = gerar_texto_ia()
        else:

            textos_disponiveis = [t for t in textos_humanos if t["texto"] not in st.session_state.textos_usados]
            
            if not textos_disponiveis:
                textos_disponiveis = textos_humanos
                st.session_state.textos_usados = []

            humano = random.choice(textos_disponiveis)
            st.session_state.textos_usados.append(humano["texto"])
            st.session_state.questao_atual = {"texto": humano["texto"], "origem": "humano", "autor": humano["autor"]}


def verificar_resposta(escolha):
    correta = st.session_state.questao_atual['origem']
    autor = st.session_state.questao_atual['autor']

    if escolha == correta:
        st.toast(f"ACERTOU!! O autor era: {autor}.")
        st.session_state.pontos += 1
    else:
        st.toast(f"ERROU!! Na verdade foi escrito por: {autor}.")
    
    time.sleep(2)
    st.session_state.rodada += 1
    st.session_state.questao_atual = None

if st.session_state.questao_atual is None and st.session_state.rodada <= 10:
    preparar_rodada()

st.title("DESAFIO DE TURING")

if st.session_state.rodada <= 10:
    st.markdown("### Será que você conseguirá diferenciar a bela mente humana de uma Inteligência Artificial?")

    col_rodada, col_pontos = st.columns(2)
    col_rodada.metric(label = "Rodada Atual", value=st.session_state.rodada)
    col_pontos.metric(label = "Sua Pontuação", value=st.session_state.pontos)

    st.divider()

    if st.session_state.questao_atual:
        st.info(f"**\"{st.session_state.questao_atual['texto']}\"**")

        st.write("Quem escreveu a frase acima?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Humano", use_container_width=True, type='primary'):
                verificar_resposta("humano")
                st.rerun()
        with col2:
            if st.button("Inteligência Artificial", use_container_width=True, type='primary'):
                verificar_resposta("ia")
                st.rerun()
else:
    st.success("FIM DE JOGO!")
    st.metric(label="Pontuação Final", value=f"{st.session_state.pontos} de 10")

    st.divider()

    if st.session_state.pontos == 10:
        st.balloons() 
        st.write("### Platinado! \nNem a malandragem da máquina conseguiu te enganar.")
    elif st.session_state.pontos >= 7:
        st.write("### Bom, mas não o suficiente. Você ainda foi enganado pela IA!")
    else:
        st.write("### Cuidado, você parece uma senhora com 60 anos que acredita em postagens do face!")
    
    if st.button("Jogar Novamente", type='primary'):
        st.session_state.pontos = 0
        st.session_state.rodada = 1
        st.session_state.textos_usados = []
        st.session_state.questao_atual = None
        st.rerun()