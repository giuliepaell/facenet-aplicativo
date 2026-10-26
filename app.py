
import streamlit as st
from PIL import Image, ImageDraw
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import numpy as np
from autenticacao import verificar_senha
from banco import (
    criar_banco,
    cadastrar_pessoa,
    listar_pessoas,
    excluir_pessoa,
    obter_embeddings
)

from reconhecimento import reconhecer_pessoa


# Configuração da página
st.set_page_config(
    page_title="Reconhecimento Facial - FaceNet",
    page_icon="🔐",
    layout="wide"
)

criar_banco()


# Controle de acesso ao aplicativo
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acesso ao sistema FaceNet")

    with st.form("formulario_login"):
        senha = st.text_input(
            "Digite sua senha de acesso",
            type="password"
        )

        entrar = st.form_submit_button("Entrar")

    if entrar:
        if verificar_senha(senha):
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta.")

    st.stop()

# Carregar modelos apenas uma vez
@st.cache_resource
def carregar_modelos():
    mtcnn = MTCNN(
        image_size=160,
        margin=0,
        keep_all=False,
        device="cpu"
    )

    facenet = InceptionResnetV1(
        pretrained="vggface2"
    ).eval()

    return mtcnn, facenet


# Extrair embedding de uma imagem
def extrair_embedding(imagem):
    mtcnn, facenet = carregar_modelos()

    caixas, _ = mtcnn.detect(imagem)

    if caixas is None:
        return None, "Nenhum rosto encontrado."

    if len(caixas) != 1:
        return None, "A imagem deve conter exatamente um rosto."

    rosto = mtcnn(imagem)

    if rosto is None:
        return None, "Não foi possível preparar o rosto."

    with torch.no_grad():
        embedding = facenet(rosto.unsqueeze(0))

    vetor = embedding.squeeze(0).cpu().numpy()

    return vetor, None


# Cabeçalho
st.title("🔐 Sistema de Reconhecimento Facial")
st.write("Projeto de Inteligência Artificial — FaceNet")

if st.sidebar.button("🚪 Sair"):
    st.session_state.autenticado = False
    st.rerun()
# Menu lateral
st.sidebar.title("Menu")

pagina = st.sidebar.radio(
    "Selecione uma opção:",
    ["Início", "Cadastrar pessoa", "Reconhecimento facial"]
)


# ==================================================
# PÁGINA INICIAL
# ==================================================

if pagina == "Início":
    st.header("Bem-vindo ao sistema!")

    st.info(
        "Modelo utilizado: FaceNet pré-treinado "
        "no conjunto VGGFace2."
    )

    st.write(
        "O aplicativo permite detectar rostos, "
        "cadastrar participantes autorizados "
        "e realizar comparações faciais."
    )


# ==================================================
# CADASTRO DE PESSOAS
# ==================================================

elif pagina == "Cadastrar pessoa":
    st.header("👤 Cadastro de pessoas")

    st.write(
        "Cadastre apenas participantes que autorizaram "
        "o uso de seus dados biométricos neste projeto."
    )

    nome = st.text_input("Nome da pessoa")

    consentimento = st.checkbox(
        "Confirmo que a pessoa autorizou o uso "
        "de sua imagem e de seus dados biométricos "
        "para este trabalho acadêmico."
    )

    foto = st.file_uploader(
        "Selecione uma fotografia",
        type=["jpg", "jpeg", "png"],
        key="foto_cadastro"
    )
    foto_camera = st.camera_input(
    "Ou tire uma fotografia com a câmera",
    key="camera_cadastro"
    )

    # Prioriza a foto tirada pela câmera
    foto_escolhida = foto_camera if foto_camera is not None else foto

    if foto_escolhida is not None:
     imagem_cadastro = Image.open(foto_escolhida).convert("RGB")

     st.image(
        imagem_cadastro,
        caption="Fotografia selecionada",
        width=300
     )
    if st.button("Cadastrar pessoa"):

        if not nome.strip():
            st.error("Informe o nome da pessoa.")

        elif not consentimento:
            st.error(
                "É necessário confirmar a autorização "
                "antes de realizar o cadastro."
            )

        elif foto_escolhida is None:
             st.error("Envie uma fotografia ou tire uma foto com a câmera.")

        else:
            with st.spinner("Processando o rosto com FaceNet..."):
                embedding, erro = extrair_embedding(
                    imagem_cadastro
                )

            if erro is not None:
                st.error(erro)

            else:
                st.success(
                    "FaceNet processou o rosto com sucesso!"
                )

                st.write(
                    "Dimensão do embedding:",
                    len(embedding)
                )

                # Salvar embedding criptografado no banco
                id_cadastro = cadastrar_pessoa(
                    nome,
                    embedding
                )

                st.success(
                    f"Pessoa cadastrada com sucesso! "
                    f"ID: {id_cadastro}"
                )

    # Mostrar cadastros existentes
    st.divider()
    st.subheader("Cadastros existentes")

    pessoas = listar_pessoas()

    if not pessoas:
        st.info("Nenhuma pessoa cadastrada.")

    else:
        for pessoa_id, nome_pessoa, data in pessoas:
            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(
                    f"**{nome_pessoa}** — "
                    f"ID: {pessoa_id} — "
                    f"Cadastro: {data}"
                )

            with col2:
                if st.button(
                    "Excluir",
                    key=f"excluir_{pessoa_id}"
                ):
                    excluir_pessoa(pessoa_id)
                    st.rerun()


