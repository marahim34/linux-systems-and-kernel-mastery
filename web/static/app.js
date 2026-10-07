/**
 * app.js - Linux Mastery Dojo Single-Page Web Engine
 */

let state = {
  challenges: [],
  selectedChallenge: null,
  datasets: {},
  curriculumTree: {},
  progress: null
};

// INITIALIZATION
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  fetchStatus();
  fetchChallenges();
  fetchDatasets();
  fetchCurriculum();
  initSandbox();
  initKernelSim();

  document.getElementById('filter-tier').addEventListener('change', renderChallengeList);
  document.getElementById('filter-cat').addEventListener('change', renderChallengeList);
  document.getElementById('btn-reset-progress').addEventListener('click', resetProgress);
});

// TAB SWITCHING
function initTabs() {
  const tabs = document.querySelectorAll('.nav-item');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const targetId = `tab-${tab.dataset.tab}`;
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      const activePane = document.getElementById(targetId);
      if (activePane) activePane.classList.add('active');
    });
  });
}

// FETCH DATA
async function fetchStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    state.progress = data;
    renderTopBarStats();
    renderBadgesTab();
  } catch (err) {
    console.error('Failed to fetch status:', err);
  }
}

async function fetchChallenges() {
  try {
    const res = await fetch('/api/challenges');
    const data = await res.json();
    state.challenges = data.challenges || [];
    renderChallengeList();
  } catch (err) {
    console.error('Failed to fetch challenges:', err);
  }
}

async function fetchDatasets() {
  try {
    const res = await fetch('/api/practice-files');
    state.datasets = await res.json();
    renderDatasetsTab();
  } catch (err) {
    console.error('Failed to fetch datasets:', err);
  }
}

async function fetchCurriculum() {
  try {
    const res = await fetch('/api/curriculum');
    const data = await res.json();
    state.curriculumTree = data.tree || {};
    renderCurriculumTree();
  } catch (err) {
    console.error('Failed to fetch curriculum:', err);
  }
}

// RENDER TOP BAR
function renderTopBarStats() {
  if (!state.progress) return;
  document.getElementById('stat-rank').textContent = state.progress.rank;
  document.getElementById('stat-completed').textContent = `${state.progress.total_completed} / ${state.progress.total_challenges}`;
  document.getElementById('stat-badges').textContent = `${state.progress.badges.length} 🏆`;
}

// RENDER CHALLENGES LIST
function renderChallengeList() {
  const listEl = document.getElementById('challenge-list');
  const tierFilter = document.getElementById('filter-tier').value;
  const catFilter = document.getElementById('filter-cat').value;

  listEl.innerHTML = '';

  const filtered = state.challenges.filter(c => {
    if (tierFilter && c.tier !== tierFilter) return false;
    if (catFilter && c.category !== catFilter) return false;
    return true;
  });

  filtered.forEach(c => {
    const card = document.createElement('div');
    card.className = `challenge-card ${c.completed ? 'completed' : ''} ${state.selectedChallenge && state.selectedChallenge.id === c.id ? 'active' : ''}`;
    card.onclick = () => selectChallenge(c.id);

    const left = document.createElement('div');
    left.className = 'card-left';
    left.innerHTML = `
      <div class="card-title">${c.title}</div>
      <div class="card-meta">${c.id} · ${c.category.toUpperCase()}</div>
    `;

    const tag = document.createElement('span');
    tag.className = `badge-tag ${c.completed ? 'completed' : 'pending'}`;
    tag.textContent = c.completed ? 'DONE ✓' : 'TODO';

    card.appendChild(left);
    card.appendChild(tag);
    listEl.appendChild(card);
  });
}

