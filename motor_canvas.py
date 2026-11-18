def obtener_html_simulador():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; color: #e2e8f0; }
  html, body { width: 100%; height: 100dvh; background-color: #060911; overflow: hidden; }
  body { display: flex; flex-direction: column; padding: 6px 10px; gap: 8px; }
  .top-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 6px; background: #111827; padding: 6px 12px; border-radius: 8px; border: 1px solid #1f2937; flex-shrink: 0; }
  .title { font-size: 16px; font-weight: 600; color: #38bdf8; white-space: nowrap; }
  .clock-box { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; background: #060911; padding: 4px 10px; border-radius: 6px; border: 1px solid #374151; }
  .clock { font-family: 'Consolas', monospace; font-size: 19px; font-weight: bold; color: #34d399; letter-spacing: 1px; margin-right: 2px; }
  select { background: #1f2937; color: #f8fafc; border: 1px solid #4b5563; padding: 3px 6px; border-radius: 6px; font-size: 12px; cursor: pointer; outline: none; }
  .controls { display: flex; flex-wrap: wrap; align-items: center; gap: 5px; }
  button { background: #1f2937; border: 1px solid #4b5563; color: #f8fafc; padding: 5px 10px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: 500; }
  button:hover { background: #38bdf8; color: #060911; font-weight: 600; }
  .mini-btn { padding: 2px 7px; font-size: 12px; font-weight: bold; }
  .main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; flex: 1; min-height: 0; }
  .panel { position: relative; background: #03050a; border: 1px solid #1f2937; border-radius: 10px; overflow: hidden; min-height: 0; }
  .panel-header { position: absolute; top: 8px; left: 10px; right: 10px; display: flex; justify-content: space-between; align-items: center; pointer-events: none; z-index: 10; gap: 4px; }
  .panel-title { font-size: 12px; background: rgba(15, 23, 42, 0.88); padding: 4px 8px; border-radius: 6px; border: 1px solid #334155; display: flex; flex-wrap: wrap; align-items: center; gap: 5px; }
  .zoom-btns { pointer-events: auto; display: flex; gap: 4px; flex-shrink: 0; }
  .zoom-btns button { padding: 3px 8px; font-size: 13px; font-weight: bold; background: rgba(15, 23, 42, 0.92); }
  .legend-bar { position: absolute; bottom: 6px; left: 8px; right: 8px; background: rgba(15, 23, 42, 0.85); border: 1px solid #334155; border-radius: 6px; padding: 3px 8px; font-size: 11px; display: flex; flex-wrap: wrap; gap: 8px; pointer-events: none; width: fit-content; max-width: calc(100% - 16px); }
  canvas { width: 100%; height: 100%; display: block; cursor: crosshair; touch-action: none; }

  @media (max-width: 960px) {
    body { padding: 4px 6px; gap: 5px; }
    .top-bar { padding: 4px 8px; gap: 4px; }
    .title { font-size: 13px; }
    .clock { font-size: 14px; }
    .clock-box { padding: 2px 6px; gap: 4px; }
    select, button { font-size: 11px; padding: 3px 6px; }
    .panel-title { font-size: 11px; padding: 3px 6px; }
    .legend-bar { font-size: 10px; gap: 6px; padding: 2px 6px; }
    .hint-mouse { display: none; }
  }

  @media (max-width: 768px) and (orientation: portrait) {
    .main-grid { grid-template-columns: 1fr; grid-template-rows: 1fr 1fr; gap: 6px; }
  }
</style>
</head>
<body>
<div class="top-bar">
  <div class="title">🌌 Modelo del Globo y las Ondas Desfasadas</div>
  <div class="clock-box">
    <span class="clock" id="reloj">00:00:00</span>
    <select id="sel-ciclo" onchange="cambiarCiclo()">
      <option value="1" selected>📈 Expansión</option>
      <option value="-1">📉 Implosión (Punto Cero)</option>
    </select>
    <button class="mini-btn" onclick="ajustarEscala(-0.3)">-</button>
    <select id="sel-ritmo" onchange="cambiarModoSelect()">
      <option value="0.3">🐢 Lenta</option>
      <option value="1.0" selected>⏩ Normal</option>
      <option value="3.0">🚀 Rápida</option>
    </select>
    <span id="lbl-esc" style="font-size:11px;color:#94a3b8;min-width:30px;">x1.0</span>
    <button class="mini-btn" onclick="ajustarEscala(0.3)">+</button>
  </div>
  <div class="controls">
    <button id="btn-audio" onclick="toggleAudio()">🔊 ON</button>
    <input type="range" id="vol-slider" min="0" max="1" step="0.05" value="0.6" oninput="cambiarVolumen()" style="width:55px;accent-color:#38bdf8;cursor:pointer;" title="Volumen">
    <button onclick="setPlay(true)">▶️ Iniciar</button>
    <button onclick="setPlay(false)">⏸️ Pausa</button>
    <button onclick="stepForward()">⏭️ +1</button>
    <button onclick="resetSim()">🔄 Reiniciar</button>
  </div>
</div>
<div class="main-grid">
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">🌐 Globo Completo | Radio: <span id="lbl-radio" style="color:#38bdf8;font-weight:bold;">1.00x</span> <span id="lbl-fase" style="color:#fbbf24;font-weight:bold;"></span> <span class="hint-mouse" style="color:#94a3b8;font-size:11px;">(🖱️ Recuadro seleccionable)</span></div>
      <div class="zoom-btns">
        <button onclick="zoomMacro *= 1.2">🔍+</button>
        <button onclick="zoomMacro /= 1.2">🔍-</button>
      </div>
    </div>
    <canvas id="canvasMacro"></canvas>
    <div class="legend-bar"><span>🟡 Mantequilla</span><span>🩶 Tinta (M. Oscura)</span><span>🟢 Gas (E. Oscura)</span><span>⚪ Neutrinos</span><span>⚫ Esfera sin luz</span></div>
  </div>
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">
        🔬 Lupa Local | <span id="estado-agua" style="color:#34d399;font-weight:bold;">▶️ Agua Relajada</span>
        <span style="pointer-events:auto;margin-left:4px;display:inline-flex;gap:3px;align-items:center;">
          <button class="mini-btn" onclick="cambiarRitmoLocal(-0.25)">-</button>
          <span id="lbl-ritmo-local" style="font-size:11px;color:#94a3b8;padding:0 2px;">x1.0</span>
          <button class="mini-btn" onclick="cambiarRitmoLocal(0.25)">+</button>
        </span>
      </div>
      <div class="zoom-btns">
        <button onclick="zoomDetalle *= 1.25">🔍+</button>
        <button onclick="zoomDetalle /= 1.25">🔍-</button>
      </div>
    </div>
    <canvas id="canvasZoom"></canvas>
  </div>
</div>

<script>
const cMacro = document.getElementById('canvasMacro'), ctxM = cMacro.getContext('2d');
const cZoom = document.getElementById('canvasZoom'), ctxZ = cZoom.getContext('2d');
let playing = false, simTime = 0, radioActual = 1.0, direccion = 1, lastTs = 0, zoomMacro = 1.0, zoomDetalle = 1.0;
let escala = 1.0, ritmoLocal = 1.0;
let selBox = { x0: -0.25, y0: -0.25, x1: 0.25, y1: 0.25 }, dragging = false, startDrag = {x:0, y:0};

const nodos = Array.from({length: 54}, (_, i) => {
  let a = (i * 137.508) * Math.PI / 180, r = 0.02 + 0.90 * Math.sqrt(i / 54);
  let lobulos = Array.from({length: 12}, (_, k) => 0.78 + 0.35 * Math.sin(i * 2.7 + k * 1.9));
  let puntosMO = Array.from({length: 55}, (_, p) => {
    let pa = p * 2.39996, pr = Math.sqrt((p + 0.5) / 55) * 0.95;
    return { dx: pr * Math.cos(pa), dy: pr * Math.sin(pa), sz: 0.6 + (p % 3) * 0.45 };
  });
  let estrellasGal = Array.from({length: 90}, (_, s) => {
    let brazo = s % 2, frac = (s / 90);
    let rad = 0.14 + frac * 0.76, ang = frac * 4.2 + brazo * Math.PI + Math.sin(s * 7.1) * 0.25;
    return { rad, ang, sz: 0.7 + (s % 4) * 0.55, col: s % 3 === 0 ? '#fef08a' : (s % 3 === 1 ? '#fde047' : '#bae6fd') };
  });
  return { bx: r * Math.cos(a), by: r * Math.sin(a), masa: (i % 5 === 0) ? 2.2 : 1.1, fase: i * 0.7, lobulos, puntosMO, estrellasGal };
});

const enlaces = [];
for (let i = 0; i < nodos.length; i++) {
  for (let j = i + 1; j < nodos.length; j++) {
    let d = Math.hypot(nodos[i].bx - nodos[j].bx, nodos[i].by - nodos[j].by);
    if (d < 0.32) {
      let granos = Array.from({length: 26}, (_, g) => ({
        t: (g + 0.5) / 26, off: Math.sin(g * 5.3 + i) * 0.015, sz: 0.7 + (g % 3) * 0.45
      }));
      enlaces.push({ i, j, granos, rotura: ((i + j) % 4 === 0), faseFluc: (i * 1.3 + j) });
    }
  }
}

const burbujasSueltas = Array.from({length: 26}, (_, i) => {
  let a = (i * 2.399) + 1.1, r = 0.18 + 0.68 * Math.sqrt((i + 0.3) / 26);
  let lobulos = Array.from({length: 8}, (_, k) => 0.8 + 0.3 * Math.cos(i * 4.1 + k * 2.2));
  return { bx: r * Math.cos(a), by: r * Math.sin(a), vx: Math.cos(a + 1.2) * 0.015, vy: Math.sin(a + 1.2) * 0.015, fase: i * 1.1, lobulos };
});

const paletas = ['250, 204, 21', '56, 189, 248', '192, 132, 252', '52, 211, 153'];
const focosGas = Array.from({length: 22}, (_, i) => {
  let esBorde = i >= 10;
  let a = esBorde ? ((i - 10) / 12) * Math.PI * 2 + 0.2 : (i * 2.399) + 0.4;
  let r = esBorde ? 0.88 : 0.18 + (i % 4) * 0.17;
  return { x: r * Math.cos(a), y: r * Math.sin(a), ang: esBorde ? a + Math.PI : a + Math.PI * 0.75, col: paletas[i % 4] };
});

const neutrinos = Array.from({length: 160}, (_, i) => {
  let dir = (i * 2.39996), vel = 0.25 + (i % 5) * 0.08;
  return { x: Math.sin(i*17)*0.85, y: Math.cos(i*11)*0.85, vx: Math.cos(dir)*vel, vy: Math.sin(dir)*vel };
});

function resize() {
  if (cMacro.clientWidth > 0 && cMacro.clientHeight > 0) {
    cMacro.width = cMacro.clientWidth; cMacro.height = cMacro.clientHeight;
  }
  if (cZoom.clientWidth > 0 && cZoom.clientHeight > 0) {
    cZoom.width = cZoom.clientWidth; cZoom.height = cZoom.clientHeight;
  }
}
window.addEventListener('resize', resize);
window.addEventListener('orientationchange', () => setTimeout(resize, 150));
setTimeout(resize, 50);

function cambiarCiclo() { direccion = +document.getElementById('sel-ciclo').value; }
function cambiarModoSelect() { escala = +document.getElementById('sel-ritmo').value; document.getElementById('lbl-esc').innerText = 'x' + escala.toFixed(1); }
function ajustarEscala(delta) { escala = Math.min(5.0, Math.max(0.1, +(escala + delta).toFixed(1))); document.getElementById('lbl-esc').innerText = 'x' + escala.toFixed(1); }
function cambiarRitmoLocal(delta) { ritmoLocal = Math.min(3.0, Math.max(0.2, +(ritmoLocal + delta).toFixed(2))); document.getElementById('lbl-ritmo-local').innerText = 'x' + ritmoLocal.toFixed(1); }

let audioCtx = null, oscFondo = null, oscSub = null, gainFondo = null, audioActivo = true, volumenMaster = 0.6;

function initAudio() {
  if (audioCtx) return;
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  oscFondo = audioCtx.createOscillator();
  oscSub = audioCtx.createOscillator();
  gainFondo = audioCtx.createGain();
  oscFondo.type = 'triangle';
  oscSub.type = 'sine';
  oscFondo.frequency.value = 65;
  oscSub.frequency.value = 32.5;
  gainFondo.gain.value = 0.0001;
  oscFondo.connect(gainFondo);
  oscSub.connect(gainFondo);
  gainFondo.connect(audioCtx.destination);
  oscFondo.start();
  oscSub.start();
}

function cambiarVolumen() {
  volumenMaster = +document.getElementById('vol-slider').value;
  if (audioActivo && playing && gainFondo && audioCtx) {
    gainFondo.gain.setTargetAtTime(0.55 * volumenMaster, audioCtx.currentTime, 0.08);
  }
}

function toggleAudio() {
  audioActivo = !audioActivo;
  document.getElementById('btn-audio').innerText = audioActivo ? '🔊 ON' : '🔇 OFF';
  if (!audioActivo && gainFondo && audioCtx) {
    gainFondo.gain.setTargetAtTime(0.0001, audioCtx.currentTime, 0.08);
  } else if (audioActivo && playing && gainFondo && audioCtx) {
    gainFondo.gain.setTargetAtTime(0.55 * volumenMaster, audioCtx.currentTime, 0.2);
  }
}

function sonarBigBang() {
  if (!audioActivo || volumenMaster <= 0) return;
  initAudio();
  if (audioCtx.state === 'suspended') audioCtx.resume();
  const now = audioCtx.currentTime;

  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'sine';
  osc.frequency.setValueAtTime(75, now);
  osc.frequency.exponentialRampToValueAtTime(16, now + 2.4);
  gain.gain.setValueAtTime(1.2 * volumenMaster, now);
  gain.gain.exponentialRampToValueAtTime(0.001, now + 2.5);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start(now);
  osc.stop(now + 2.5);

  const bufSize = audioCtx.sampleRate * 2.2;
  const buffer = audioCtx.createBuffer(1, bufSize, audioCtx.sampleRate);
  const data = buffer.getChannelData(0);
  for (let i = 0; i < bufSize; i++) data[i] = Math.random() * 2 - 1;
  const ruido = audioCtx.createBufferSource();
  ruido.buffer = buffer;
  const filtro = audioCtx.createBiquadFilter();
  filtro.type = 'lowpass';
  filtro.frequency.setValueAtTime(220, now);
  filtro.frequency.exponentialRampToValueAtTime(28, now + 2.1);
  const gainRuido = audioCtx.createGain();
  gainRuido.gain.setValueAtTime(0.95 * volumenMaster, now);
  gainRuido.gain.exponentialRampToValueAtTime(0.001, now + 2.2);
  ruido.connect(filtro);
  filtro.connect(gainRuido);
  gainRuido.connect(audioCtx.destination);
  ruido.start(now);
}

function setPlay(v) {
  playing = v;
  if (v && audioActivo) {
    initAudio();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    gainFondo.gain.setTargetAtTime(0.55 * volumenMaster, audioCtx.currentTime, 0.25);
  } else if (!v && gainFondo && audioCtx) {
    gainFondo.gain.setTargetAtTime(0.0001, audioCtx.currentTime, 0.1);
  }
}

function stepForward() { playing = false; simTime += 0.5 * escala; radioActual = Math.max(0.08, radioActual + direccion * 0.015 * 0.5 * escala); }
function resetSim() {
  setPlay(false);
  playing = false; simTime = 0; radioActual = 1.0; direccion = 1;
  document.getElementById('sel-ciclo').value = "1"; zoomMacro = 1.0; zoomDetalle = 1.0; ritmoLocal = 1.0;
  document.getElementById('lbl-ritmo-local').innerText = 'x1.0'; selBox = { x0: -0.25, y0: -0.25, x1: 0.25, y1: 0.25 };
}
function formatClock(sec) {
  let s = Math.floor(sec * 45);
  let h = String(Math.floor(s / 3600)).padStart(2, '0');
  let m = String(Math.floor((s % 3600) / 60)).padStart(2, '0');
  let ss = String(s % 60).padStart(2, '0');
  return `${h}:${m}:${ss}`;
}

function getMacroCoords(clientX, clientY) {
  const rect = cMacro.getBoundingClientRect();
  const s = (Math.min(cMacro.width, cMacro.height) * 0.46 * zoomMacro) / Math.max(0.65, radioActual);
  return {
    x: (clientX - rect.left - cMacro.width / 2) / s,
    y: (clientY - rect.top - cMacro.height / 2) / s
  };
}

cMacro.addEventListener('mousedown', e => {
  startDrag = getMacroCoords(e.clientX, e.clientY);
  dragging = true;
});
cMacro.addEventListener('mousemove', e => {
  if (!dragging) return;
  let pos = getMacroCoords(e.clientX, e.clientY);
  if (Math.abs(pos.x - startDrag.x) > 0.03 && Math.abs(pos.y - startDrag.y) > 0.03)
    selBox = { x0: Math.min(startDrag.x, pos.x), y0: Math.min(startDrag.y, pos.y), x1: Math.max(startDrag.x, pos.x), y1: Math.max(startDrag.y, pos.y) };
});
window.addEventListener('mouseup', () => dragging = false);

cMacro.addEventListener('touchstart', e => {
  if (e.touches.length !== 1) return;
  startDrag = getMacroCoords(e.touches[0].clientX, e.touches[0].clientY);
  dragging = true;
}, { passive: true });
cMacro.addEventListener('touchmove', e => {
  if (!dragging || e.touches.length !== 1) return;
  e.preventDefault();
  let pos = getMacroCoords(e.touches[0].clientX, e.touches[0].clientY);
  if (Math.abs(pos.x - startDrag.x) > 0.03 && Math.abs(pos.y - startDrag.y) > 0.03)
    selBox = { x0: Math.min(startDrag.x, pos.x), y0: Math.min(startDrag.y, pos.y), x1: Math.max(startDrag.x, pos.x), y1: Math.max(startDrag.y, pos.y) };
}, { passive: false });
window.addEventListener('touchend', () => dragging = false);

function dibujarGloboOrganico(ctx, nx, ny, rBase, lobulos, fase, simTime) {
  const pts = [];
  for (let k = 0; k < lobulos.length; k++) {
    let ang = (k / lobulos.length) * Math.PI * 2 + fase;
    let rad = rBase * (lobulos[k] + 0.07 * Math.sin(simTime * 1.8 + k));
    pts.push({ x: nx + rad * Math.cos(ang), y: ny + rad * Math.sin(ang) });
  }
  ctx.beginPath();
  for (let k = 0; k < pts.length; k++) {
    let p1 = pts[k], p2 = pts[(k + 1) % pts.length];
    let mx = (p1.x + p2.x) / 2, my = (p1.y + p2.y) / 2;
    if (k === 0) ctx.moveTo((pts[pts.length-1].x + p1.x)/2, (pts[pts.length-1].y + p1.y)/2);
    ctx.quadraticCurveTo(p1.x, p1.y, mx, my);
  }
  ctx.closePath();
}

function renderUniverse(ctx, w, h, scalePx, offX, offY, isZoom) {
  ctx.clearRect(0, 0, w, h); ctx.save(); ctx.translate(offX, offY);
  const R = radioActual;
  const desint = R < 0.45 ? Math.min(1, (0.45 - R) / 0.37) : 0;

  let grad = ctx.createRadialGradient(-R*scalePx*0.22, -R*scalePx*0.22, R*scalePx*0.05, 0, 0, R*scalePx);
  grad.addColorStop(0, desint > 0.5 ? 'rgba(251, 146, 60, 0.25)' : 'rgba(15, 28, 54, 0.32)');
  grad.addColorStop(0.75, 'rgba(10, 18, 36, 0.22)');
  grad.addColorStop(0.95, 'rgba(56, 189, 248, 0.14)');
  grad.addColorStop(1, 'rgba(125, 211, 252, 0.02)');
  ctx.beginPath(); ctx.arc(0, 0, R * scalePx, 0, Math.PI*2); ctx.fillStyle = grad; ctx.fill();
  ctx.lineWidth = 1.2; ctx.strokeStyle = 'rgba(125, 211, 252, 0.24)'; ctx.stroke();

  ctx.beginPath(); ctx.arc(0, 0, 1.0 * scalePx, 0, Math.PI*2);
  ctx.setLineDash([5, 5]); ctx.strokeStyle = 'rgba(148, 163, 184, 0.28)'; ctx.lineWidth = 1; ctx.stroke(); ctx.setLineDash([]);

  focosGas.forEach(f => {
    let fx = f.x * R * scalePx, fy = f.y * R * scalePx;
    for (let k = 1; k <= 12; k++) {
      let rw = ((k * 0.026) * R + (simTime * 0.04) % (0.026 * R)) * scalePx;
      let alpha = (0.34 + 0.3 * desint) * (1 - k / 13);
      ctx.beginPath(); ctx.arc(fx, fy, rw, f.ang - 0.8, f.ang + 0.8);
      ctx.strokeStyle = desint > 0.6 ? `rgba(251, 146, 60, ${alpha})` : `rgba(${f.col}, ${alpha})`;
      ctx.lineWidth = isZoom ? 2.1 : 1.3; ctx.stroke();
    }
  });
  if (desint < 0.85) {
    enlaces.forEach(e => {
      let n1 = nodos[e.i], n2 = nodos[e.j];
      let x1 = n1.bx * R * scalePx, y1 = n1.by * R * scalePx, x2 = n2.bx * R * scalePx, y2 = n2.by * R * scalePx;
      let pulsoAncho = 0.7 + 0.5 * Math.sin(simTime * 1.5 + e.faseFluc);
      ctx.save(); ctx.globalAlpha = (1 - desint);
      if (e.rotura && R > 1.12) {
        [0.26, 0.74].forEach(pos => {
          let gx = x1 + (x2 - x1) * pos, gy = y1 + (y2 - y1) * pos, ang = Math.atan2(y2 - y1, x2 - x1);
          ctx.save(); ctx.translate(gx, gy); ctx.rotate(ang);
          ctx.beginPath(); ctx.ellipse(0, 0, Math.hypot(x2-x1, y2-y1)*0.18, (isZoom ? 0.018*scalePx : 2.8)*pulsoAncho, 0, 0, Math.PI*2);
          ctx.fillStyle = 'rgba(203, 213, 225, 0.25)'; ctx.fill(); ctx.restore();
        });
      } else {
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
        ctx.lineWidth = (isZoom ? 0.032 * scalePx : 4.2) * pulsoAncho;
        ctx.strokeStyle = 'rgba(148, 163, 184, 0.16)'; ctx.lineCap = 'round'; ctx.stroke();
      }
      e.granos.forEach(g => {
        if (e.rotura && R > 1.12 && g.t > 0.38 && g.t < 0.62) return;
        let gx = x1 + (x2 - x1) * g.t - (y2 - y1) * g.off * pulsoAncho;
        let gy = y1 + (y2 - y1) * g.t + (x2 - x1) * g.off * pulsoAncho;
        ctx.beginPath(); ctx.arc(gx, gy, isZoom ? g.sz * 1.4 : g.sz * 0.7, 0, Math.PI*2);
        ctx.fillStyle = 'rgba(254, 240, 138, 0.78)'; ctx.fill();
      });
      ctx.restore();
    });
  }

  burbujasSueltas.forEach(b => {
    let bx = (b.bx + Math.sin(simTime * 0.3 + b.fase) * 0.03) * R * scalePx;
    let by = (b.by + Math.cos(simTime * 0.3 + b.fase) * 0.03) * R * scalePx;
    let rb = 0.026 * scalePx * (1 - desint * 0.7);
    dibujarGloboOrganico(ctx, bx, by, rb, b.lobulos, b.fase, simTime);
    ctx.fillStyle = `rgba(203, 213, 225, ${0.24 * (1 - desint)})`; ctx.fill();
    ctx.beginPath(); ctx.arc(bx, by, isZoom ? 2.4 : 1.3, 0, Math.PI*2);
    ctx.fillStyle = desint > 0.5 ? '#fb923c' : '#fef08a'; ctx.fill();
  });

  nodos.forEach(n => {
    let nx = n.bx * R * scalePx, ny = n.by * R * scalePx, rBase = (0.060 * n.masa) * scalePx * (1 - desint * 0.6);
    dibujarGloboOrganico(ctx, nx, ny, rBase, n.lobulos, n.fase, simTime);
    let gMO = ctx.createRadialGradient(nx, ny, rBase * 0.1, nx, ny, rBase * 1.15);
    gMO.addColorStop(0, `rgba(203, 213, 225, ${0.34 * (1 - desint)})`); gMO.addColorStop(1, 'rgba(148, 163, 184, 0.02)');
    ctx.fillStyle = gMO; ctx.fill();

    n.puntosMO.forEach(p => {
      ctx.beginPath(); ctx.arc(nx + p.dx * rBase, ny + p.dy * rBase, isZoom ? p.sz * 1.1 : p.sz * 0.5, 0, Math.PI*2);
      ctx.fillStyle = `rgba(226, 232, 240, ${0.42 * (1 - desint)})`; ctx.fill();
    });

    if (isZoom && desint < 0.75) {
      ctx.save(); ctx.translate(nx, ny); ctx.rotate(simTime * ritmoLocal * 1.1 + n.fase);
      n.estrellasGal.forEach(st => {
        let sx = st.rad * rBase * 0.85 * Math.cos(st.ang), sy = st.rad * rBase * 0.85 * Math.sin(st.ang);
        ctx.beginPath(); ctx.arc(sx, sy, st.sz * 1.25, 0, Math.PI*2); ctx.fillStyle = st.col; ctx.fill();
      });
      if (n.masa > 1.5) {
        let rBH = Math.max(8, rBase * 0.16);
        let gAcc = ctx.createRadialGradient(0, 0, rBH * 0.7, 0, 0, rBH * 2.4);
        gAcc.addColorStop(0, 'rgba(251, 146, 60, 0.95)'); gAcc.addColorStop(0.5, 'rgba(239, 68, 68, 0.55)'); gAcc.addColorStop(1, 'rgba(239, 68, 68, 0)');
        ctx.beginPath(); ctx.arc(0, 0, rBH * 2.4, 0, Math.PI*2); ctx.fillStyle = gAcc; ctx.fill();
        for (let esp = 0; esp < 3; esp++) {
          ctx.beginPath();
          for (let k = 0; k < 14; k++) {
            let er = rBH * (0.8 + (k / 14) * 1.5), ea = k * 0.45 + esp * 2.09 - simTime * ritmoLocal * 3.5;
            if (k === 0) ctx.moveTo(er * Math.cos(ea), er * Math.sin(ea)); else ctx.lineTo(er * Math.cos(ea), er * Math.sin(ea));
          }
          ctx.strokeStyle = 'rgba(254, 215, 170, 0.85)'; ctx.lineWidth = 1.6; ctx.stroke();
        }
        ctx.beginPath(); ctx.arc(0, 0, rBH, 0, Math.PI*2); ctx.fillStyle = '#000000'; ctx.fill();
        ctx.lineWidth = 1.8; ctx.strokeStyle = '#fb923c'; ctx.stroke();
      }
      ctx.restore();
    } else {
      ctx.beginPath(); ctx.arc(nx, ny, 2.6 * n.masa, 0, Math.PI*2);
      ctx.fillStyle = desint > 0.4 ? '#fb923c' : '#fde047'; ctx.fill();
    }
  });

  neutrinos.forEach(p => {
    let px = (((p.x + p.vx * simTime * 0.25) + 1) % 2 - 1) * R, py = (((p.y + p.vy * simTime * 0.25) + 1) % 2 - 1) * R;
    if (px*px + py*py <= R*R) {
      ctx.beginPath(); ctx.arc(px * scalePx, py * scalePx, isZoom ? 2.6 : 1.6, 0, Math.PI*2);
      ctx.fillStyle = 'rgba(255, 255, 255, 0.88)'; ctx.fill();
    }
  });

  if (!isZoom) {
    ctx.strokeStyle = 'rgba(239, 68, 68, 0.85)';
    ctx.lineWidth = 2;
    ctx.strokeRect(selBox.x0 * scalePx, selBox.y0 * scalePx, (selBox.x1 - selBox.x0) * scalePx, (selBox.y1 - selBox.y0) * scalePx);
  }
  ctx.restore();
}

function loop(ts) {
  if (!lastTs) lastTs = ts;
  let dt = (ts - lastTs) / 1000;
  lastTs = ts;
  if (cMacro.width !== cMacro.clientWidth || cMacro.height !== cMacro.clientHeight) resize();
  if (playing) {
    simTime += dt * escala;
    radioActual += direccion * 0.018 * dt * escala;
    if (radioActual >= 2.50) {
      radioActual = 2.50;
      direccion = -1;
      document.getElementById('sel-ciclo').value = "-1";
    }
    if (radioActual <= 0.04) {
      radioActual = 0.04;
      sonarBigBang();
      direccion = 1;
      document.getElementById('sel-ciclo').value = "1";
    }
  }
  const R = radioActual;
  if (playing && audioActivo && oscFondo && audioCtx) {
    oscFondo.frequency.setTargetAtTime(42 + (2.5 - R) * 18, audioCtx.currentTime, 0.1);
  }
  document.getElementById('reloj').innerText = formatClock(simTime);
  document.getElementById('lbl-radio').innerText = R.toFixed(2) + 'x';
  const elFase = document.getElementById('lbl-fase');
  if (R <= 0.08) elFase.innerText = '💥 ¡REBOTE NÚCLEO MÍNIMO (BIG BANG)!';
  else if (R < 0.45) elFase.innerText = '🔥 Desintegración en Plasma';
  else if (R >= 2.25) elFase.innerText = '⚠️ Gas Agotado — Iniciando Implosión';
  else elFase.innerText = '';

  const baseScaleM = (Math.min(cMacro.width, cMacro.height) * 0.46 * zoomMacro) / Math.max(0.65, R);
  renderUniverse(ctxM, cMacro.width, cMacro.height, baseScaleM, cMacro.width/2, cMacro.height/2, false);

  let boxW = Math.max(0.05, selBox.x1 - selBox.x0), boxH = Math.max(0.05, selBox.y1 - selBox.y0);
  let cx = (selBox.x0 + selBox.x1) / 2, cy = (selBox.y0 + selBox.y1) / 2;
  let scaleZ = Math.min(cZoom.width / boxW, cZoom.height / boxH) * 0.88 * zoomDetalle;
  renderUniverse(ctxZ, cZoom.width, cZoom.height, scaleZ, cZoom.width/2 - cx*scaleZ, cZoom.height/2 - cy*scaleZ, true);

  let minD = 99;
  nodos.forEach(n => { let d = Math.hypot(n.bx * R - cx, n.by * R - cy); if (d < minD) minD = d; });
  const elAgua = document.getElementById('estado-agua');
  elAgua.innerText = minD < 0.14 * R ? '🐢 Agua Tensa (Tiempo Frenado)' : '▶️ Agua Relajada (Tiempo Local)';
  elAgua.style.color = minD < 0.14 * R ? '#fbbf24' : '#34d399';
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
</script>
</body>
</html>
"""
