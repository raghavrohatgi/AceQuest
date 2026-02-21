// ── Config ──
const API_BASE = window.location.hostname === 'localhost'
  ? 'http://localhost:8080'
  : 'https://ari-acequest.fly.dev';

const IS_LOCALHOST = window.location.hostname === 'localhost' ||
                     window.location.hostname === '127.0.0.1';

// ── State ──
let state = {
  text: '',
  subject: 'English',
  ari: null,
  teacherGrade: null,
  turnstileToken: null,
  npsScore: null,
  feedbackId: null,
};

// ── Turnstile ──
let _turnstileWidgetId = null;

function onTurnstileLoad() {
  // Script ready — widget rendered when rating card is shown
}

function renderTurnstile() {
  if (IS_LOCALHOST || !window.turnstile) return;
  if (_turnstileWidgetId !== null) {
    try { window.turnstile.remove(_turnstileWidgetId); } catch(e) {}
    _turnstileWidgetId = null;
  }
  document.getElementById('turnstile-container').innerHTML = '';
  _turnstileWidgetId = window.turnstile.render('#turnstile-container', {
    sitekey: '0x4AAAAAACfwc5dvbP3OGmXs',
    theme: 'light',
    callback: function(token) {
      state.turnstileToken = token;
      updateSubmitBtn();
    },
    'expired-callback': function() {
      state.turnstileToken = null;
      updateSubmitBtn();
    },
  });
}

// ── Step indicators ──
function setStep(n) {
  for (let i = 1; i <= 3; i++) {
    const dot = document.getElementById('dot-' + i);
    if (i < n) { dot.className = 'step-dot done'; dot.textContent = '✓'; }
    else if (i === n) { dot.className = 'step-dot active'; dot.textContent = i; }
    else { dot.className = 'step-dot'; dot.textContent = i; }
  }
  const l12 = document.getElementById('line-1-2');
  const l23 = document.getElementById('line-2-3');
  if (l12) l12.className = 'step-line' + (n > 1 ? ' done' : '');
  if (l23) l23.className = 'step-line' + (n > 2 ? ' done' : '');
}

// ── Passage input ──
function onPassageInput() {
  const text = document.getElementById('passage').value;
  const words = text.trim().split(/\s+/).filter(Boolean).length;
  document.getElementById('word-count').textContent = words + ' words';
  document.getElementById('btn-check').disabled = words < 5;
}

// ── Grade pills ──
function renderPills() {
  const container = document.getElementById('pills');
  container.innerHTML = '';
  for (let g = 1; g <= 10; g++) {
    const d = document.createElement('div');
    d.className = 'pill' + (state.teacherGrade === g ? ' selected' : '');
    d.textContent = g;
    d.onclick = () => selectGrade(g);
    container.appendChild(d);
  }
}

function selectGrade(g) {
  state.teacherGrade = g;
  renderPills();
  updateSubmitBtn();
}

function updateSubmitBtn() {
  const ready = IS_LOCALHOST
    ? state.teacherGrade !== null
    : state.teacherGrade !== null && state.turnstileToken !== null;
  document.getElementById('btn-submit').disabled = !ready;
}

// ── Step 1 → 2: Score the passage ──
async function checkPassage() {
  const text = document.getElementById('passage').value.trim();
  const subject = document.getElementById('subject').value;

  if (!text || text.split(/\s+/).length < 5) return;

  state.text = text;
  state.subject = subject;
  state.teacherGrade = null;
  state.turnstileToken = null;

  const btn = document.getElementById('btn-check');
  btn.disabled = true;
  btn.textContent = 'Analysing…';

  try {
    const resp = await fetch(`${API_BASE}/score`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, subject }),
    });

    if (!resp.ok) {
      const err = await resp.json();
      alert('Error: ' + (err.detail || 'Something went wrong'));
      return;
    }

    state.ari = await resp.json();
    show('card-rate');
    hide('card-input');
    renderPills();
    renderTurnstile();
    setStep(2);
  } catch (e) {
    alert('Could not reach PassageCheck server. Please try again.');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Check Reading Level →';
    if (!document.getElementById('card-input').classList.contains('hidden')) {
      show('card-input');
    }
  }
}