// SELECT & DISPLAY CHALLENGE
async function selectChallenge(id) {
  try {
    const res = await fetch(`/api/challenges/${id}`);
    const c = await res.json();
    state.selectedChallenge = c;
    renderChallengeList();

    const detailEl = document.getElementById('challenge-detail');
    detailEl.innerHTML = `
      <div class="challenge-title-row">
        <div>
          <h2>${c.title}</h2>
          <div style="font-family: var(--font-mono); color: var(--text-muted); font-size: 12px; margin-top: 4px;">
            ID: ${c.id} | Tier: ${c.tier.toUpperCase()} | Category: ${c.category.toUpperCase()}
          </div>
        </div>
        <span class="badge-tag ${c.completed ? 'completed' : 'pending'}" style="font-size: 12px; padding: 4px 10px;">
          ${c.completed ? 'COMPLETED ✓' : 'INCOMPLETE'}
        </span>
      </div>

      <div class="challenge-desc-box">
        <strong>Task:</strong> ${c.description}
      </div>

      <div class="workspace-input-section">
        <label style="font-weight: 600; font-size: 13px;">Your Solution Command:</label>
        <textarea id="editor-cmd" class="cmd-editor" placeholder="Enter bash command (e.g. grep ERROR app.log)...">${c.completed && c.user_solution ? c.user_solution : ''}</textarea>
        
        <div class="action-row">
          <button class="btn btn-primary" id="btn-submit-sol">Submit & Verify</button>
          <button class="btn btn-secondary" id="btn-toggle-hint">Hint</button>
          <button class="btn btn-secondary" id="btn-toggle-sol">Reveal Solution</button>
        </div>
      </div>

      <div id="hint-box" style="display: none; background: var(--bg-secondary); border-left: 3px solid var(--accent-yellow); padding: 12px; border-radius: 4px;">
        <strong>Hint:</strong> ${c.hint || 'No hint available.'}
      </div>

      <div id="solution-box" style="display: none; background: var(--bg-secondary); border-left: 3px solid var(--accent-blue); padding: 12px; border-radius: 4px; font-family: var(--font-mono);">
        <strong>Reference Solution:</strong><br>
        <code>${c.solution}</code>
      </div>

      <div id="verification-panel"></div>
    `;

    document.getElementById('btn-submit-sol').onclick = () => submitSolution(c.id);
    document.getElementById('btn-toggle-hint').onclick = () => {
      const hb = document.getElementById('hint-box');
      hb.style.display = hb.style.display === 'none' ? 'block' : 'none';
    };
    document.getElementById('btn-toggle-sol').onclick = () => {
      const sb = document.getElementById('solution-box');
      sb.style.display = sb.style.display === 'none' ? 'block' : 'none';
    };
  } catch (err) {
    console.error('Failed to load challenge details:', err);
  }
}

// SUBMIT CHALLENGE FOR VERIFICATION
async function submitSolution(id) {
  const cmd = document.getElementById('editor-cmd').value.trim();
  if (!cmd) {
    alert('Please enter a command to verify.');
    return;
  }

  const panel = document.getElementById('verification-panel');
  panel.innerHTML = '<div style="color: var(--text-muted); font-family: var(--font-mono);">Evaluating in sandboxed environment...</div>';

  try {
    const res = await fetch('/api/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ challenge_id: id, command: cmd })
    });
    const result = await res.json();

    const isPass = result.passed;
    panel.innerHTML = `
      <div class="verification-result-box ${isPass ? 'pass' : 'fail'}">
        <div class="result-status-header">
          <span style="color: ${isPass ? 'var(--accent-green)' : 'var(--accent-red)'}">
            ${isPass ? '✓ CHALLENGE PASSED' : '✗ VERIFICATION FAILED'}
          </span>
          <span style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">
            Latency: ${result.execution_ms}ms
          </span>
        </div>
        <div style="font-size: 13px;">${result.message}</div>
        ${result.reasons && result.reasons.length ? `<ul style="margin-left: 20px; font-size: 12px; color: var(--accent-red);">${result.reasons.map(r => `<li>${r}</li>`).join('')}</ul>` : ''}
        ${result.stdout ? `<div class="console-output">${escapeHtml(result.stdout)}</div>` : ''}
        ${result.stderr ? `<div class="console-output" style="color: var(--accent-red);">${escapeHtml(result.stderr)}</div>` : ''}
      </div>
    `;

    // Refresh progress and list
    await fetchStatus();
    await fetchChallenges();
  } catch (err) {
    panel.innerHTML = `<div style="color: var(--accent-red)">Error submitting: ${err.message}</div>`;
  }
}

