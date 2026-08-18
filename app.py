import streamlit as st

# Configuración de la página para computadora (layout wide)
st.set_page_config(
    page_title="Sorteo Neblina 105.5 FM",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Código de la aplicación web integrado en Streamlit
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sorteo Neblina 105.5 FM - Escritorio</title>
    <link href="https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #f5f5f7;
            --card-bg: rgba(255, 255, 255, 0.85);
            --text-primary: #1d1d1f;
            --text-secondary: #86868b;
            --accent-cyan: #00c7be;
            --accent-blue: #007aff;
            --border-color: rgba(0, 0, 0, 0.08);
            --shadow-ios: 0 10px 30px rgba(0, 0, 0, 0.05);
            --radius-ios: 24px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }

        .app-container {
            width: 100%;
            max-width: 1280px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        /* HEADER DE ESCRITORIO */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--card-bg);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            padding: 16px 30px;
            border-radius: var(--radius-ios);
            box-shadow: var(--shadow-ios);
            border: 1px solid var(--border-color);
        }

        .logo-area {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-img {
            height: 45px;
            object-fit: contain;
        }

        header h1 {
            font-size: 1.2rem;
            font-weight: 600;
            letter-spacing: -0.4px;
            color: var(--text-primary);
        }

        /* SECCIONES / STAGES */
        .stage {
            display: none;
            width: 100%;
            background: var(--card-bg);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            padding: 24px;
            border-radius: var(--radius-ios);
            box-shadow: var(--shadow-ios);
            border: 1px solid var(--border-color);
            animation: fadeIn 0.4s ease forwards;
        }

        .stage.active {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* DISEÑO ETAPA 1 */
        .setup-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
        }

        .panel-box {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .panel-box h3 {
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        textarea, select, input {
            width: 100%;
            padding: 12px 14px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            background: rgba(255, 255, 255, 0.9);
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        textarea:focus, select:focus, input:focus {
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
        }

        textarea {
            resize: vertical;
            height: 160px;
        }

        .participants-list-preview {
            background: rgba(0,0,0,0.015);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            height: 160px;
            overflow-y: auto;
            padding: 8px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .preview-item {
            font-size: 0.85rem;
            padding: 8px 10px;
            background: white;
            border-radius: 10px;
            border: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* BOTONES ESTILO iOS */
        .ios-btn {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 14px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0, 199, 190, 0.25);
            transition: transform 0.1s, opacity 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            text-align: center;
            width: 100%;
        }

        .ios-btn:hover { opacity: 0.95; transform: scale(1.01); }
        .ios-btn:active { transform: scale(0.98); }

        /* ETAPA 2 Y 3: JUEGO ESCRITORIO */
        .game-layout {
            display: grid;
            grid-template-columns: 280px 1fr 300px;
            gap: 20px;
            align-items: center;
        }

        .wheel-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }

        .wheel-wrapper {
            position: relative;
            width: 360px;
            height: 360px;
        }

        canvas {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }

        .wheel-pointer {
            position: absolute;
            top: -14px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 14px solid transparent;
            border-right: 14px solid transparent;
            border-top: 24px solid #ff3b30;
            z-index: 10;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.15));
        }

        /* TARJETA DE GANADOR DINÁMICA */
        .winner-display-box {
            background: linear-gradient(135deg, rgba(0, 199, 190, 0.08), rgba(0, 122, 255, 0.08));
            border: 2px dashed var(--accent-cyan);
            border-radius: var(--radius-ios);
            padding: 20px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 10px;
            min-height: 200px;
        }

        .winner-avatar {
            font-size: 2.8rem;
            background: white;
            width: 75px;
            height: 75px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            box-shadow: 0 6px 16px rgba(0,0,0,0.06);
        }

        .winner-name {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
            word-break: break-word;
        }

        .status-text {
            font-size: 0.9rem;
            font-weight: 500;
            color: var(--text-secondary);
        }

        .winners-history {
            max-height: 200px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .winner-pill {
            background: white;
            padding: 8px 12px;
            border-radius: 10px;
            border: 1px solid var(--border-color);
            font-size: 0.85rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        @keyframes popIn {
            0% { transform: scale(0.85); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        .footer-info {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        /* MODAL / VENTANA EMERGENTE PARA DECIDIR SOBRE EL GANADOR */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(5px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            animation: fadeIn 0.2s ease forwards;
        }

        .modal-card {
            background: #ffffff;
            padding: 30px;
            border-radius: var(--radius-ios);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
            text-align: center;
            max-width: 400px;
            width: 90%;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .modal-card h3 {
            font-size: 1.3rem;
            font-weight: 700;
        }

        .modal-buttons {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
    </style>
</head>
<body>

    <!-- MODAL DE DECISIÓN DE ELIMINACIÓN -->
    <div class="modal-overlay" id="winner-modal">
        <div class="modal-card">
            <div style="font-size: 3rem;" id="modal-emoji">🎉</div>
            <h3>¡Tenemos Ganador!</h3>
            <p class="status-text" id="modal-winner-text" style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary);"></p>
            <p class="status-text">¿Deseas eliminar a este participante de la ruleta para las siguientes jugadas?</p>
            <div class="modal-buttons">
                <button class="ios-btn" style="background: #ff3b30;" onclick="handleWinnerDecision(true)">🗑️ Sí, eliminar</button>
                <button class="ios-btn" style="background: #34c759;" onclick="handleWinnerDecision(false)">🔄 No, mantener</button>
            </div>
        </div>
    </div>

    <div class="app-container">
        <!-- HEADER DE ESCRITORIO CON LOGO Y TÍTULO DEL SORTEO -->
        <header>
            <div class="logo-area">
                <img src="https://i0.wp.com/neblina105fm.com/wp-content/uploads/2026/03/Recurso-5%402xQaaa-scaled.png?fit=2560%2C891&ssl=1" alt="Neblina 105.5 FM" class="logo-img">
                <h1 id="header-sorteo-title">Sorteo Interactivo</h1>
            </div>
            <div id="header-stats" class="status-text" style="font-weight: 600;">Participantes: 0</div>
        </header>

        <!-- ETAPA 1: INGRESO DE PARTICIPANTES, NOMBRE DEL SORTEO Y CONFIGURACIÓN -->
        <section id="stage-1" class="stage active">
            <div class="setup-grid">
                <div class="panel-box">
                    <h3>🎁 Nombre del Sorteo</h3>
                    <input type="text" id="sorteo-name-input" placeholder="Ej: Gran Sorteo Aniversario Neblina" value="Sorteo Interactivo">
                    
                    <h3 style="margin-top: 10px;">👥 Ingresar Participantes (Máx. 150)</h3>
                    <textarea id="participants-input" placeholder="Escribe o pega los nombres (uno por línea)..."></textarea>
                    <div class="footer-info">Total actual: <span id="count-display">0</span> / 150</div>
                </div>

                <div class="panel-box">
                    <h3>📋 Puestos Generados</h3>
                    <div class="participants-list-preview" id="preview-list">
                        <div class="preview-item" style="color:var(--text-secondary)">Aún no hay participantes...</div>
                    </div>
                </div>

                <div class="panel-box">
                    <h3>⚙️ Opciones de Sorteo</h3>
                    <label for="winners-count" class="status-text">Ganadores a sacar por jugada:</label>
                    <select id="winners-count">
                        <option value="1">1 Ganador</option>
                        <option value="2">2 Ganadores</option>
                        <option value="3">3 Ganadores</option>
                        <option value="5">5 Ganadores</option>
                    </select>
                    <div style="margin-top: auto; padding-top: 15px;">
                        <button class="ios-btn" onclick="goToStage2()">
                            <span>Configurar Rueda</span> ➔
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- ETAPA 2 Y 3: RULETA Y SORTEO DINÁMICO -->
        <section id="stage-2" class="stage">
            <div class="game-layout">
                <div class="panel-box">
                    <h3>📌 Participantes en Juego</h3>
                    <div class="participants-list-preview" id="active-participants-list" style="height: 260px;"></div>
                </div>

                <div class="wheel-container">
                    <div class="wheel-wrapper">
                        <div class="wheel-pointer"></div>
                        <canvas id="wheelCanvas" width="380" height="380"></canvas>
                    </div>
                    <div style="margin-top: 15px; display: flex; gap: 8px; width: 100%;">
                        <button class="ios-btn" id="spin-btn" onclick="startBatchSpin()">
                            🎯 ¡Girar Ruleta!
                        </button>
                        <button class="ios-btn" style="background: rgba(0,0,0,0.06); color: var(--text-primary); width: 55px;" onclick="resetApp()" title="Reiniciar">
                            🔄
                        </button>
                    </div>
                </div>

                <div class="panel-box">
                    <h3>🏆 Ganador Actual</h3>
                    <div class="winner-display-box" id="current-winner-card">
                        <div class="winner-avatar">🎁</div>
                        <div class="winner-name" id="display-winner-name">Listo para girar</div>
                        <div class="status-text" id="spin-status-msg">Gira para elegir ganador(es)</div>
                    </div>
                    <div class="winners-history" id="winners-history-list"></div>
                </div>
            </div>
        </section>
    </div>

    <script>
        const vectorEmojis = ["⭐", "🎉", "🔥", "💎", "🍀", "🚀", "🎨", "🎵", "🏆", "🎁", "✨", "💫"];
        
        let participants = [];
        let activeParticipants = [];
        let targetWinnersCount = 1;
        let pendingBatchWinners = 0;
        let isSpinning = false;
        let currentWinnerIndex = -1;
        let currentWinnerName = "";
        let currentWinnerEmoji = "";
        
        const canvas = document.getElementById('wheelCanvas');
        const ctx = canvas.getContext('2d');
        let currentAngle = 0;
        let spinVelocity = 0;
        
        const wheelColors = [
            "#FF3B30", "#FF9500", "#FFCC00", "#4CD964", 
            "#5AC8FA", "#007AFF", "#5856D6", "#FF2D55", "#00C7BE"
        ];

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        function playTickSound() {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(600, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(200, audioCtx.currentTime + 0.04);
            gain.gain.setValueAtTime(0.06, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.04);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.04);
        }

        function playWinSound() {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const notes = [523.25, 659.25, 783.99, 1046.50];
            notes.forEach((freq, index) => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime + index * 0.06);
                gain.gain.setValueAtTime(0.08, audioCtx.currentTime + index * 0.06);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + index * 0.06 + 0.3);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start(audioCtx.currentTime + index * 0.06);
                osc.stop(audioCtx.currentTime + index * 0.06 + 0.3);
            });
        }

        // Actualizar el título del sorteo en tiempo real
        document.getElementById('sorteo-name-input').addEventListener('input', (e) => {
            const val = e.target.value.trim();
            document.getElementById('header-sorteo-title').innerText = val || "Sorteo Interactivo";
        });

        document.getElementById('participants-input').addEventListener('input', (e) => {
            const rawText = e.target.value;
            const lines = rawText.split('\\n').map(p => p.trim()).filter(p => p.length > 0);
            participants = lines.slice(0, 150);

            document.getElementById('count-display').innerText = participants.length;
            document.getElementById('header-stats').innerText = `Participantes: ${participants.length}`;
            updatePreviewList();
        });

        function updatePreviewList() {
            const previewContainer = document.getElementById('preview-list');
            previewContainer.innerHTML = '';
            
            if (participants.length === 0) {
                previewContainer.innerHTML = '<div class="preview-item" style="color:var(--text-secondary)">Aún no hay participantes...</div>';
                return;
            }

            participants.forEach((name, index) => {
                const randomEmoji = vectorEmojis[index % vectorEmojis.length];
                const div = document.createElement('div');
                div.className = 'preview-item';
                div.innerHTML = `<span>Puesto ${index + 1}: ${name}</span><span>${randomEmoji}</span>`;
                previewContainer.appendChild(div);
            });
        }

        function goToStage2() {
            if (participants.length === 0) {
                alert("Por favor, ingresa al menos un participante.");
                return;
            }

            targetWinnersCount = parseInt(document.getElementById('winners-count').value);
            activeParticipants = [...participants];
            
            document.getElementById('stage-1').classList.remove('active');
            document.getElementById('stage-2').classList.add('active');

            updateActiveParticipantsUI();
            drawWheel();
        }

        function updateActiveParticipantsUI() {
            const container = document.getElementById('active-participants-list');
            container.innerHTML = '';
            activeParticipants.forEach((p, idx) => {
                const div = document.createElement('div');
                div.className = 'preview-item';
                div.innerHTML = `<span>${idx + 1}. ${p}</span>`;
                container.appendChild(div);
            });
        }

        function drawWheel() {
            const numSegments = activeParticipants.length;
            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            const radius = canvas.width / 2 - 8;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (numSegments === 0) {
                ctx.beginPath();
                ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
                ctx.fillStyle = "#e5e5ea";
                ctx.fill();
                return;
            }

            const arcSize = (2 * Math.PI) / numSegments;

            for (let i = 0; i < numSegments; i++) {
                const startAngle = currentAngle + i * arcSize;
                const endAngle = startAngle + arcSize;

                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, radius, startAngle, endAngle);
                ctx.closePath();

                ctx.fillStyle = wheelColors[i % wheelColors.length];
                ctx.fill();
                ctx.strokeStyle = "#ffffff";
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.save();
                ctx.translate(centerX, centerY);
                ctx.rotate(startAngle + arcSize / 2);
                ctx.textAlign = "right";
                ctx.fillStyle = "#ffffff";
                ctx.font = "bold 11px -apple-system, sans-serif";
                
                let displayName = activeParticipants[i];
                if (displayName.length > 10) displayName = displayName.substring(0, 8) + "..";
                
                ctx.fillText(displayName, radius - 20, 4);
                ctx.restore();
            }

            ctx.beginPath();
            ctx.arc(centerX, centerY, 30, 0, 2 * Math.PI);
            ctx.fillStyle = "#ffffff";
            ctx.shadowColor = "rgba(0, 0, 0, 0.12)";
            ctx.shadowBlur = 8;
            ctx.fill();
            ctx.shadowBlur = 0;

            ctx.font = "18px sans-serif";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText("🎯", centerX, centerY);
        }

        function startBatchSpin() {
            if (isSpinning) return;
            if (activeParticipants.length === 0) {
                alert("¡Ya no quedan participantes activos!");
                return;
            }

            pendingBatchWinners = Math.min(targetWinnersCount, activeParticipants.length);
            executeNextSpin();
        }

        function executeNextSpin() {
            if (pendingBatchWinners <= 0 || activeParticipants.length === 0) {
                isSpinning = false;
                document.getElementById('spin-btn').style.opacity = '1';
                document.getElementById('spin-status-msg').innerText = "¡Ronda de sorteo finalizada!";
                return;
            }

            isSpinning = true;
            document.getElementById('spin-btn').style.opacity = '0.5';
            document.getElementById('spin-status-msg').innerText = `Faltan ${pendingBatchWinners} ganadores por sacar...`;

            spinVelocity = Math.random() * 0.18 + 0.38;
            let lastSegmentIndex = -1;

            function animateSpin() {
                currentAngle += spinVelocity;
                spinVelocity *= 0.982;

                const numSegments = activeParticipants.length;
                const arcSize = (2 * Math.PI) / numSegments;
                
                const normalizedAngle = (currentAngle % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI);
                const pointerAngle = (1.5 * Math.PI - normalizedAngle + 2 * Math.PI) % (2 * Math.PI);
                const currentSegment = Math.floor(pointerAngle / arcSize) % numSegments;

                if (currentSegment !== lastSegmentIndex) {
                    playTickSound();
                    lastSegmentIndex = currentSegment;
                }

                drawWheel();

                if (spinVelocity > 0.002) {
                    requestAnimationFrame(animateSpin);
                } else {
                    isSpinning = false;
                    // Guardamos temporalmente el ganador y mostramos la ventana modal de decisión
                    currentWinnerIndex = currentSegment;
                    currentWinnerName = activeParticipants[currentWinnerIndex];
                    currentWinnerEmoji = vectorEmojis[Math.floor(Math.random() * vectorEmojis.length)];
                    
                    playWinSound();
                    showWinnerModal(currentWinnerName, currentWinnerEmoji);
                }
            }

            requestAnimationFrame(animateSpin);
        }

        function showWinnerModal(name, emoji) {
            document.getElementById('modal-winner-text').innerText = name;
            document.getElementById('modal-emoji').innerText = emoji;
            document.getElementById('winner-modal').style.display = 'flex';
        }

        function handleWinnerDecision(shouldRemove) {
            // Ocultar modal
            document.getElementById('winner-modal').style.display = 'none';

            // Mostrar el nombre idéntico en la tarjeta grande central
            document.getElementById('display-winner-name').innerText = currentWinnerName;
            document.getElementById('current-winner-card').querySelector('.winner-avatar').innerText = currentWinnerEmoji;

            // Registrar en el historial de ganadores
            const historyList = document.getElementById('winners-history-list');
            const pill = document.createElement('div');
            pill.className = 'winner-pill';
            pill.innerHTML = `<span>${currentWinnerEmoji}</span> <span>${currentWinnerName}</span>`;
            historyList.prepend(pill);

            // Eliminar o mantener según la elección del usuario en la ventana modal
            if (shouldRemove) {
                activeParticipants.splice(currentWinnerIndex, 1);
                updateActiveParticipantsUI();
                drawWheel();
            }

            pendingBatchWinners--;

            if (pendingBatchWinners > 0) {
                setTimeout(() => {
                    executeNextSpin();
                }, 1000);
            } else {
                document.getElementById('spin-btn').style.opacity = '1';
                document.getElementById('spin-status-msg').innerText = "¡Selección completada!";
            }
        }

        function resetApp() {
            location.reload();
        }
    </script>
</body>
</html>
"""

# Renderizar la aplicación en Streamlit
st.components.v1.html(html_code, height=720, scrolling=True)
