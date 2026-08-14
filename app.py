import os
from requests.auth import HTTPBasicAuth
import requests
import streamlit as str_ui
import tweepy

# Configuración de la página con estilo iOS Moderno
str_ui.set_page_config(
    page_title="Neblina 105.1 FM | Central Center",
    page_icon="📻",
    layout="centered",
)

# --- ESTILOS CSS PERSONALIZADOS (UI Limpia estilo iOS, Degradado Animado y Efectos Translúcidos) ---
ios_css = """
<style>
    /* Importar fuente limpia similar a SF Pro de Apple */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Fondo general de la aplicación */
    .stApp {
        background-color: #f5f7fa;
        color: #001e4d;
    }

    /* Animación de Degradado Continuo para la Cabecera */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .header-container {
        background: linear-gradient(-45deg, #001e4d, #00dd9e, #001e4d, #0077b6);
        background-size: 300% 300%;
        animation: gradientBG 8s ease infinite;
        padding: 35px 20px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 30, 77, 0.15);
    }

    /* Efecto translúcido tipo Glassmorphism para las tarjetas y contenedores */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 30, 77, 0.08);
        margin-bottom: 20px;
    }

    /* Estilo de la barra lateral translúcida tipo iOS */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(0, 0, 0, 0.05);
    }

    /* Botones limpios estilo iOS con acento #00dd9e y texto #001e4d */
    .stButton>button {
        background: linear-gradient(135deg, #00dd9e, #00b37e);
        color: #001e4d;
        font-weight: 600;
        border: none;
        border-radius: 14px;
        padding: 12px 24px;
        box-shadow: 0 4px 15px rgba(0, 221, 158, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 221, 158, 0.4);
        background: linear-gradient(135deg, #00efa8, #00c48a);
        color: #001e4d;
    }

    /* Campos de entrada refinados */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 12px;
        border: 1px solid #d1d9e6;
        background-color: #ffffff;
        color: #001e4d;
    }

    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #00dd9e;
        box-shadow: 0 0 0 2px rgba(0, 221, 158, 0.2);
    }
</style>
"""

str_ui.markdown(ios_css, unsafe_allow_html=True)

# --- CABECERA CON LOGO Y DEGRADADO ANIMADO ---
str_ui.markdown(
    """
    <div class="header-container">
        <img src="https://i0.wp.com/neblina105fm.com/wp-content/uploads/2026/03/Recurso-5%402xQaaa-scaled.png?fit=2560%2C891&ssl=1" 
             style="max-width: 240px; width: 100%; height: auto; margin-bottom: 15px; filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.2));" />
        <h2 style="color: #ffffff; font-weight: 700; margin: 0; font-size: 1.5rem; letter-spacing: -0.5px;">Central de Publicaciones</h2>
        <p style="color: rgba(255,255,255,0.85); font-size: 0.95rem; margin-top: 5px;">Sistema Multiplataforma Inteligente</p>
    </div>
""",
    unsafe_allow_html=True,
)

