(function () {
  'use strict';
  const D = window.LOM, $ = id => document.getElementById(id);
  const KEY = { nominal: 'n', ordinal: 'o', interval: 'i', ratio: 'r' };
  const LABEL = { nominal: '名義尺度', ordinal: '順序尺度', interval: '間隔尺度', ratio: '比例尺度' };
  const ORDER = ['nominal', 'ordinal', 'interval', 'ratio'];

  /* ---------- STEP1 ---------- */
  let current = 'nominal';
  function showScale(s) {
    current = s;
    document.querySelectorAll('[data-scale]').forEach(b =>
      b.setAttribute('aria-pressed', b.dataset.scale === s));
    const d = D.scales[s];
    $('sName').textContent = d.name;
    $('sDesc').textContent = d.desc;
    $('sExamples').innerHTML = '<ul>' + d.examples.map(e => '<li>' + e + '</li>').join('') + '</ul>';
    drawOps();
  }
  function drawOps() {
    const k = KEY[current];
    const head = $('opTable').tHead.rows[0];
    ORDER.forEach((s, i) => head.cells[i + 1].className = (s === current ? 'on' : ''));
    const tb = $('opTable').tBodies[0];
    tb.innerHTML = '';
    D.ops.forEach(o => {
      const tr = document.createElement('tr');
      tr.innerHTML = '<td>' + o.op + '</td>' +
        ORDER.map(s => {
          const yes = o[KEY[s]];
          return '<td class="' + (s === current ? 'on ' : '') + (yes ? 'yes' : 'no') + '">' + (yes ? '○' : '×') + '</td>';
        }).join('');
      tb.appendChild(tr);
    });
  }

  /* ---------- STEP2 仕分け ---------- */
  let qList = [], qi = 0, qScore = 0, qMiss = [];
  function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

  function startQuiz() {
    qList = shuffle(D.items).slice(0, 10); qi = 0; qScore = 0; qMiss = [];
    $('reviewBox').hidden = true;
    renderQ();
  }
  function renderQ() {
    if (qi >= qList.length) return finishQuiz();
    const it = qList[qi];
    $('qProgress').textContent = (qi + 1) + ' / ' + qList.length;
    $('qScore').textContent = qScore;
    $('qVar').textContent = it.v;
    $('qSub').textContent = 'この変数はどの尺度水準？';
    const box = $('qChoices');
    box.className = 'choice4';
    box.innerHTML = '';
    ORDER.forEach(s => {
      const b = document.createElement('button');
      b.className = 'btn'; b.textContent = LABEL[s]; b.dataset.s = s;
      b.addEventListener('click', () => answerQ(s));
      box.appendChild(b);
    });
    $('qFb').hidden = true;
    $('qNext').disabled = true;
    $('qNext').textContent = (qi === qList.length - 1) ? '結果を見る' : '次の問題';
  }
  function answerQ(s) {
    const it = qList[qi], ok = s === it.s;
    const box = $('qChoices');
    box.classList.add('locked');
    [...box.children].forEach(b => {
      if (b.dataset.s === it.s) b.classList.add('correct');
      else if (b.dataset.s === s) b.classList.add('wrong');
    });
    if (ok) qScore++; else qMiss.push(it);
    const fb = $('qFb');
    fb.className = 'note ' + (ok ? 'ok' : 'ng');
    fb.innerHTML = (ok ? '正解。' : '正解は <strong>' + LABEL[it.s] + '</strong>。') + it.why;
    fb.hidden = false;
    $('qScore').textContent = qScore;
    $('qNext').disabled = false;
  }
  function finishQuiz() {
    $('qVar').textContent = qScore + ' / ' + qList.length + ' 問正解';
    $('qSub').textContent = qScore === qList.length ? '全問正解です。' :
      (qScore >= qList.length * 0.7 ? 'あと少し。まちがえたところを確認しましょう。' : 'STEP 1 の表に戻って確かめましょう。');
    $('qChoices').innerHTML = '';
    $('qFb').hidden = true;
    $('qNext').disabled = true;
    $('qProgress').textContent = qList.length + ' / ' + qList.length;
    if (qMiss.length) {
      $('reviewBox').hidden = false;
      $('review').innerHTML = qMiss.map(m =>
        '<div class="r-item"><b>' + m.v + ' → ' + LABEL[m.s] + '</b>' + m.why + '</div>').join('');
    }
  }

  /* ---------- STEP3 判定 ---------- */
  let jList = [], ji = 0, jScore = 0;
  function startJudge() { jList = shuffle(D.judges).slice(0, 8); ji = 0; jScore = 0; renderJ(); }
  function renderJ() {
    if (ji >= jList.length) {
      $('jText').textContent = jScore + ' / ' + jList.length + ' 問正解';
      $('jFb').hidden = true; $('jNext').disabled = true;
      $('jOk').disabled = $('jNg').disabled = true;
      $('jProgress').textContent = jList.length + ' / ' + jList.length;
      return;
    }
    $('jProgress').textContent = (ji + 1) + ' / ' + jList.length;
    $('jScore').textContent = jScore;
    $('jText').textContent = jList[ji].t;
    $('jOk').disabled = $('jNg').disabled = false;
    $('jOk').className = $('jNg').className = 'btn';
    $('jFb').hidden = true;
    $('jNext').disabled = true;
    $('jNext').textContent = (ji === jList.length - 1) ? '結果を見る' : '次の問題';
  }
  function answerJ(v) {
    const it = jList[ji], ok = v === it.ok;
    if (ok) jScore++;
    $('jOk').disabled = $('jNg').disabled = true;
    (it.ok ? $('jOk') : $('jNg')).classList.add('correct');
    if (!ok) (v ? $('jOk') : $('jNg')).classList.add('wrong');
    const fb = $('jFb');
    fb.className = 'note ' + (ok ? 'ok' : 'ng');
    fb.innerHTML = (ok ? '正解。' : 'ちがいます。') + it.why;
    fb.hidden = false;
    $('jScore').textContent = jScore;
    $('jNext').disabled = false;
  }

  function init() {
    document.querySelectorAll('[data-scale]').forEach(b =>
      b.addEventListener('click', () => showScale(b.dataset.scale)));
    $('qNext').addEventListener('click', () => { qi++; renderQ(); });
    $('qReset').addEventListener('click', startQuiz);
    $('jOk').addEventListener('click', () => answerJ(true));
    $('jNg').addEventListener('click', () => answerJ(false));
    $('jNext').addEventListener('click', () => { ji++; renderJ(); });
    $('jReset').addEventListener('click', startJudge);
    showScale('nominal');
    startQuiz();
    startJudge();
    if (window.Terms) { window.Terms.glossary(document.getElementById('glossBox'), ["尺度水準", "名義尺度", "順序尺度", "間隔尺度", "比例尺度", "平均値", "中央値", "最頻値", "代表値"]); window.Terms.attach(); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