// LIVE SANDBOX TERMINAL
function initSandbox() {
  const input = document.getElementById('sandbox-cmd-input');
  const btn = document.getElementById('btn-run-sandbox');
  const termOut = document.getElementById('sandbox-terminal-out');

  async function executeCmd() {
    const cmd = input.value.trim();
    if (!cmd) return;
    termOut.textContent += `\n$ ${cmd}\n`;
    termOut.scrollTop = termOut.scrollHeight;

    try {
      const res = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: cmd })
      });
      const data = await res.json();
      if (data.stdout) termOut.textContent += data.stdout;
      if (data.stderr) termOut.textContent += `[stderr] ${data.stderr}`;
      if (data.returncode !== 0) termOut.textContent += `[exit ${data.returncode}]\n`;
      termOut.scrollTop = termOut.scrollHeight;
    } catch (err) {
      termOut.textContent += `Error: ${err.message}\n`;
    }
    input.value = '';
  }

  btn.onclick = executeCmd;
  input.onkeydown = (e) => {
    if (e.key === 'Enter') executeCmd();
  };
}

// KERNEL HARNESS TAB
function initKernelSim() {
  const runBtn = document.getElementById('btn-run-kernel-sim');
  const buildSysprogBtn = document.getElementById('btn-build-sysprog');
  const consoleOut = document.getElementById('kernel-console-out');

  runBtn.onclick = async () => {
    consoleOut.textContent = 'Building and launching user-space kernel driver simulator harness...\n';
    try {
      const res = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: 'make -C code_examples/04_kernel_modules test' })
      });
      const data = await res.json();
      consoleOut.textContent = (data.stdout || '') + (data.stderr || '');
    } catch (err) {
      consoleOut.textContent = `Error: ${err.message}`;
    }
  };

  buildSysprogBtn.onclick = async () => {
    consoleOut.textContent = 'Compiling and verifying all 9 C System Programming modules (epoll, fork, shm, pipes, threads, mmap)...\n';
    try {
      const res = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: 'make -C code_examples/03_system_programming test' })
      });
      const data = await res.json();
      consoleOut.textContent = (data.stdout || '') + (data.stderr || '');
    } catch (err) {
      consoleOut.textContent = `Error: ${err.message}`;
    }
  };
}

// CURRICULUM TREE RENDERER
function renderCurriculumTree() {
  const treeEl = document.getElementById('curriculum-tree');
  treeEl.innerHTML = '<div style="font-size: 11px; font-weight: 700; color: var(--text-muted); margin-bottom: 12px; letter-spacing: 1px;">CURRICULUM CHAPTERS</div>';

  for (const [folder, files] of Object.entries(state.curriculumTree)) {
    const group = document.createElement('div');
    group.style.marginBottom = '14px';

    const header = document.createElement('div');
    header.style.fontSize = '12px';
    header.style.fontWeight = '700';
    header.style.color = 'var(--accent-blue)';
    header.style.marginBottom = '6px';
    header.textContent = folder === '.' ? 'ROOT ROADMAP' : folder.toUpperCase().replace(/_/g, ' ');

    group.appendChild(header);

    files.forEach(f => {
      const item = document.createElement('div');
      item.style.padding = '6px 8px';
      item.style.borderRadius = '4px';
      item.style.cursor = 'pointer';
      item.style.fontSize = '12px';
      item.style.color = 'var(--text-secondary)';
      item.textContent = f.replace('.md', '').replace(/^[0-9]+_/, '').replace(/_/g, ' ');
      item.onmouseover = () => item.style.backgroundColor = 'var(--bg-tertiary)';
      item.onmouseout = () => item.style.backgroundColor = 'transparent';
      item.onclick = () => loadCurriculumFile(folder === '.' ? f : `${folder}/${f}`);
      group.appendChild(item);
    });

    treeEl.appendChild(group);
  }
}