// ── Step 2 → 3: Submit rating ──
async function submitRating() {
  const needsTurnstile = !IS_LOCALHOST && !state.turnstileToken;
  if (!state.teacherGrade || needsTurnstile) return;

  const btn = document.getElementById('btn-submit');
  btn.disabled = true;
  btn.textContent = 'Submitting…';

  try {
    const resp = await fetch(`${API_BASE}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: state.text,
        subject: state.subject,
        ari_grade_mid: state.ari.grade_mid,
        teacher_grade: state.teacherGrade,
        teacher_board: 'CBSE',
        reason: '',
        turnstile_token: state.turnstileToken || 'dev-mode-bypass',
      }),
    });

    if (!resp.ok) {
      const err = await resp.json();
      showMsg('msg-rate', 'error', err.detail || 'Submission failed. Please try again.');
      btn.disabled = false;
      btn.textContent = 'Submit My Rating →';
      return;
    }

    const data = await resp.json();
    state.feedbackId = data.feedback_id || null;
    revealResult();
  } catch (e) {
    showMsg('msg-rate', 'error', 'Network error — please try again.');
    btn.disabled = false;
    btn.textContent = 'Submit My Rating →';
  }
}

// ── Reveal result ──
function revealResult() {
  const { grade_low, grade_mid, grade_high, label } = state.ari;
  const tg = state.teacherGrade;

  document.getElementById('echo-grade').textContent = 'Grade ' + tg;
  document.getElementById('ari-grade').textContent = label;

  const pct = ((grade_high - grade_low + 2) / 10) * 100;
  document.getElementById('bar-fill').style.width = Math.min(pct, 100) + '%';
  document.getElementById('conf-label').textContent =
    `Confidence range: Grade ${grade_low}–${grade_high}`;

  const inRange = tg >= grade_low && tg <= grade_high;
  const agreeEl = document.getElementById('agree-text');
  const stripEl = document.getElementById('agree-strip');
  const iconEl  = document.getElementById('agree-icon');
  const isDuplicate = !state.feedbackId;

  if (inRange) {
    agreeEl.innerHTML = 'Your rating is <strong>within PassageCheck\'s predicted range</strong>. Great — your intuition aligns with the model!';
    stripEl.style.cssText = '';
    iconEl.textContent = '✓';
  } else {
    const extra = isDuplicate ? '' : ' Your expertise matters — please share why below.';
    agreeEl.innerHTML = `Your rating (Grade ${tg}) is <strong>outside PassageCheck's range</strong> (${label}).${extra}`;
    stripEl.style.background = 'var(--amber-lt)';
    stripEl.style.border = '1px solid #FCD34D';
    iconEl.style.background = 'var(--amber)';
    iconEl.textContent = '!';
    if (!isDuplicate) show('disagree-section');
  }

  hide('card-rate');
  show('card-result');

  if (!isDuplicate) {
    state.npsScore = null;
    renderNpsScale();
    setTimeout(() => document.getElementById('nps-panel').classList.add('open'), 600);
  }
  setStep(3);
}

// ── Submit disagree reason ──
async function submitReason() {
  const reason = document.getElementById('disagree-input').value.trim();
  if (!reason) {
    showMsg('msg-reason', 'error', 'Please enter a reason before submitting.');
    return;
  }

  const btn = document.querySelector('#disagree-section .btn-secondary');
  btn.disabled = true;
  btn.textContent = 'Sending…';

  if (!state.feedbackId) {
    showMsg('msg-reason', 'error', 'Could not link feedback. Please try again.');
    btn.disabled = false;
    btn.textContent = 'Send Feedback';
    return;
  }

  try {
    const resp = await fetch(`${API_BASE}/feedback/${state.feedbackId}/reason`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason }),
    });

    if (resp.ok) {
      showMsg('msg-reason', 'success', 'Thank you — your feedback helps improve PassageCheck!');
      btn.textContent = 'Sent ✓';
      document.getElementById('disagree-input').disabled = true;
    } else {
      const err = await resp.json();
      showMsg('msg-reason', 'error', err.detail || 'Failed to send feedback. Please try again.');
      btn.disabled = false;
      btn.textContent = 'Send Feedback';
    }
  } catch (e) {
    showMsg('msg-reason', 'error', 'Network error. Please check your connection and try again.');
    btn.disabled = false;
    btn.textContent = 'Send Feedback';
  }
}

// ── NPS ──
function renderNpsScale() {
  const container = document.getElementById('nps-scale');
  container.innerHTML = '';
  for (let i = 0; i <= 10; i++) {
    const btn = document.createElement('button');
    btn.className = 'nps-btn' + (state.npsScore === i ? ' selected' : '');
    btn.textContent = i;
    btn.onclick = () => {
      state.npsScore = i;
      renderNpsScale();
      document.getElementById('btn-nps').disabled = false;
    };
    container.appendChild(btn);
  }
}

function _slideOutNps() {
  document.getElementById('nps-panel').classList.remove('open');
}

