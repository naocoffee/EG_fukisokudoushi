import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="不規則動詞シューティング",
    page_icon="🚀",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 0.8rem; padding-bottom: 0.4rem; max-width: 900px; }
    </style>
    <h1 style="text-align:center;color:#00fff2;font-family:'Courier New',monospace;
    text-shadow:0 0 10px #00fff2,0 0 20px #ff00e6;letter-spacing:1px;
    font-size:16px;margin:0 0 3px 0;">
    🚀 IRREGULAR VERB SHOOTER 🚀
    </h1>
    """,
    unsafe_allow_html=True,
)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

  html, body {
    margin: 0;
    padding: 0;
    background: #05010f;
    overflow: hidden;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    touch-action: none;
    overscroll-behavior: none;
  }

  #gameContainer {
    position: relative;
    width: 100%;
    aspect-ratio: 9 / 15;
    margin: 0 auto;
    border: 3px solid #00fff2;
    border-radius: 10px;
    box-shadow: 0 0 25px #00fff2, 0 0 45px #ff00e6 inset;
    background: #05010f;
    font-family: 'Press Start 2P', 'Courier New', monospace;
    user-select: none;
    touch-action: none;
    overflow: hidden;
  }

  #gameCanvas {
    display: block;
    width: 100%;
    height: 100%;
    background: #05010f;
    cursor: crosshair;
    border-radius: 7px;
    touch-action: none;
  }

  .overlay {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(2, 2, 15, 0.88);
    color: #00fff2;
    text-align: center;
    border-radius: 7px;
    z-index: 10;
  }

  .hidden { display: none !important; }

  .title-glow {
    font-size: clamp(15px, 4.2vw, 28px);
    color: #00fff2;
    text-shadow: 0 0 8px #00fff2, 0 0 20px #ff00e6;
    margin-bottom: 22px;
    line-height: 1.6;
    width: 90%;
  }

  .sub-glow {
    font-size: clamp(9px, 2.1vw, 12px);
    color: #ffe14d;
    margin-bottom: 10px;
    line-height: 1.9;
    width: 90%;
  }

  .arcade-btn {
    margin-top: 26px;
    padding: 16px 34px;
    font-family: 'Press Start 2P', 'Courier New', monospace;
    font-size: clamp(11px, 2.6vw, 14px);
    color: #05010f;
    background: linear-gradient(180deg, #00fff2, #00b3ff);
    border: none;
    border-radius: 6px;
    cursor: pointer;
    box-shadow: 0 0 15px #00fff2, 0 0 30px #ff00e6;
    letter-spacing: 2px;
    transition: transform 0.1s ease;
    touch-action: manipulation;
  }
  .arcade-btn:hover { transform: scale(1.08); }
  .arcade-btn:active { transform: scale(0.96); }

  .verb-table {
    font-size: 9px;
    color: #9aa5b1;
    margin-top: 18px;
    line-height: 1.7;
    max-width: 560px;
  }

  .result-score {
    font-size: clamp(14px, 3.6vw, 20px);
    color: #ffe14d;
    margin: 14px 0;
    text-shadow: 0 0 10px #ffe14d;
  }

  #shakeWrap {
    width: 100%;
    max-width: 380px;
    margin: 0 auto;
  }
</style>
</head>
<body>

<div id="shakeWrap">
<div id="gameContainer">
  <canvas id="gameCanvas" width="450" height="750" tabindex="0"></canvas>

  <!-- START SCREEN -->
  <div id="startScreen" class="overlay">
    <div class="title-glow">🚀 IRREGULAR VERB<br>SHOOTER 🚀</div>
    <div class="sub-glow">
      落ちてくる単語の中から<br>
      「過去形」→「過去分詞形」の順に<br>
      正しいターゲットを撃ち抜け！<br><br>
      画面をドラッグして自機を移動<br>
      タップで発射<br>
      ライフは5つ。間違ったターゲットを撃つと-1！
    </div>
    <button class="arcade-btn" id="startBtn">PUSH START</button>
  </div>

  <!-- GAME OVER SCREEN -->
  <div id="gameOverScreen" class="overlay hidden">
    <div class="title-glow" style="color:#ff2b6b;text-shadow:0 0 8px #ff2b6b,0 0 20px #ff00e6;">GAME OVER</div>
    <div class="result-score" id="finalScoreGO">SCORE: 0</div>
    <div class="sub-glow" id="clearedCountGO">CLEARED: 0 / 14</div>
    <button class="arcade-btn" id="retryBtnGO">RETRY</button>
  </div>

  <!-- CLEAR SCREEN -->
  <div id="clearScreen" class="overlay hidden">
    <div class="title-glow" style="color:#00ff88;text-shadow:0 0 8px #00ff88,0 0 20px #00fff2;">🎉 ALL CLEAR! 🎉</div>
    <div class="result-score" id="finalScoreCL">SCORE: 0</div>
    <div class="sub-glow">14種類の不規則動詞をすべて撃破した！</div>
    <button class="arcade-btn" id="retryBtnCL">RETRY</button>
  </div>

</div>
</div>

<script>
(function() {
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const shakeWrap = document.getElementById('shakeWrap');

  // ---------------------------------------------------------
  // Verb data (14 irregular verbs required by spec)
  // ---------------------------------------------------------
  const VERBS = [
    { mean: "話す",       base: "speak", past: "spoke", pp: "spoken",  ppAlt: null   },
    { mean: "書く",       base: "write", past: "wrote", pp: "written", ppAlt: null   },
    { mean: "与える",     base: "give",  past: "gave",  pp: "given",   ppAlt: null   },
    { mean: "取る",       base: "take",  past: "took",  pp: "taken",   ppAlt: null   },
    { mean: "壊す",       base: "break", past: "broke", pp: "broken",  ppAlt: null   },
    { mean: "食べる",     base: "eat",   past: "ate",   pp: "eaten",   ppAlt: null   },
    { mean: "見る",       base: "see",   past: "saw",   pp: "seen",    ppAlt: null   },
    { mean: "手に入れる", base: "get",   past: "got",   pp: "gotten",  ppAlt: null   },
    { mean: "行く",       base: "go",    past: "went",  pp: "gone",    ppAlt: null   },
    { mean: "始める",     base: "begin", past: "began", pp: "begun",   ppAlt: null   },
    { mean: "飲む",       base: "drink", past: "drank", pp: "drunk",   ppAlt: null   },
    { mean: "着ている",   base: "wear",  past: "wore",  pp: "worn",    ppAlt: null   },
    { mean: "横たわる",   base: "lie",   past: "lay",   pp: "lain",    ppAlt: null   },
    { mean: "知っている", base: "know",  past: "knew",  pp: "known",   ppAlt: null   },
  ];

  const MAX_LIFE = 5;
  const MAX_TARGETS = 8;

  // Lane layout: targets fall straight down inside one of these fixed
  // vertical lanes so their x position never drifts into a neighboring
  // target's path. This is what prevents pieces from overlapping.
  const LANE_COUNT = 4;
  const LANE_WIDTH = W / LANE_COUNT;
  const LANE_MIN_GAP = 240; // required vertical spacing before a lane can spawn again
  function laneCenterX(i) { return LANE_WIDTH * (i + 0.5); }

  // The ship is no longer pinned to the bottom edge - it can be dragged
  // anywhere inside this vertical band (kept clear of the top HUD banner).
  const PLAYER_Y_MIN = 122;
  const PLAYER_Y_MAX = H - 20;

  let state = 'start'; // start | playing | gameover | clear
  let verbOrder = [];
  let verbPtr = 0;
  let currentStage = 'past'; // 'past' or 'pp'
  let life = MAX_LIFE;
  let score = 0;
  let clearedCount = 0;
  let lastTimeTick = 0;
  let lastCorrectSeenAt = 0;
  let lastRandomWord = null;

  let targets = [];
  let bullets = [];
  let particles = [];
  let stars = [];
  let shakeFrames = 0;

  let player = { x: W / 2, y: H - 70, w: 40, h: 26, speed: 6 };
  let keys = { left: false, right: false, up: false, down: false };
  let shootCooldown = 0;
  let flame = 0;

  // ---------------------------------------------------------
  // Audio (simple WebAudio beeps, no external files)
  // ---------------------------------------------------------
  let audioCtx = null;
  function beep(freq, dur, type, vol) {
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = type || 'square';
      osc.frequency.value = freq;
      gain.gain.value = vol !== undefined ? vol : 0.08;
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + dur);
      osc.stop(audioCtx.currentTime + dur);
    } catch (e) { /* audio not available, ignore */ }
  }
  function sfxShoot()   { beep(880, 0.08, 'square', 0.05); }
  function sfxCorrect() { beep(1200, 0.12, 'triangle', 0.09); beep(1600, 0.15, 'triangle', 0.07); }
  function sfxWrong()   { beep(120, 0.25, 'sawtooth', 0.1); }
  function sfxClearVerb(){ beep(700,0.08,'square',0.07); beep(1000,0.08,'square',0.07); beep(1400,0.14,'square',0.08); }
  function sfxLifeLost(){ beep(200, 0.3, 'sawtooth', 0.12); }

  // ---------------------------------------------------------
  // Init / reset
  // ---------------------------------------------------------
  function shuffledIndices(n) {
    const arr = Array.from({length: n}, (_, i) => i);
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function initStars() {
    stars = [];
    for (let i = 0; i < 90; i++) {
      stars.push({
        x: Math.random() * W,
        y: Math.random() * H,
        r: Math.random() * 1.6 + 0.4,
        speed: Math.random() * 0.6 + 0.15,
      });
    }
  }

  function resetGame() {
    verbOrder = shuffledIndices(VERBS.length);
    verbPtr = 0;
    currentStage = 'past';
    life = MAX_LIFE;
    score = 0;
    clearedCount = 0;
    targets = [];
    bullets = [];
    particles = [];
    player.x = W / 2;
    player.y = H - 70;
    shakeFrames = 0;
    lastCorrectSeenAt = performance.now();
    lastRandomWord = null;
    initStars();
  }

  function currentVerb() { return VERBS[verbOrder[verbPtr]]; }

  // ---------------------------------------------------------
  // Targets
  // ---------------------------------------------------------
  function wordForForm(verb, form) {
    if (form === 'pp' && verb.ppAlt && Math.random() < 0.5) return verb.ppAlt;
    return verb[form];
  }

  function isAcceptable(target) {
    // true if shooting this target is the CORRECT action right now
    if (target.verbIdx !== verbOrder[verbPtr]) return false;
    if (target.form !== currentStage) return false;
    return true;
  }

  function laneTopMostY(laneIdx) {
    const inLane = targets.filter(t => t.lane === laneIdx);
    if (inLane.length === 0) return Infinity;
    return Math.min(...inLane.map(t => t.y));
  }

  function laneSpeed(laneIdx, freshSpeed) {
    // If the lane already has a falling target, the new one must inherit
    // its speed (the slowest one present) so it can never catch up and
    // collide with it later - only an empty lane gets a fresh random speed.
    const inLane = targets.filter(t => t.lane === laneIdx);
    if (inLane.length === 0) return freshSpeed;
    return Math.min(...inLane.map(t => t.speed));
  }

  function pickLane(forceCorrect) {
    const roomy = [];
    for (let i = 0; i < LANE_COUNT; i++) {
      if (laneTopMostY(i) > LANE_MIN_GAP) roomy.push(i);
    }
    if (roomy.length > 0) return roomy[Math.floor(Math.random() * roomy.length)];
    if (!forceCorrect) return null; // no lane has room yet - just wait for the next spawn tick
    // forced spawn (the needed word has been missing too long): pick whichever
    // lane currently has the most vertical clearance so it still doesn't overlap
    let best = 0, bestY = -Infinity;
    for (let i = 0; i < LANE_COUNT; i++) {
      const y = laneTopMostY(i);
      if (y > bestY) { bestY = y; best = i; }
    }
    return best;
  }

  function spawnTarget(forceCorrect) {
    if (targets.length >= MAX_TARGETS) return;
    const lane = pickLane(forceCorrect);
    if (lane === null) return;

    let verbIdx, form, word;
    if (forceCorrect) {
      verbIdx = verbOrder[verbPtr];
      form = currentStage;
      word = wordForForm(VERBS[verbIdx], form);
    } else {
      // pick a random word, but reroll a few times if it repeats the
      // previous random spawn so the sequence never feels patterned
      let tries = 0;
      do {
        verbIdx = Math.floor(Math.random() * VERBS.length);
        form = Math.random() < 0.5 ? 'past' : 'pp';
        word = wordForForm(VERBS[verbIdx], form);
        tries++;
      } while (word === lastRandomWord && tries < 5);
      lastRandomWord = word;
    }
    const hues = [190, 320, 45, 270, 150];
    // speed is scaled up for the taller 9:20 canvas so the fall time (in
    // seconds) feels the same as on the old, shorter layout
    const freshSpeed = 1.08 + Math.random() * 0.64 + Math.min(score / 380, 0.87);
    targets.push({
      word: word,
      verbIdx: verbIdx,
      form: form,
      lane: lane,
      x: laneCenterX(lane),
      y: -40,
      r: 28 + Math.min(word.length, 10) * 1.6,
      speed: laneSpeed(lane, freshSpeed),
      hue: hues[Math.floor(Math.random() * hues.length)],
      rot: Math.random() * Math.PI * 2,
      rotSpeed: (Math.random() - 0.5) * 0.02,
      wobble: Math.random() * Math.PI * 2,
      alive: true,
    });
  }

  let spawnTimer = 0;
  function updateSpawning(dtMs) {
    spawnTimer += dtMs;
    const interval = 950;
    if (spawnTimer > interval) {
      spawnTimer = 0;
      spawnTarget(false);
    }
    // guarantee the currently-needed target appears reasonably often
    const hasCorrect = targets.some(t => t.alive && isAcceptable(t));
    if (hasCorrect) {
      lastCorrectSeenAt = performance.now();
    } else if (performance.now() - lastCorrectSeenAt > 3200) {
      spawnTarget(true);
      lastCorrectSeenAt = performance.now();
    }
  }

  // ---------------------------------------------------------
  // Particles / effects
  // ---------------------------------------------------------
  function spawnBurst(x, y, color, count) {
    for (let i = 0; i < count; i++) {
      const ang = Math.random() * Math.PI * 2;
      const spd = 1.5 + Math.random() * 3.5;
      particles.push({
        x, y,
        vx: Math.cos(ang) * spd,
        vy: Math.sin(ang) * spd,
        life: 1,
        decay: 0.02 + Math.random() * 0.02,
        color, size: 2 + Math.random() * 3,
      });
    }
  }

  function triggerShake(frames) { shakeFrames = Math.max(shakeFrames, frames); }

  // ---------------------------------------------------------
  // Player / shooting
  // ---------------------------------------------------------
  function shoot() {
    if (state !== 'playing') return;
    if (shootCooldown > 0) return;
    shootCooldown = 16;
    bullets.push({ x: player.x, y: player.y - 22, speed: 10 });
    sfxShoot();
    flame = 8;
  }

  function hitTarget(target, bulletX, bulletY) {
    target.alive = false;
    targets = targets.filter(t => t !== target);

    if (isAcceptable(target)) {
      score += 10;
      spawnBurst(bulletX, bulletY, '#00ff88', 26);
      sfxCorrect();
      if (currentStage === 'past') {
        currentStage = 'pp';
      } else {
        // full verb cleared
        score += 50;
        clearedCount += 1;
        sfxClearVerb();
        verbPtr += 1;
        currentStage = 'past';
        if (verbPtr >= verbOrder.length) {
          endGame('clear');
          return;
        }
      }
      lastCorrectSeenAt = performance.now();
    } else {
      spawnBurst(bulletX, bulletY, '#ff2b6b', 22);
      sfxWrong();
      loseLife();
    }
  }

  function loseLife() {
    life -= 1;
    triggerShake(14);
    sfxLifeLost();
    if (life <= 0) {
      endGame('gameover');
    }
  }

  // ---------------------------------------------------------
  // Update loop
  // ---------------------------------------------------------
  function update(dtMs) {
    // player movement (free 2D movement - keyboard fallback for desktop testing)
    if (keys.left) player.x -= player.speed;
    if (keys.right) player.x += player.speed;
    if (keys.up) player.y -= player.speed;
    if (keys.down) player.y += player.speed;
    player.x = Math.max(player.w / 2 + 4, Math.min(W - player.w / 2 - 4, player.x));
    player.y = Math.max(PLAYER_Y_MIN, Math.min(PLAYER_Y_MAX, player.y));

    if (shootCooldown > 0) shootCooldown -= 1;
    if (flame > 0) flame -= 1;

    // bullets
    bullets.forEach(b => b.y -= b.speed);
    bullets = bullets.filter(b => b.y > -20);

    // targets
    targets.forEach(t => {
      t.y += t.speed;
      t.rot += t.rotSpeed;
      t.wobble += 0.05;
    });

    // bullet-target collisions
    for (const b of bullets.slice()) {
      for (const t of targets.slice()) {
        const dx = b.x - t.x, dy = b.y - t.y;
        if (Math.sqrt(dx * dx + dy * dy) < t.r) {
          bullets = bullets.filter(x => x !== b);
          hitTarget(t, b.x, b.y);
          break;
        }
      }
    }

    // targets falling off bottom - no longer costs a life, even if it was
    // the currently-needed correct target; it's just removed (with a small
    // neutral puff so a miss is still visible) and a new one keeps spawning.
    for (const t of targets.slice()) {
      if (t.y - t.r > H) {
        targets = targets.filter(x => x !== t);
        if (isAcceptable(t)) {
          spawnBurst(t.x, H - 10, '#9aa5b1', 12);
        }
      }
    }

    // particles
    particles.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      p.vy += 0.03;
      p.life -= p.decay;
    });
    particles = particles.filter(p => p.life > 0);

    if (shakeFrames > 0) shakeFrames -= 1;

    updateSpawning(dtMs);

    stars.forEach(s => {
      s.y += s.speed;
      if (s.y > H) { s.y = 0; s.x = Math.random() * W; }
    });
  }

  // ---------------------------------------------------------
  // Draw
  // ---------------------------------------------------------
  function drawBackground() {
    const g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, '#0b0330');
    g.addColorStop(1, '#05010f');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#ffffff';
    stars.forEach(s => {
      ctx.globalAlpha = 0.5 + Math.sin(s.y * 0.05) * 0.3;
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.globalAlpha = 1;
  }

  function drawPlayer() {
    ctx.save();
    ctx.translate(player.x, player.y);
    ctx.shadowColor = '#00fff2';
    ctx.shadowBlur = 16;
    ctx.fillStyle = '#00fff2';
    ctx.beginPath();
    ctx.moveTo(0, -player.h);
    ctx.lineTo(player.w / 2, player.h / 2);
    ctx.lineTo(player.w / 4, player.h / 3);
    ctx.lineTo(-player.w / 4, player.h / 3);
    ctx.lineTo(-player.w / 2, player.h / 2);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#ff00e6';
    ctx.beginPath();
    ctx.arc(0, -player.h * 0.25, 5, 0, Math.PI * 2);
    ctx.fill();
    if (flame > 0) {
      ctx.fillStyle = `rgba(255, ${150 + Math.random()*80|0}, 60, ${flame/8})`;
      ctx.beginPath();
      ctx.moveTo(-8, player.h / 2);
      ctx.lineTo(0, player.h / 2 + 10 + Math.random() * 8);
      ctx.lineTo(8, player.h / 2);
      ctx.closePath();
      ctx.fill();
    }
    ctx.restore();
  }

  function drawBullets() {
    ctx.fillStyle = '#ffe14d';
    ctx.shadowColor = '#ffe14d';
    ctx.shadowBlur = 10;
    bullets.forEach(b => {
      ctx.beginPath();
      ctx.ellipse(b.x, b.y, 3, 10, 0, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.shadowBlur = 0;
  }

  function drawTargets() {
    targets.forEach(t => {
      ctx.save();
      ctx.translate(t.x, t.y + Math.sin(t.wobble) * 3);
      ctx.rotate(t.rot);
      const grad = ctx.createRadialGradient(0, 0, t.r * 0.2, 0, 0, t.r);
      grad.addColorStop(0, '#ffffff');
      grad.addColorStop(1, '#dcdcdc');
      ctx.fillStyle = grad;
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.shadowColor = `hsl(${t.hue}, 100%, 60%)`;
      ctx.shadowBlur = 12;
      ctx.beginPath();
      const spikes = 9;
      for (let i = 0; i < spikes; i++) {
        const ang = (i / spikes) * Math.PI * 2;
        const rr = t.r * (0.82 + 0.18 * Math.sin(i * 2.3 + t.hue));
        const px = Math.cos(ang) * rr, py = Math.sin(ang) * rr;
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
      ctx.restore();

      ctx.shadowBlur = 0;
      ctx.globalAlpha = 1;
      ctx.fillStyle = '#000000';
      ctx.font = 'bold 16px Arial, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      const ty = t.y + Math.sin(t.wobble) * 3;
      ctx.fillText(t.word, t.x, ty);
    });
  }

  function drawParticles() {
    particles.forEach(p => {
      ctx.globalAlpha = Math.max(p.life, 0);
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.globalAlpha = 1;
  }

  function drawHUD() {
    if (state !== 'playing') return;
    const verb = currentVerb();

    // top banner
    ctx.textAlign = 'center';
    ctx.fillStyle = 'rgba(0,0,0,0.35)';
    ctx.fillRect(0, 0, W, 104);

    ctx.font = 'bold 26.4px "Courier New", monospace';
    ctx.fillStyle = '#ffe14d';
    ctx.shadowColor = '#ffe14d';
    ctx.shadowBlur = 10;
    ctx.fillText(verb.mean + '  ( ' + verb.base + ' )', W / 2, 54);
    ctx.shadowBlur = 0;

    ctx.font = 'bold 22.1px "Courier New", monospace';
    ctx.fillStyle = currentStage === 'past' ? '#00fff2' : '#ff8bd1';
    const stageLabel = currentStage === 'past'
      ? '▶ 過去形 (Past) を撃て！'
      : '▶ 過去分詞形 (PP) を撃て！';
    ctx.fillText(stageLabel, W / 2, 90);

    // lives (hearts) top-left
    ctx.textAlign = 'left';
    for (let i = 0; i < MAX_LIFE; i++) {
      ctx.font = '22px Arial';
      ctx.fillStyle = i < life ? '#ff2b6b' : 'rgba(255,255,255,0.15)';
      ctx.fillText('♥', 16 + i * 28, 24);
    }

    // score / cleared top-right
    ctx.textAlign = 'right';
    ctx.font = '13px "Courier New", monospace';
    ctx.fillStyle = '#00fff2';
    ctx.fillText('SCORE ' + score, W - 14, 20);
    ctx.fillStyle = '#9aa5b1';
    ctx.fillText('CLEARED ' + clearedCount + ' / ' + VERBS.length, W - 14, 38);
  }

  function render() {
    ctx.save();
    if (shakeFrames > 0) {
      const dx = (Math.random() - 0.5) * 8;
      const dy = (Math.random() - 0.5) * 8;
      ctx.translate(dx, dy);
    }
    drawBackground();
    if (state === 'playing') {
      drawTargets();
      drawPlayer();
      drawBullets();
    }
    drawParticles();
    drawHUD();
    ctx.restore();
  }

  // ---------------------------------------------------------
  // State transitions
  // ---------------------------------------------------------
  function showScreen(id) {
    ['startScreen', 'gameOverScreen', 'clearScreen'].forEach(sid => {
      document.getElementById(sid).classList.toggle('hidden', sid !== id);
    });
  }

  function startGame() {
    resetGame();
    state = 'playing';
    showScreen(null);
    document.getElementById('startScreen').classList.add('hidden');
    document.getElementById('gameOverScreen').classList.add('hidden');
    document.getElementById('clearScreen').classList.add('hidden');
    canvas.focus();
  }

  function endGame(kind) {
    state = kind;
    if (kind === 'gameover') {
      document.getElementById('finalScoreGO').textContent = 'SCORE: ' + score;
      document.getElementById('clearedCountGO').textContent = 'CLEARED: ' + clearedCount + ' / ' + VERBS.length;
      document.getElementById('gameOverScreen').classList.remove('hidden');
    } else if (kind === 'clear') {
      score += 300; // full-clear bonus
      document.getElementById('finalScoreCL').textContent = 'SCORE: ' + score;
      document.getElementById('clearScreen').classList.remove('hidden');
    }
  }

  // ---------------------------------------------------------
  // Input handling
  // ---------------------------------------------------------
  document.getElementById('startBtn').addEventListener('click', startGame);
  document.getElementById('retryBtnGO').addEventListener('click', startGame);
  document.getElementById('retryBtnCL').addEventListener('click', startGame);

  window.addEventListener('keydown', (e) => {
    if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', ' ', 'Spacebar'].includes(e.key)) e.preventDefault();
    if (e.key === 'ArrowLeft') keys.left = true;
    if (e.key === 'ArrowRight') keys.right = true;
    if (e.key === 'ArrowUp') keys.up = true;
    if (e.key === 'ArrowDown') keys.down = true;
    if (e.key === ' ' || e.key === 'Spacebar') shoot();
  });
  window.addEventListener('keyup', (e) => {
    if (e.key === 'ArrowLeft') keys.left = false;
    if (e.key === 'ArrowRight') keys.right = false;
    if (e.key === 'ArrowUp') keys.up = false;
    if (e.key === 'ArrowDown') keys.down = false;
  });

  canvas.addEventListener('mousemove', (e) => {
    if (state !== 'playing') return;
    const rect = canvas.getBoundingClientRect();
    const scaleX = W / rect.width;
    const scaleY = H / rect.height;
    player.x = Math.max(player.w / 2 + 4, Math.min(W - player.w / 2 - 4, (e.clientX - rect.left) * scaleX));
    player.y = Math.max(PLAYER_Y_MIN, Math.min(PLAYER_Y_MAX, (e.clientY - rect.top) * scaleY));
  });
  canvas.addEventListener('mousedown', () => { shoot(); });
  canvas.addEventListener('click', () => canvas.focus());

  document.getElementById('gameContainer').addEventListener('click', () => canvas.focus());
  window.addEventListener('load', () => canvas.focus());

  // ---------------------------------------------------------
  // Touch controls (smartphone / tablet support)
  // Drag anywhere on the canvas to move the ship. A tap (touch down and
  // up again without dragging past TAP_MOVE_THRESHOLD) fires one shot.
  // ---------------------------------------------------------
  const TAP_MOVE_THRESHOLD = 12; // CSS px of finger travel before it counts as a drag, not a tap
  let touchStartX = 0, touchStartY = 0, touchDragged = false;

  function updateTouchAim(e) {
    const touch = e.touches[0] || e.changedTouches[0];
    if (!touch) return;
    const rect = canvas.getBoundingClientRect();
    const scaleX = W / rect.width;
    const scaleY = H / rect.height;
    player.x = Math.max(player.w / 2 + 4, Math.min(W - player.w / 2 - 4, (touch.clientX - rect.left) * scaleX));
    player.y = Math.max(PLAYER_Y_MIN, Math.min(PLAYER_Y_MAX, (touch.clientY - rect.top) * scaleY));
  }

  canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    canvas.focus();
    if (state !== 'playing') return;
    const touch = e.touches[0];
    touchStartX = touch.clientX;
    touchStartY = touch.clientY;
    touchDragged = false;
    updateTouchAim(e);
  }, { passive: false });

  canvas.addEventListener('touchmove', (e) => {
    e.preventDefault();
    if (state !== 'playing') return;
    const touch = e.touches[0];
    const dx = touch.clientX - touchStartX;
    const dy = touch.clientY - touchStartY;
    if (Math.sqrt(dx * dx + dy * dy) > TAP_MOVE_THRESHOLD) touchDragged = true;
    updateTouchAim(e);
  }, { passive: false });

  canvas.addEventListener('touchend', (e) => {
    e.preventDefault();
    if (state === 'playing' && !touchDragged) shoot();
    touchDragged = false;
  }, { passive: false });

  canvas.addEventListener('touchcancel', (e) => {
    touchDragged = false;
  }, { passive: false });

  // ---------------------------------------------------------
  // Main loop
  // ---------------------------------------------------------
  function loop(ts) {
    if (!lastTimeTick) lastTimeTick = ts;
    const dtMs = Math.min(ts - lastTimeTick, 50);
    lastTimeTick = ts;

    if (state === 'playing') update(dtMs);
    else {
      stars.forEach(s => { s.y += s.speed * 0.4; if (s.y > H) { s.y = 0; s.x = Math.random() * W; } });
    }
    render();
    requestAnimationFrame(loop);
  }

  initStars();
  render();
  requestAnimationFrame(loop);
})();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=650, scrolling=False)

st.markdown(
    """
    <div style="text-align:center;color:#555;font-family:'Courier New',monospace;font-size:10px;margin-top:4px;">
    Tips: 画面をドラッグして移動、タップで発射します。
    </div>
    """,
    unsafe_allow_html=True,
)