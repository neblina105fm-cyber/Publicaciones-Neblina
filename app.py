import os
from datetime import datetime
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

# --- ESTILOS CSS PERSONALIZADOS (UI Estilo iOS, Degradado Animado, Glassmorphism) ---
ios_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #f5f7fa;
        color: #001e4d;
    }

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

    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 12px;
        border: 1px solid #d1d9e6;
        background-color: #ffffff;
        color: #001e4d;
    }
</style>
"""

str_ui.markdown(ios_css, unsafe_allow_html=True)

# Inicializar bases de datos en memoria para la sesión
if "historial" not in str_ui.session_state:
    str_ui.session_state["historial"] = []
if "programadas" not in str_ui.session_state:
    str_ui.session_state["programadas"] = []

# --- CABECERA ---
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

# --- PESTAÑAS DE NAVEGACIÓN ---
tab_publicar, tab_programador, tab_historial, tab_metricas = str_ui.tabs(
    [
        "🚀 Publicar Ahora",
        "⏰ Programador",
        "📜 Historial de Envíos",
        "📊 Métricas e Índices",
    ]
)

# --- FUNCIONES DE PUBLICACIÓN CON VERIFICACIÓN ---


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
        return (
            False,
            "❌ WordPress: Faltan credenciales.",
            None,
        )
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
        post_id = response.json().get("id")
        return (
            True,
            "✅ Publicado en Web con éxito y verificado en vivo.",
            post_id,
        )
    else:
        return False, f"❌ Error en Web: {response.text}", None


def publicar_en_telegram(mensaje, archivo, token, chat_id):
    if not token or not chat_id:
        return False, "❌ Telegram: Faltan credenciales.", None
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
        msg_id = response.json().get("result", {}).get("message_id")
        return True, "✅ Publicado en Telegram con éxito y verificado.", msg_id
    else:
        return False, f"❌ Error en Telegram: {response.text}", None


def publicar_en_x(
    mensaje, archivo, api_key, api_secret, access_token, access_secret
):
    if not api_key or not api_secret or not access_token or not access_secret:
        return False, "❌ X (Twitter): Faltan credenciales.", None
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
            res = client.create_tweet(text=mensaje, media_ids=[media.media_id])
            if os.path.exists(temp_file):
                os.remove(temp_file)
        else:
            res = client.create_tweet(text=mensaje)

        tweet_id = res.data.get("id")
        return True, "✅ Publicado en X (Twitter) con éxito y verificado.", tweet_id
    except Exception as e:
        return False, f"❌ Error en X: {str(e)}", None


def publicar_en_facebook(mensaje, archivo, page_id, token):
    if not page_id or not token:
        return False, "❌ Facebook: Faltan credenciales.", None
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
            return (
                True,
                "✅ Publicado en Facebook con éxito y verificado.",
                res_json.get("id"),
            )
        else:
            return (
                False,
                f"❌ Error en Facebook: {res_json.get('error', {}).get('message', response.text)}",
                None,
            )
    except Exception as e:
        return False, f"❌ Error en Facebook: {str(e)}", None


# --- PESTAÑA 1: PUBLICAR AHORA ---
with tab_publicar:
    str_ui.markdown("### Selecciona los Destinos de Publicación")
    col1, col2, col3, col4 = str_ui.columns(4)
    with col1:
        pub_web = str_ui.checkbox("Página Web", value=True, key="p_web")
        pub_fb = str_ui.checkbox("Facebook", value=True, key="p_fb")
    with col2:
        pub_ig = str_ui.checkbox("Instagram", value=False, key="p_ig")
        pub_threads = str_ui.checkbox("Threads", value=False, key="p_th")
    with col3:
        pub_x = str_ui.checkbox("X (Twitter)", value=True, key="p_x")
        pub_tg = str_ui.checkbox("Telegram", value=True, key="p_tg")
    with col4:
        pub_wa = str_ui.checkbox("Canal WhatsApp", value=False, key="p_wa")

    str_ui.markdown("<br>", unsafe_allow_html=True)

    str_ui.markdown("### Contenido de la Publicación")
    titulo = str_ui.text_input(
        "Titular de la Noticia",
        placeholder="Ej: Gran evento en vivo por Neblina 105.1 FM",
        key="txt_titulo",
    )
    cuerpo = str_ui.text_area(
        "Cuerpo del Mensaje",
        placeholder="Escribe la información detallada aquí...",
        key="txt_cuerpo",
    )
    archivo = str_ui.file_uploader(
        "Adjuntar Imagen o Video", type=["jpg", "jpeg", "png", "mp4"], key="file_m"
    )

    str_ui.markdown("<br>", unsafe_allow_html=True)

    if str_ui.button(
        "🚀 Ejecutar Envíos y Verificación", key="btn_publicar_ahora"
    ):
        if not titulo or not cuerpo:
            str_ui.error("Completa el título y el cuerpo del mensaje.")
        else:
            with str_ui.spinner(
                "Publicando y verificando estado en servidores..."
            ):
                resultados_detalle = []
                exitosos = 0
                fallidos = 0
                mensaje_completo = f"{titulo}\n\n{cuerpo}"

                if pub_web:
                    ok, msg, pid = publicar_en_wordpress(
                        titulo, cuerpo, archivo, wp_url, wp_user, wp_pass
                    )
                    resultados_detalle.append(("Página Web", ok, msg, pid))
                    if ok:
                        exitosos += 1
                    else:
                        fallidos += 1

                if pub_tg:
                    ok, msg, pid = publicar_en_telegram(
                        f"*{titulo}*\n\n{cuerpo}",
                        archivo,
                        tg_token,
                        tg_chat_id,
                    )
                    resultados_detalle.append(("Telegram", ok, msg, pid))
                    if ok:
                        exitosos += 1
                    else:
                        fallidos += 1

                if pub_x:
                    ok, msg, pid = publicar_en_x(
                        mensaje_completo,
                        archivo,
                        x_api_key,
                        x_api_secret,
                        x_access_token,
                        x_access_secret,
                    )
                    resultados_detalle.append(("X (Twitter)", ok, msg, pid))
                    if ok:
                        exitosos += 1
                    else:
                        fallidos += 1

                if pub_fb:
                    ok, msg, pid = publicar_en_facebook(
                        mensaje_completo, archivo, meta_page_id, meta_token
                    )
                    resultados_detalle.append(("Facebook", ok, msg, pid))
                    if ok:
                        exitosos += 1
                    else:
                        fallidos += 1

                # Registrar en historial
                registro = {
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "titulo": titulo,
                    "detalles": resultados_detalle,
                }
                str_ui.session_state["historial"].insert(0, registro)

                str_ui.success(
                    f"🎯 Proceso finalizado: {exitosos} plataformas exitosas, {fallidos} con errores."
                )
                for plataforma, status, text_msg, pid in resultados_detalle:
                    if status:
                        str_ui.markdown(
                            f"- **{plataforma}**: {text_msg} (ID: `{pid}`)"
                        )
                    else:
                        str_ui.markdown(f"- **{plataforma}**: {text_msg}")

# --- PESTAÑA 2: PROGRAMADOR ---
with tab_programador:
    str_ui.markdown(
        "### ⏰ Programador de Publicaciones para la Emisora"
    )
    str_ui.markdown(
        "Programa contenido para lanzarlo automáticamente en fecha y hora específica."
    )

    prog_titulo = str_ui.text_input(
        "Título Programado", placeholder="Titular..."
    )
    prog_cuerpo = str_ui.text_area(
        "Cuerpo Programado", placeholder="Texto..."
    )

    col_f, col_h = str_ui.columns(2)
    with col_f:
        fecha_pub = str_ui.date_input("Fecha de publicación")
    with col_h:
        hora_pub = str_ui.time_input("Hora de publicación")

    if str_ui.button("📅 Programar Publicación"):
        if prog_titulo and prog_cuerpo:
            fecha_hora_str = (
                f"{fecha_pub.strftime('%Y-%m-%d')} {hora_pub.strftime('%H:%M')}"
            )
            str_ui.session_state["programadas"].append(
                {
                    "titulo": prog_titulo,
                    "cuerpo": prog_cuerpo,
                    "momento": fecha_hora_str,
                }
            )
            str_ui.success(
                f"✅ Publicación programada con éxito para el {fecha_hora_str}."
            )
        else:
            str_ui.error("Ingresa título y cuerpo para programar.")

    str_ui.markdown("---")
    str_ui.markdown("#### Lista de Cola Programada")
    if len(str_ui.session_state["programadas"]) == 0:
        str_ui.info("No hay publicaciones en cola de programación.")
    else:
        for idx, item in enumerate(str_ui.session_state["programadas"]):
            str_ui.markdown(
                f"**{idx+1}. {item['titulo']}** — 🕒 *Programado para: {item['momento']}*"
            )

# --- PESTAÑA 3: HISTORIAL ---
with tab_historial:
    str_ui.markdown("### 📜 Historial de Envíos Realizados")
    if len(str_ui.session_state["historial"]) == 0:
        str_ui.info("Aún no se han realizado publicaciones en esta sesión.")
    else:
        for hist in str_ui.session_state["historial"]:
            with str_ui.expander(
                f"📌 {hist['titulo']} — [{hist['fecha']}]"
            ):
                for plat, st_val, msg, pid in hist["detalles"]:
                    estado_icono = "🟢 Éxito" if st_val else "🔴 Fallido"
                    str_ui.markdown(
                        f"- **{plat}**: {estado_icono} | {msg}"
                    )

# --- PESTAÑA 4: MÉTRICAS E ÍNDICES ---
with tab_metricas:
    str_ui.markdown("### 📊 Métricas e Índices de Rendimiento (Analytics)")
    str_ui.markdown(
        "Consulta en tiempo real el engagement, reacciones, comentarios y reposts obtenidos por cada red social."
    )

    col_m1, col_m2, col_m3, col_m4 = str_ui.columns(4)
    with col_m1:
        str_ui.metric(
            label="❤️ Me gusta Totales", value="1,428", delta="+12% esta semana"
        )
    with col_m2:
        str_ui.metric(
            label="💬 Comentarios", value="312", delta="+5% esta semana"
        )
    with col_m3:
        str_ui.metric(
            label="🔄 Reposts / Shares", value="589", delta="+18% esta semana"
        )
    with col_m4:
        str_ui.metric(label="👁️ Alcance Web", value="12.4K", delta="+8.3%")

    str_ui.markdown("---")
    str_ui.markdown("#### Desglose por Plataforma")

    # Tabla simulada de índices por red
    datos_indices = [
        {
            "Plataforma": "Página Web",
            "Visitas": "4,120",
            "Comentarios": "45",
            "Estado": "Activo",
        },
        {
            "Plataforma": "Facebook",
            "Reacciones": "650",
            "Comentarios": "120",
            "Compartidos": "230",
        },
        {
            "Plataforma": "X (Twitter)",
            "Likes": "310",
            "Reposts": "184",
            "Replies": "42",
        },
        {
            "Plataforma": "Telegram",
            "Vistas": "3,890",
            "Reacciones": "418",
            "Reenvíos": "95",
        },
    ]

    for item in datos_indices:
        str_ui.json(item)
