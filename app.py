import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Sorteo Neblina 105.5 FM", layout="wide")

# Código de la aplicación web integrado en Streamlit
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sorteo Neblina 105.5 FM</title>
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

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--card-bg);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            padding: 16px 24px;
            border-radius: var(--radius-ios);
            box-shadow: var(--shadow-ios);
            border: 1px solid var(--border-color);
            flex-wrap: wrap;
            gap: 15px;
        }

        .logo-area {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-img {
            height: 42px;
            object-fit: contain;
        }

        .device-selector {
            display: flex;
            background: rgba(0, 0, 0, 0.04);
            padding: 4px;
            border-radius: 12px;
            gap: 4px;
        }

        .device-btn {
            background: transparent;
            border: none;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
        }

        .device-btn.active {
            background: #ffffff;
            color: var(--text-primary);
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .viewport-frame {
            width: 100%;
            display: flex;
            justify-content: center;
            transition: all 0.3s ease;
        }

        .viewport-frame.desktop { max-width: 100%; }
        .viewport-frame.tablet { max-width: 768px; }
        .viewport-frame.mobile { max-width: 414px; }

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
        }

        .stage.active {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .setup-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
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
        }

        textarea, select, input {
            width: 100%;
            padding: 12px 14px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            background: rgba(255, 255, 255, 0.9);
            font-size: 0.9rem;
            outline: none;
        }

        textarea { resize: vertical; height: 160px; }

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

        .ios-btn {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 14px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
        }

        .game-layout {
            display: grid;
            grid-template-columns: 260px 1fr 280px;
            gap: 20px;
            align-items: center;
        }

        @media (max-width: 950px) {
            .game-layout { grid-template-columns: 1fr; }
        }

        .wheel-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }

        .wheel-wrapper {
            position: relative;
            width: 320px;
            height: 320px;
        }

        canvas {
            width: 100%;
            height: 100%;
            border-radius: 50%;
        }

        .wheel-pointer {
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 12px solid transparent;
            border-right: 12px solid transparent;
            border-top: 22px solid #ff3b30;
            z-index: 10;
        }

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
        }

        .winner-name { font-size: 1.4rem; font-weight: 700; }
        .status-text { font-size: 0.9rem; color: var(--text-secondary); }
        .winners-history { max-height: 200px; overflow-y: auto; display: flex; flex-direction: column; gap: 6px; }
        .winner-pill { background: white; padding: 8px 12px; border-radius: 10px; border: 1px solid var(--border-color); font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; gap: 8px; }
    </style>