function closeNps() {
  _slideOutNps();
}

async function skipNps() {
  _slideOutNps();
  try {
    await fetch(`${API_BASE}/nps/skip`, { method: 'POST' });
  } catch(e) { /* best-effort */ }
}

function _showNpsThankyou() {
  document.getElementById('nps-comment').disabled = true;
  document.querySelectorAll('.nps-btn').forEach(b => b.disabled = true);
  let secs = 3;
  document.getElementById('nps-body').innerHTML = `
    <div class="nps-thankyou">
      <div class="nps-thankyou-icon">🙏</div>
      <div class="nps-thankyou-text">Thank you for your feedback!</div>
      <div class="nps-thankyou-sub">Your input helps us improve PassageCheck.</div>
      <button class="btn btn-primary" onclick="reset()" style="width:100%; margin-bottom:10px;">← Check Another Passage</button>
      <div class="nps-countdown" id="nps-countdown">Closing in ${secs}s…</div>
    </div>
  `;
  const timer = setInterval(() => {
    secs--;
    const el = document.getElementById('nps-countdown');
    if (!el) { clearInterval(timer); return; }
    if (secs <= 0) {
      clearInterval(timer);
      _slideOutNps();
    } else {
      el.textContent = `Closing in ${secs}s…`;
    }
  }, 1000);
}

async function submitNps() {
  if (state.npsScore === null) return;
  const comment = document.getElementById('nps-comment').value.trim();
  const btn = document.getElementById('btn-nps');
  btn.disabled = true;
  btn.textContent = 'Submitting…';
  try {
    const resp = await fetch(`${API_BASE}/nps`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ score: state.npsScore, comment }),
    });
    if (resp.ok) {
      _showNpsThankyou();
    } else {
      showMsg('msg-nps', 'error', 'Could not save feedback. Please try again.');
      btn.disabled = false;
      btn.textContent = 'Submit Feedback';
    }
  } catch (e) {
    showMsg('msg-nps', 'error', 'Network error. Please try again.');
    btn.disabled = false;
    btn.textContent = 'Submit Feedback';
  }
}

// ── Reset ──
function reset() {
  state = { text:'', subject:'English', ari:null, teacherGrade:null, turnstileToken:null, npsScore:null, feedbackId:null };
  document.getElementById('passage').value = '';
  document.getElementById('word-count').textContent = '0 words';
  document.getElementById('btn-check').disabled = true;

  const disagreeInput = document.getElementById('disagree-input');
  disagreeInput.value = '';
  disagreeInput.disabled = false;

  // Reset NPS panel
  document.getElementById('nps-panel').classList.remove('open');
  document.getElementById('nps-body').innerHTML = `
    <p class="nps-question">How likely are you to recommend PassageCheck to a colleague?</p>
    <div class="nps-scale" id="nps-scale"></div>
    <div class="nps-labels">
      <span>Not likely</span>
      <span>Very likely</span>
    </div>
    <textarea class="nps-comment" id="nps-comment"
      placeholder="What could we improve? (optional)"></textarea>
    <div id="nps-actions">
      <button class="btn btn-primary" id="btn-nps" onclick="submitNps()" disabled style="width:100%;">
        Submit Feedback
      </button>
      <div id="msg-nps" class="hidden" style="margin-top:8px;"></div>
    </div>
    <div class="nps-footer-row">
      <button class="nps-skip" onclick="skipNps()">Skip</button>
    </div>
  `;

  // Reset agree strip styles
  const stripEl = document.getElementById('agree-strip');
  stripEl.style.cssText = '';
  document.getElementById('agree-icon').style.cssText = '';

  hide('card-rate'); hide('card-result'); hide('disagree-section');
  show('card-input');
  setStep(1);

  if (_turnstileWidgetId !== null && window.turnstile) {
    try { window.turnstile.remove(_turnstileWidgetId); } catch(e) {}
    _turnstileWidgetId = null;
  }
  document.getElementById('turnstile-container').innerHTML = '';
}

// ── UI helpers ──
function show(id) { document.getElementById(id).classList.remove('hidden'); }
function hide(id) { document.getElementById(id).classList.add('hidden'); }

function showMsg(id, type, text) {
  const el = document.getElementById(id);
  el.className = 'msg msg-' + type;
  el.textContent = text;
  el.classList.remove('hidden');
}

// ── Initialize ──
if (IS_LOCALHOST) {
  const captchaWrap = document.getElementById('captcha-wrap');
  if (captchaWrap) captchaWrap.style.display = 'none';
}
setStep(1);