# --- PANEL LATERAL DE CONFIGURACIÓN ---
with str_ui.sidebar:
    str_ui.header("⚙️ Configuración")
    str_ui.markdown("Credenciales activas del sistema.")

    with str_ui.expander("🌐 WordPress", expanded=False):
        wp_url = str_ui.text_input("URL", value="https://neblina105fm.com")
        wp_user = str_ui.text_input("Usuario", value="neblina105fm.com")
        wp_pass = str_ui.text_input(
            "API Pass", value="gngl rCQ5 tszF oE5K krLc iAgf", type="password"
        )

    with str_ui.expander("✈️ Telegram", expanded=False):
        tg_token = str_ui.text_input(
            "Token",
            value="8887694908:AAEs7UpTrGtg77i97K51Pw6UswhODt8Z7WQ",
            type="password",
        )
        tg_chat_id = str_ui.text_input("Chat ID", value="@neblina105fm")

    with str_ui.expander("✖️ X (Twitter)", expanded=False):
        x_api_key = str_ui.text_input(
            "API Key", value="ChFWf1N8649jifdMmjFBLx01s", type="password"
        )
        x_api_secret = str_ui.text_input(
            "API Secret",
            value="RiqiSD7vTdAPCohq4dSXuTPIXqqinGy7tgcAE9lxAr7NMbeXMc",
            type="password",
        )
        x_access_token = str_ui.text_input(
            "Access Token",
            value="1749171071050276865-sK8LeXSpCwMtN5wHB7tHZKzurYm1aG",
            type="password",
        )
        x_access_secret = str_ui.text_input(
            "Access Secret",
            value="KotoRIzfkgH4Gb5fEcYjmWtW7eR942i76usY8QFiWJfUj",
            type="password",
        )

    with str_ui.expander("📘 Meta / Facebook", expanded=False):
        meta_token = str_ui.text_input(
            "Token",
            value=(
                "EAAPAgugp10QBSE4OZBFicoYZCfWrjLOxzzxFHZAq4sEI9IcVLSKI75aprRjSSZAYWsz2kV2ZAwkeLYbwjf1ZAm3mPnhZAQBoyTqpE1dc5b3epuVAUDjeYKdKAodJHfCSE38ZCxWJYvUZAKjHsBWAUUOMz7lNFdIWtybmFB7qojalpP9ZBuIthjNqNsFbdb6fAhoq1PJJe7IZABDIJJm7IGZAeiH7ZAN3dKkQFZBVVKZAzVaZBFug8CcekxghFbrUZAn8f6fW81fHUHm5cdn2P8CVL3QRoDbMUHcsJ"
            ),
            type="password",
        )
        meta_page_id = str_ui.text_input(
            "Page ID", value="147705650070934"
        )

# --- CUERPO PRINCIPAL (CONTENEDORES TRANSLÚCIDOS) ---
str_ui.markdown("### 1. Selecciona los Destinos de Publicación")
col1, col2, col3, col4 = str_ui.columns(4)
with col1:
    pub_web = str_ui.checkbox("Página Web", value=True)
    pub_fb = str_ui.checkbox("Facebook", value=True)
with col2:
    pub_ig = str_ui.checkbox("Instagram", value=False)
    pub_threads = str_ui.checkbox("Threads", value=False)
with col3:
    pub_x = str_ui.checkbox("X (Twitter)", value=True)
    pub_tg = str_ui.checkbox("Telegram", value=True)
with col4:
    pub_wa = str_ui.checkbox("Canal WhatsApp", value=False)

str_ui.markdown("<br>", unsafe_allow_html=True)

str_ui.markdown("### 2. Contenido Multimedia y Redacción")
titulo = str_ui.text_input(
    "Titular de la Noticia",
    placeholder="Ej: Gran evento en vivo por Neblina 105.1 FM",
)
cuerpo = str_ui.text_area(
    "Cuerpo del Mensaje / Noticia",
    placeholder="Escribe la información detallada aquí...",
)
archivo = str_ui.file_uploader(
    "Adjuntar Imagen o Video", type=["jpg", "jpeg", "png", "mp4"]
)

str_ui.markdown("<br>", unsafe_allow_html=True)

# --- FUNCIONES DE PUBLICACIÓN ---


def subir_imagen_wordpress(archivo, wp_url, wp_user, wp_pass):
    try:
        url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/media"
        headers = {
            "Content-Disposition": f"attachment; filename={archivo.name}"
        }
        files = {"file": archivo.getvalue()}
        response = requests.post(
            url,
            headers=headers,
            files=files,
            auth=HTTPBasicAuth(wp_user, wp_pass.replace(" ", "")),
        )
        if response.status_code == 201:
            return response.json().get("id")
    except Exception:
        pass
    return None