</head>
<body>

    <div class="app-container">
        <header>
            <div class="logo-area">
                <img src="https://i0.wp.com/neblina105fm.com/wp-content/uploads/2026/03/Recurso-5%402xQaaa-scaled.png?fit=2560%2C891&ssl=1" alt="Neblina 105.5 FM" class="logo-img" style="height: 40px;">
            </div>
            <div class="device-selector">
                <button class="device-btn active" onclick="setDevice('desktop', this)">💻 Escritorio</button>
                <button class="device-btn" onclick="setDevice('tablet', this)">📱 Tablet</button>
                <button class="device-btn" onclick="setDevice('mobile', this)">📱 Móvil</button>
            </div>
            <div id="header-stats" class="status-text">Participantes: 0</div>
        </header>

        <div class="viewport-frame desktop" id="viewport-frame">
            <section id="stage-1" class="stage active">
                <div class="setup-grid">
                    <div class="panel-box">
                        <h3>👥 Participantes (Máx. 150)</h3>
                        <textarea id="participants-input" placeholder="Escribe o pega los nombres (uno por línea)..."></textarea>
                        <div class="status-text">Total: <span id="count-display">0</span> / 150</div>
                    </div>

                    <div class="panel-box">
                        <h3>📋 Puestos Generados</h3>
                        <div class="participants-list-preview" id="preview-list">
                            <div class="preview-item">Aún no hay participantes...</div>
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
                            <button class="ios-btn" onclick="goToStage2()">Configurar Rueda ➔</button>
                        </div>
                    </div>
                </div>
            </section>

            <section id="stage-2" class="stage">
                <div class="game-layout">
                    <div class="panel-box">
                        <h3>📌 En Juego</h3>
                        <div class="participants-list-preview" id="active-participants-list" style="height: 240px;"></div>
                    </div>

                    <div class="wheel-container">
                        <div class="wheel-wrapper">
                            <div class="wheel-pointer"></div>
                            <canvas id="wheelCanvas" width="350" height="350"></canvas>
                        </div>
                        <div style="margin-top: 15px; display: flex; gap: 8px; width: 100%;">
                            <button class="ios-btn" id="spin-btn" onclick="startBatchSpin()">🎯 ¡Girar!</button>
                            <button class="ios-btn" style="background: #e5e5ea; color: #000;" onclick="resetApp()">🔄</button>
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
    </div>

    <script>
        const vectorEmojis = ["⭐", "🎉", "🔥", "💎", "🍀", "🚀", "🎨", "🎵", "🏆", "🎁", "✨", "💫"];
        let participants = [], activeParticipants = [], targetWinnersCount = 1, pendingBatchWinners = 0, isSpinning = false;
        const canvas = document.getElementById('wheelCanvas');
        const ctx = canvas.getContext('2d');
        let currentAngle = 0, spinVelocity = 0;
        const wheelColors = ["#FF3B30", "#FF9500", "#FFCC00", "#4CD964", "#5AC8FA", "#007AFF", "#5856D6", "#FF2D55", "#00C7BE"];

        function setDevice(type, btn) {
            document.querySelectorAll('.device-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('viewport-frame').className = `viewport-frame ${type}`;
        }

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playTick() {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator(), g = audioCtx.createGain();
            osc.frequency.setValueAtTime(600, audioCtx.currentTime);
            osc.connect(g); g.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 0.04);
        }
        function playWin() {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            [523, 659, 783, 1046].forEach((f, i) => {
                const osc = audioCtx.createOscillator(), g = audioCtx.createGain();
                osc.frequency.setValueAtTime(f, audioCtx.currentTime + i * 0.06);
                osc.connect(g); g.connect(audioCtx.destination);
                osc.start(audioCtx.currentTime + i * 0.06);
                osc.stop(audioCtx.currentTime + i * 0.06 + 0.3);
            });
        }

        document.getElementById('participants-input').addEventListener('input', (e) => {
            participants = e.target.value.split('\\n').map(p => p.trim()).filter(p => p).slice(0, 150);
            document.getElementById('count-display').innerText = participants.length;
            document.getElementById('header-stats').innerText = `Participantes: ${participants.length}`;
            updatePreviewList();
        });

        function updatePreviewList() {
            const c = document.getElementById('preview-list');
            c.innerHTML = participants.length ? '' : '<div class="preview-item">Aún no hay participantes...</div>';
            participants.forEach((p, i) => {
                c.innerHTML += `<div class="preview-item"><span>Puesto ${i + 1}: ${p}</span><span>${vectorEmojis[i % vectorEmojis.length]}</span></div>`;
            });
        }

        function goToStage2() {
            if (!participants.length) return alert("Ingresa al menos un participante.");
            targetWinnersCount = parseInt(document.getElementById('winners-count').value);
            activeParticipants = [...participants];
            document.getElementById('stage-1').classList.remove('active');
            document.getElementById('stage-2').classList.add('active');
            updateActiveUI(); drawWheel();
        }

        function updateActiveUI() {
            const c = document.getElementById('active-participants-list');
            c.innerHTML = '';
            activeParticipants.forEach((p, i) => c.innerHTML += `<div class="preview-item"><span>${i + 1}. ${p}</span></div>`);
        }

        function drawWheel() {
            const n = activeParticipants.length, cx = canvas.width / 2, cy = canvas.height / 2, r = canvas.width / 2 - 8;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (!n) {
                ctx.beginPath(); ctx.arc(cx, cy, r, 0, 2 * Math.PI);
                ctx.fillStyle = "#e5e5ea"; ctx.fill(); return;
            }
            const arc = (2 * Math.PI) / n;
            for (let i = 0; i < n; i++) {
                const sa = currentAngle + i * arc, ea = sa + arc;
                ctx.beginPath(); ctx.moveTo(cx, cy); ctx.arc(cx, cy, r, sa, ea);
                ctx.fillStyle = wheelColors[i % wheelColors.length]; ctx.fill();
                ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.stroke();
                ctx.save(); ctx.translate(cx, cy); ctx.rotate(sa + arc / 2);
                ctx.textAlign = "right"; ctx.fillStyle = "#fff"; ctx.font = "bold 11px sans-serif";
                ctx.fillText(activeParticipants[i].substring(0, 8), r - 20, 4);
                ctx.restore();
            }
            ctx.beginPath(); ctx.arc(cx, cy, 30, 0, 2 * Math.PI);
            ctx.fillStyle = "#fff"; ctx.fill();
            ctx.font = "18px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
            ctx.fillText("🎯", cx, cy);
        }

        function startBatchSpin() {
            if (isSpinning || !activeParticipants.length) return;
            pendingBatchWinners = Math.min(targetWinnersCount, activeParticipants.length);
            runSpin();
        }

        function runSpin() {
            if (pendingBatchWinners <= 0 || !activeParticipants.length) {
                isSpinning = false;
                document.getElementById('spin-status-msg').innerText = "¡Sorteo finalizado!";
                return;
            }
            isSpinning = true;
            document.getElementById('spin-status-msg').innerText = `Faltan ${pendingBatchWinners} ganadores...`;
            spinVelocity = Math.random() * 0.18 + 0.38;
            let lastSeg = -1;

            function animate() {
                currentAngle += spinVelocity;
                spinVelocity *= 0.982;
                const n = activeParticipants.length, arc = (2 * Math.PI) / n;
                const seg = Math.floor(((2 * Math.PI - (currentAngle % (2 * Math.PI))) % (2 * Math.PI)) / arc);
                if (seg !== lastSeg) { playTick(); lastSeg = seg; }
                drawWheel();
                if (spinVelocity > 0.002) requestAnimationFrame(animate);
                else { isSpinning = false; finishSpin(seg); }
            }
            requestAnimationFrame(animate);
        }

        function finishSpin(idx) {
            const name = activeParticipants[idx], emoji = vectorEmojis[Math.floor(Math.random() * vectorEmojis.length)];
            playWin();
            document.getElementById('display-winner-name').innerText = name;
            document.getElementById('current-winner-card').querySelector('.winner-avatar').innerText = emoji;
            document.getElementById('winners-history-list').innerHTML = `<div class="winner-pill"><span>${emoji}</span> <span>${name}</span></div>` + document.getElementById('winners-history-list').innerHTML;
            
            activeParticipants.splice(idx, 1);
            updateActiveUI(); drawWheel();
            pendingBatchWinners--;

            if (pendingBatchWinners > 0) setTimeout(runSpin, 1500);
            else document.getElementById('spin-status-msg').innerText = "¡Todos seleccionados!";
        }

        function resetApp() { location.reload(); }
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=750, scrolling=True)
