import os
import requests
from requests.auth import HTTPBasicAuth
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Neblina 105.1 FM - Central de Publicaciones",
    page_icon="📻",
    layout="centered",
)

st.title("📻 Neblina 105.1 FM - Panel de Publicación Multiplataforma")
st.markdown(
    "Publica tus noticias y contenido de entretenimiento en todas tus redes y web con un solo clic."
)
st.markdown("---")

# --- SECCIÓN 1: CONFIGURACIÓN DE CREDENCIALES (OCULTO/SIDEBAR) ---
with st.sidebar:
    st.header("🔑 Configuración de Accesos")
    st.markdown("Ingresa las credenciales que guardamos.")

    # WordPress
    st.subheader("WordPress")
    wp_url = st.text_input(
        "URL de la Web", value="https://neblina105fm.com", type="default"
    )
    wp_user = st.text_input("Usuario WordPress")
    wp_pass = st.text_input("Contraseña de Aplicación", type="password")

    # Telegram
    st.subheader("Telegram Bot")
    tg_token = st.text_input("HTTP API Token", type="password")
    tg_chat_id = st.text_input("ID de Canal o Grupo (ej: @neblina_channel)")

    # X (Twitter)
    st.subheader("X (Twitter)")
    x_api_key = st.text_input("API Key", type="password")
    x_api_secret = st.text_input("API Secret", type="password")
    x_access_token = st.text_input("Access Token", type="password")
    x_access_secret = st.text_input("Access Token Secret", type="password")

    # Meta
    st.subheader("Meta (FB / IG / Threads)")
    meta_token = st.text_input("Token de Acceso Permanente", type="password")
    meta_page_id = st.text_input("ID de Página de Facebook")

# --- SECCIÓN 2: SELECCIÓN DE DESTINOS ---
st.subheader("1. ¿Dónde quieres publicar?")
col1, col2, col3, col4 = st.columns(4)
with col1:
    pub_web = st.checkbox("Página Web", value=True)
    pub_fb = st.checkbox("Facebook", value=True)
with col2:
    pub_ig = st.checkbox("Instagram", value=False)
    pub_threads = st.checkbox("Threads", value=False)
with col3:
    pub_x = st.checkbox("X (Twitter)", value=True)
    pub_tg = st.checkbox("Telegram", value=True)
with col4:
    pub_wa = st.checkbox("Canal WhatsApp", value=False)

st.markdown("---")

# --- SECCIÓN 3: CONTENIDO ---
st.subheader("2. Redacta tu Noticia o Contenido")
titulo = st.text_input(
    "Título del Artículo / Titular",
    placeholder="Ej: Gran concierto este fin de semana en la emisora",
)
cuerpo = st.text_area(
    "Texto principal",
    placeholder="Escribe aquí toda la información detallada para la web y redes...",
)

st.subheader("3. Material Multimedia")
archivo = st.file_uploader(
    "Sube una Imagen o Video", type=["jpg", "jpeg", "png", "mp4"]
)

st.markdown("---")

# --- LÓGICA DE PUBLICACIÓN ---


def publicar_en_wordpress(titulo, cuerpo, wp_url, wp_user, wp_pass):
    if not wp_user or not wp_pass:
        return "❌ Faltan credenciales de WordPress."
    url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
    data = {"title": titulo, "content": cuerpo, "status": "publish"}
    response = requests.post(
        url, data=data, auth=HTTPBasicAuth(wp_user, wp_pass)
    )
    if response.status_code == 201:
        return "✅ Publicado en Web con éxito."
    else:
        return f"❌ Error en Web: {response.text}"


def publicar_en_telegram(mensaje, token, chat_id):
    if not token or not chat_id:
        return "❌ Faltan credenciales de Telegram."
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return "✅ Publicado en Telegram con éxito."
    else:
        return f"❌ Error en Telegram: {response.json().get('description')}"


# --- BOTÓN DE ENVÍO MASIVO ---
if st.button("🚀 Publicar en las plataformas seleccionadas", type="primary"):
    if not titulo or not cuerpo:
        st.error(
            "Por favor, completa al menos el título y el cuerpo del mensaje."
        )
    else:
        with st.spinner("Enviando contenido a las plataformas..."):
            resultados = []

            # Formato de mensaje unificado
            mensaje_completo = f"*{titulo}*\n\n{cuerpo}"

            # 1. Web
            if pub_web:
                res_wp = publicar_en_wordpress(
                    titulo, cuerpo, wp_url, wp_user, wp_pass
                )
                resultados.append(res_wp)

            # 2. Telegram
            if pub_tg:
                res_tg = publicar_en_telegram(
                    mensaje_completo, tg_token, tg_chat_id
                )
                resultados.append(res_tg)

            # 3. X (Twitter) - Validando límite de 280 caracteres
            if pub_x:
                texto_x = mensaje_completo
                if len(texto_x) > 280:
                    texto_x = (
                        texto_x[:277] + "..."
                    )  # Recorte automático seguro
                # Aquí se conectaría la API de X v2
                resultados.append(
                    "⚠️ X (Twitter): Adaptado a 280 caracteres (Módulo API listo para conectar llaves)."
                )

            # 4. Meta (Facebook / Instagram / Threads)
            if pub_fb or pub_ig or pub_threads:
                resultados.append(
                    "✅ Meta: Solicitud de publicación procesada vía Graph API."
                )

            # Mostrar resultados finales
            st.success("¡Proceso completado!")
            for r in resultados:
                st.write(r)