async function loadCurriculumFile(relPath) {
  try {
    const res = await fetch(`/api/curriculum/${relPath}`);
    const data = await res.json();
    const contentEl = document.getElementById('curriculum-content');
    contentEl.innerHTML = parseSimpleMarkdown(data.content);
  } catch (err) {
    console.error('Failed to load curriculum file:', err);
  }
}

// PRACTICE DATASETS
function renderDatasetsTab() {
  const tabsEl = document.getElementById('dataset-tabs');
  const codeEl = document.getElementById('dataset-content');
  const metaEl = document.getElementById('dataset-meta');
  tabsEl.innerHTML = '';

  const filenames = Object.keys(state.datasets);
  if (filenames.length === 0) return;

  filenames.forEach((fname, idx) => {
    const btn = document.createElement('button');
    btn.className = `btn btn-secondary ${idx === 0 ? 'active' : ''}`;
    btn.textContent = fname;
    btn.onclick = () => {
      document.querySelectorAll('#dataset-tabs .btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      metaEl.textContent = `File: practice_data/${fname} (${state.datasets[fname].split('\n').length} lines)`;
      codeEl.textContent = state.datasets[fname];
    };
    tabsEl.appendChild(btn);
  });

  // Load first file
  const first = filenames[0];
  metaEl.textContent = `File: practice_data/${first} (${state.datasets[first].split('\n').length} lines)`;
  codeEl.textContent = state.datasets[first];
}

// BADGES TAB
function renderBadgesTab() {
  const grid = document.getElementById('badges-grid');
  if (!grid || !state.progress) return;
  grid.innerHTML = '';

  const allPossibleBadges = [
    { key: "grep_master", name: "Grep Grandmaster", icon: "🔍", desc: "Solved all 15 core grep challenges" },
    { key: "sed_surgeon", name: "Sed Stream Surgeon", icon: "✂️", desc: "Mastered stream editing across all 15 sed exercises" },
    { key: "awk_alchemist", name: "Awk Alchemist", icon: "⚗️", desc: "Completed all 20 advanced field & aggregation challenges" },
    { key: "trio_conqueror", name: "Text Processing Virtuoso", icon: "🧙‍♂️", desc: "Completed 50+ text processing exercises" },
    { key: "c_syscaller", name: "Syscall Sorcerer", icon: "⚡", desc: "Successfully wrote and verified Linux C System Programs" },
    { key: "kernel_craftsman", name: "Kernel Subsystem Hacker", icon: "🐧", desc: "Implemented and verified Linux Kernel Driver Modules" }
  ];

  const earnedKeys = new Set((state.progress.badges || []).map(b => b.key));

  allPossibleBadges.forEach(b => {
    const card = document.createElement('div');
    const isEarned = earnedKeys.has(b.key);
    card.className = `badge-card ${isEarned ? 'earned' : 'unearned'}`;
    card.innerHTML = `
      <div class="badge-icon">${b.icon}</div>
      <div class="badge-info">
        <h4>${b.name} ${isEarned ? '✓' : ''}</h4>
        <p>${b.desc}</p>
      </div>
    `;
    grid.appendChild(card);
  });
}

async function resetProgress() {
  if (!confirm('Are you sure you want to reset your progress?')) return;
  await fetch('/api/reset', { method: 'POST' });
  await fetchStatus();
  await fetchChallenges();
  alert('Progress has been reset.');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// LIGHTWEIGHT MARKDOWN RENDERER
function parseSimpleMarkdown(md) {
  if (!md) return '';
  let html = md
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    .replace(/```([\s\S]*?)```/gim, '<pre><code>$1</code></pre>')
    .replace(/`(.*?)`/gim, '<code>$1</code>')
    .replace(/^\- (.*$)/gim, '<li>$1</li>')
    .replace(/\n\n/gim, '<br><br>');
  return html;
}