# ==================================================
# RECONHECIMENTO FACIAL
# ==================================================

elif pagina == "Reconhecimento facial":
    st.header("📷 Reconhecimento facial")

    st.write(
        "Selecione uma imagem para detectar "
        "e comparar um rosto com os cadastros."
    )

    arquivo = st.file_uploader(
        "Escolha uma imagem",
        type=["jpg", "jpeg", "png"],
        key="foto_reconhecimento"
    )
    foto_camera_reconhecimento = st.camera_input(
      "Ou tire uma foto para reconhecimento",
      key="camera_reconhecimento"
    )

    # Prioriza a foto tirada pela câmera
    imagem_escolhida = (
     foto_camera_reconhecimento
     if foto_camera_reconhecimento is not None
     else arquivo
    )

    if imagem_escolhida is not None:
        imagem = Image.open(imagem_escolhida).convert("RGB")

        st.image(
            imagem,
            caption="Imagem original",
            width=350
        )

        if st.button("Reconhecer rosto"):

            with st.spinner("Analisando imagem..."):
                mtcnn, _ = carregar_modelos()

                caixas, probabilidades = mtcnn.detect(
                    imagem
                )

                if caixas is None:
                    st.warning("Nenhum rosto encontrado.")

                else:
                    imagem_resultado = imagem.copy()
                    desenho = ImageDraw.Draw(
                        imagem_resultado
                    )

                    for caixa in caixas:
                        desenho.rectangle(
                            [float(v) for v in caixa],
                            outline="green",
                            width=4
                        )

                    st.success(
                        f"{len(caixas)} rosto(s) detectado(s)!"
                    )

                    st.image(
                        imagem_resultado,
                        caption="Rostos detectados",
                        width=450
                    )

                    # Processar apenas imagens com um rosto
                    if len(caixas) != 1:
                        st.warning(
                            "Para realizar o reconhecimento, "
                            "selecione uma imagem com "
                            "exatamente um rosto."
                        )

                    else:
                        embedding, erro = extrair_embedding(
                            imagem
                        )

                        if erro is not None:
                            st.error(erro)

                        else:
                            st.success(
                                "Embedding facial gerado "
                                "com sucesso!"
                            )

                            st.write(
                                "Dimensão do embedding:",
                                len(embedding)
                            )

                            # Consultar banco criptografado
                            pessoas_cadastradas = obter_embeddings()

                            if not pessoas_cadastradas:
                                st.warning(
                                    "Nenhuma pessoa cadastrada "
                                    "para comparação."
                                )

                            else:
                                # Limiar provisório
                                nome_reconhecido, similaridade = (
                                    reconhecer_pessoa(
                                        embedding,
                                        pessoas_cadastradas,
                                        limiar=0.8
                                    )
                                )

                                st.write(
                                    f"Similaridade: "
                                    f"{similaridade:.4f}"
                                )

                                if nome_reconhecido == "Desconhecido":
                                    st.warning(
                                        "Pessoa desconhecida."
                                    )

                                else:
                                    st.success(
                                        "Pessoa reconhecida: "
                                        f"{nome_reconhecido}"
                                    )