def publicar_en_wordpress(titulo, cuerpo, archivo, wp_url, wp_user, wp_pass):
    if not wp_user or not wp_pass:
        return "❌ Faltan credenciales de WordPress."
    media_id = None
    if archivo:
        media_id = subir_imagen_wordpress(archivo, wp_url, wp_user, wp_pass)
    url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
    data = {
        "title": titulo,
        "content": cuerpo,
        "status": "publish",
        "featured_media": media_id if media_id else 0,
    }
    response = requests.post(
        url,
        data=data,
        auth=HTTPBasicAuth(wp_user, wp_pass.replace(" ", "")),
    )
    if response.status_code == 201:
        return "✅ Publicado en Web con éxito."
    else:
        return f"❌ Error en Web: {response.text}"


def publicar_en_telegram(mensaje, archivo, token, chat_id):
    if not token or not chat_id:
        return "❌ Faltan credenciales de Telegram."
    if archivo:
        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        files = {"photo": archivo.getvalue()}
        payload = {"chat_id": chat_id, "caption": mensaje, "parse_mode": "Markdown"}
        response = requests.post(url, data=payload, files=files)
    else:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"}
        response = requests.post(url, data=payload)
    if response.status_code == 200:
        return "✅ Publicado en Telegram con éxito."
    else:
        return f"❌ Error en Telegram: {response.text}"


def publicar_en_x(
    mensaje, archivo, api_key, api_secret, access_token, access_secret
):
    if not api_key or not api_secret or not access_token or not access_secret:
        return "❌ Faltan credenciales de X."
    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
        )
        if len(mensaje) > 280:
            mensaje = mensaje[:277] + "..."
        if archivo:
            auth = tweepy.OAuth1UserHandler(
                api_key, api_secret, access_token, access_secret
            )
            api_v1 = tweepy.API(auth)
            temp_file = "temp_media.jpg"
            with open(temp_file, "wb") as f:
                f.write(archivo.getvalue())
            media = api_v1.media_upload(temp_file)
            client.create_tweet(text=mensaje, media_ids=[media.media_id])
            if os.path.exists(temp_file):
                os.remove(temp_file)
        else:
            client.create_tweet(text=mensaje)
        return "✅ Publicado en X (Twitter) con éxito."
    except Exception as e:
        return f"❌ Error en X: {str(e)}"


def publicar_en_facebook(mensaje, archivo, page_id, token):
    if not page_id or not token:
        return "❌ Faltan credenciales de Facebook."
    try:
        if archivo:
            url = f"https://graph.facebook.com/v18.0/{page_id}/photos"
            files = {"source": archivo.getvalue()}
            payload = {"caption": mensaje, "access_token": token}
            response = requests.post(url, data=payload, files=files)
        else:
            url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
            payload = {"message": mensaje, "access_token": token}
            response = requests.post(url, data=payload)
        res_json = response.json()
        if "id" in res_json:
            return "✅ Publicado en Facebook con éxito."
        else:
            return f"❌ Error en Facebook: {res_json.get('error', {}).get('message', response.text)}"
    except Exception as e:
        return f"❌ Error en Facebook: {str(e)}"


# --- BOTÓN DE ENVÍO MASIVO ---
if str_ui.button("🚀 Publicar en Canales Seleccionados"):
    if not titulo or not cuerpo:
        str_ui.error("Completa el título y el cuerpo del mensaje.")
    else:
        with str_ui.spinner("Procesando envíos simultáneos..."):
            resultados = []
            mensaje_completo = f"{titulo}\n\n{cuerpo}"

            if pub_web:
                resultados.append(
                    publicar_en_wordpress(
                        titulo, cuerpo, archivo, wp_url, wp_user, wp_pass
                    )
                )
            if pub_tg:
                resultados.append(
                    publicar_en_telegram(
                        f"*{titulo}*\n\n{cuerpo}",
                        archivo,
                        tg_token,
                        tg_chat_id,
                    )
                )
            if pub_x:
                resultados.append(
                    publicar_en_x(
                        mensaje_completo,
                        archivo,
                        x_api_key,
                        x_api_secret,
                        x_access_token,
                        x_access_secret,
                    )
                )
            if pub_fb:
                resultados.append(
                    publicar_en_facebook(
                        mensaje_completo, archivo, meta_page_id, meta_token
                    )
                )

            str_ui.success("¡Operación completada!")
            for r in resultados:
                str_ui.write(r)
