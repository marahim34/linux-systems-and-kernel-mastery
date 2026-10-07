/**
 * app.js - Linux Mastery Dojo Single-Page Web Engine
 * Fully featured client for 536-chapter library, 107 challenges,
 * command reference, interview dojo, kernel harness, and terminal sandbox.
 */

let state = {
  challenges: [],
  selectedChallenge: null,
  datasets: {},
  curriculumTree: {},
  commands: [],
  interviews: [],
  progress: null
};

// INITIALIZATION
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  fetchStatus();
  fetchChallenges();
  fetchDatasets();
  fetchCurriculum();
  fetchCommands();
  fetchInterviews();
  initSandbox();
  initKernelSim();

  // Filter & Search Listeners
  const filterTier = document.getElementById('filter-tier');
  if (filterTier) filterTier.addEventListener('change', renderChallengeList);

  const filterCat = document.getElementById('filter-cat');
  if (filterCat) filterCat.addEventListener('change', renderChallengeList);

  const btnReset = document.getElementById('btn-reset-progress');
  if (btnReset) btnReset.addEventListener('click', resetProgress);

  const currSearch = document.getElementById('curriculum-search');
  if (currSearch) {
    currSearch.addEventListener('input', (e) => {
      renderCurriculumTree(e.target.value.trim().toLowerCase());
    });
  }

  const cmdSearch = document.getElementById('cmd-search-input');
  if (cmdSearch) {
    cmdSearch.addEventListener('input', (e) => {
      renderCommandsTab(e.target.value.trim().toLowerCase());
    });
  }
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

// FETCH DATA ENDPOINTS
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

async function fetchCommands() {
  try {
    const res = await fetch('/api/commands');
    state.commands = await res.json();
    renderCommandsTab();
  } catch (err) {
    console.error('Failed to fetch commands:', err);
  }
}

async function fetchInterviews() {
  try {
    const res = await fetch('/api/interviews');
    state.interviews = await res.json();
    renderInterviewsTab();
  } catch (err) {
    console.error('Failed to fetch interviews:', err);
  }
}

// RENDER TOP BAR STATS
function renderTopBarStats() {
  if (!state.progress) return;
  const rankEl = document.getElementById('stat-rank');
  if (rankEl) rankEl.textContent = state.progress.rank;

  const compEl = document.getElementById('stat-completed');
  if (compEl) compEl.textContent = `${state.progress.total_completed} / ${state.progress.total_challenges}`;

  const badgeEl = document.getElementById('stat-badges');
  if (badgeEl) badgeEl.textContent = `${state.progress.badges.length} 🏆`;
}

// RENDER CHALLENGES LIST
function renderChallengeList() {
  const listEl = document.getElementById('challenge-list');
  if (!listEl) return;
  const tierFilter = document.getElementById('filter-tier') ? document.getElementById('filter-tier').value : '';
  const catFilter = document.getElementById('filter-cat') ? document.getElementById('filter-cat').value : '';

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
      <div class="card-title">${escapeHtml(c.title)}</div>
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
    if (!detailEl) return;

    detailEl.innerHTML = `
      <div class="challenge-title-row">
        <div>
          <h2>${escapeHtml(c.title)}</h2>
          <div style="font-family: var(--font-mono); color: var(--text-muted); font-size: 12px; margin-top: 4px;">
            ID: ${c.id} | Tier: ${c.tier.toUpperCase()} | Category: ${c.category.toUpperCase()}
          </div>
        </div>
        <span class="badge-tag ${c.completed ? 'completed' : 'pending'}" style="font-size: 12px; padding: 4px 10px;">
          ${c.completed ? 'COMPLETED ✓' : 'INCOMPLETE'}
        </span>
      </div>

      <div class="challenge-desc-box">
        <strong>Task:</strong> ${escapeHtml(c.description)}
      </div>

      <div class="workspace-input-section">
        <label style="font-weight: 600; font-size: 13px;">Your Solution Command:</label>
        <textarea id="editor-cmd" class="cmd-editor" placeholder="Enter bash command (e.g. grep ERROR app.log)...">${c.completed && c.user_solution ? escapeHtml(c.user_solution) : ''}</textarea>
        
        <div class="action-row">
          <button class="btn btn-primary" id="btn-submit-sol">Submit & Verify</button>
          <button class="btn btn-secondary" id="btn-toggle-hint">Hint</button>
          <button class="btn btn-secondary" id="btn-toggle-sol">Reveal Solution</button>
        </div>
      </div>

      <div id="hint-box" style="display: none; background: var(--bg-secondary); border-left: 3px solid var(--accent-yellow); padding: 12px; border-radius: 4px;">
        <strong>Hint:</strong> ${escapeHtml(c.hint || 'No hint available.')}
      </div>

      <div id="solution-box" style="display: none; background: var(--bg-secondary); border-left: 3px solid var(--accent-blue); padding: 12px; border-radius: 4px; font-family: var(--font-mono);">
        <strong>Reference Solution:</strong><br>
        <code>${escapeHtml(c.solution)}</code>
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
        <div style="font-size: 13px;">${escapeHtml(result.message)}</div>
        ${result.reasons && result.reasons.length ? `<ul style="margin-left: 20px; font-size: 12px; color: var(--accent-red);">${result.reasons.map(r => `<li>${escapeHtml(r)}</li>`).join('')}</ul>` : ''}
        ${result.stdout ? `<div class="console-output">${escapeHtml(result.stdout)}</div>` : ''}
        ${result.stderr ? `<div class="console-output" style="color: var(--accent-red);">${escapeHtml(result.stderr)}</div>` : ''}
      </div>
    `;

    await fetchStatus();
    await fetchChallenges();
  } catch (err) {
    panel.innerHTML = `<div style="color: var(--accent-red)">Error submitting: ${escapeHtml(err.message)}</div>`;
  }
}

// LIVE SANDBOX TERMINAL
function initSandbox() {
  const input = document.getElementById('sandbox-cmd-input');
  const btn = document.getElementById('btn-run-sandbox');
  const termOut = document.getElementById('sandbox-terminal-out');
  if (!input || !btn || !termOut) return;

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
  if (!runBtn || !buildSysprogBtn || !consoleOut) return;

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

// FOLDER DISPLAY LABELS MAPPING
const FOLDER_NAMES = {
  '.': '📌 Root Roadmaps & Overview',
  'volume_01_the_ultimate_edition': 'Vol 1: The Ultimate Edition',
  'volume_02_specialist_topics': 'Vol 2: Specialist Topics',
  'volume_03_practice_workbook': 'Vol 3: TAMK Practice Workbook',
  'volume_04_internals_and_architecture': 'Vol 4: Internals & Architecture',
  'volume_05_operating_system_theory': 'Vol 5: Operating System Theory',
  'volume_06_installing_software': 'Vol 6: Installing Software',
  'volume_07_bash_configuration_and_scripting': 'Vol 7: Bash Scripting & Env',
  'volume_08_kernel_development': 'Vol 8: Kernel Development Core',
  'volume_09_kernel_deep_guide': 'Vol 9: Kernel Deep Subsystems',
  'specialist_guides': '⭐ Specialist Mastery Guides',
  'tlpi_systems_programming': '📖 Michael Kerrisk: TLPI 64-Ch',
  'kernel_subsystems_lkd_ulk3': '🐧 Robert Love: LKD & ULK3'
};

// CURRICULUM TREE RENDERER WITH ACCORDION & SEARCH
function renderCurriculumTree(searchQuery = '') {
  const treeEl = document.getElementById('curriculum-tree');
  if (!treeEl) return;

  treeEl.innerHTML = '';

  const entries = Object.entries(state.curriculumTree);
  if (entries.length === 0) {
    treeEl.innerHTML = '<div style="color: var(--text-muted); font-size: 12px; padding: 10px;">Loading curriculum index...</div>';
    return;
  }

  let totalMatchCount = 0;

  for (const [folder, files] of entries) {
    const folderLabel = FOLDER_NAMES[folder] || folder.replace(/_/g, ' ').toUpperCase();

    // Filter files if search is active
    const matchingFiles = files.filter(f => {
      if (!searchQuery) return true;
      const cleanName = f.toLowerCase().replace(/_/g, ' ');
      return cleanName.includes(searchQuery) || folderLabel.toLowerCase().includes(searchQuery);
    });

    if (matchingFiles.length === 0 && searchQuery) {
      continue; // Skip folders with no matches
    }

    totalMatchCount += matchingFiles.length;

    const folderContainer = document.createElement('div');
    folderContainer.className = 'vol-folder';

    const header = document.createElement('div');
    header.className = 'vol-header';
    const isExpanded = !!searchQuery || folder === 'volume_01_the_ultimate_edition';

    header.innerHTML = `
      <span>${folderLabel} <small style="color: var(--text-muted);">(${matchingFiles.length})</small></span>
      <span class="folder-arrow">${isExpanded ? '▼' : '▶'}</span>
    `;

    const content = document.createElement('div');
    content.className = `vol-content ${isExpanded ? 'open' : ''}`;

    header.onclick = () => {
      const willOpen = !content.classList.contains('open');
      content.classList.toggle('open', willOpen);
      const arrow = header.querySelector('.folder-arrow');
      if (arrow) arrow.textContent = willOpen ? '▼' : '▶';
    };

    matchingFiles.forEach(f => {
      const item = document.createElement('div');
      item.className = 'ch-item';
      const displayName = f
        .replace(/\.md$/i, '')
        .replace(/^[0-9]+_/, '')
        .replace(/_/g, ' ');

      item.textContent = displayName;
      item.title = `${folder}/${f}`;
      item.onclick = (e) => {
        e.stopPropagation();
        document.querySelectorAll('.ch-item').forEach(el => el.style.backgroundColor = '');
        item.style.backgroundColor = 'var(--accent-blue-bg)';
        loadCurriculumFile(folder === '.' ? f : `${folder}/${f}`);
      };

      content.appendChild(item);
    });

    folderContainer.appendChild(header);
    folderContainer.appendChild(content);
    treeEl.appendChild(folderContainer);
  }

  if (searchQuery && totalMatchCount === 0) {
    treeEl.innerHTML = `<div style="color: var(--text-muted); font-size: 12px; padding: 12px;">No chapters found matching "${escapeHtml(searchQuery)}"</div>`;
  }
}

// LOAD AND DISPLAY CURRICULUM CHAPTER
async function loadCurriculumFile(relPath) {
  try {
    const viewer = document.getElementById('curriculum-viewer');
    const contentEl = document.getElementById('curriculum-content');
    contentEl.innerHTML = '<div style="color: var(--text-muted); font-family: var(--font-mono);">Loading chapter content...</div>';

    // Switch tab to curriculum if not already there
    const navCurriculum = document.querySelector('[data-tab="curriculum"]');
    if (navCurriculum && !navCurriculum.classList.contains('active')) {
      navCurriculum.click();
    }

    const res = await fetch(`/api/curriculum/${relPath}`);
    const data = await res.json();

    contentEl.innerHTML = parseMarkdown(data.content);
    if (viewer) viewer.scrollTop = 0;
  } catch (err) {
    console.error('Failed to load curriculum file:', err);
    const contentEl = document.getElementById('curriculum-content');
    if (contentEl) contentEl.innerHTML = `<div style="color: var(--accent-red)">Error loading file: ${escapeHtml(err.message)}</div>`;
  }
}
window.loadCurriculumFile = loadCurriculumFile;

// COMMAND REFERENCE TAB
function renderCommandsTab(query = '') {
  const grid = document.getElementById('cmd-cards-grid');
  if (!grid) return;

  grid.innerHTML = '';

  const filtered = state.commands.filter(cmd => {
    if (!query) return true;
    return cmd.cmd.toLowerCase().includes(query) ||
           cmd.desc.toLowerCase().includes(query) ||
           (cmd.flags && cmd.flags.toLowerCase().includes(query)) ||
           (cmd.category && cmd.category.toLowerCase().includes(query));
  });

  if (filtered.length === 0) {
    grid.innerHTML = `<div style="color: var(--text-muted); grid-column: 1 / -1; padding: 20px;">No commands matching "${escapeHtml(query)}"</div>`;
    return;
  }

  filtered.forEach(c => {
    const card = document.createElement('div');
    card.className = 'cmd-card';
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span class="cmd-title">${escapeHtml(c.cmd)}</span>
        <span class="badge-tag pending" style="font-size: 10px;">${escapeHtml((c.category || 'general').toUpperCase())}</span>
      </div>
      <div class="cmd-desc">${escapeHtml(c.desc)}</div>
      <div class="cmd-syntax"><code>$ ${escapeHtml(c.syntax)}</code></div>
      ${c.flags ? `<div class="cmd-flags"><strong>Key Options:</strong> ${escapeHtml(c.flags)}</div>` : ''}
      <div class="cmd-example"><strong>Example:</strong> $ ${escapeHtml(c.example)}</div>
    `;
    grid.appendChild(card);
  });
}

// INTERVIEW QUESTIONS TAB
function renderInterviewsTab() {
  const list = document.getElementById('interview-list');
  if (!list) return;

  list.innerHTML = '';

  if (state.interviews.length === 0) {
    list.innerHTML = '<div style="color: var(--text-muted); padding: 20px;">Loading interview questions...</div>';
    return;
  }

  state.interviews.forEach((q, idx) => {
    const card = document.createElement('div');
    card.className = 'interview-card';
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span class="interview-badge">${escapeHtml(q.level)} · ${escapeHtml(q.category)}</span>
        <span style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">Q${idx + 1}</span>
      </div>
      <div class="interview-question">${escapeHtml(q.question)}</div>
      <button class="btn btn-secondary btn-sm" id="btn-toggle-ans-${idx}">
        <span>Reveal Deep Technical Answer</span>
      </button>
      <div class="interview-answer" id="ans-${idx}" style="display: none;">
        ${parseMarkdown(q.answer)}
      </div>
    `;

    const btn = card.querySelector(`#btn-toggle-ans-${idx}`);
    const ans = card.querySelector(`#ans-${idx}`);
    btn.onclick = () => {
      const isHidden = ans.style.display === 'none';
      ans.style.display = isHidden ? 'block' : 'none';
      btn.firstElementChild.textContent = isHidden ? 'Hide Answer' : 'Reveal Deep Technical Answer';
    };

    list.appendChild(card);
  });
}

// PRACTICE DATASETS
function renderDatasetsTab() {
  const tabsEl = document.getElementById('dataset-tabs');
  const codeEl = document.getElementById('dataset-content');
  const metaEl = document.getElementById('dataset-meta');
  if (!tabsEl || !codeEl || !metaEl) return;

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
    { key: "grep_master", name: "Grep Grandmaster", icon: "🔍", desc: "Solved all 19 core and TAMK grep challenges" },
    { key: "sed_surgeon", name: "Sed Stream Surgeon", icon: "✂️", desc: "Mastered stream editing across all 19 sed exercises" },
    { key: "awk_alchemist", name: "Awk Alchemist", icon: "⚗️", desc: "Completed all 22 advanced field & aggregation challenges" },
    { key: "tamk_conqueror", name: "TAMK Lab Veteran", icon: "🛡️", desc: "Mastered directory navigation, globbing, permissions, and tar archives" },
    { key: "trio_virtuoso", name: "Text Processing Virtuoso", icon: "🧙‍♂️", desc: "Completed 60+ text processing exercises" },
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
        <h4>${escapeHtml(b.name)} ${isEarned ? '✓' : ''}</h4>
        <p>${escapeHtml(b.desc)}</p>
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
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ROBUST MARKDOWN PARSER
function parseMarkdown(md) {
  if (!md) return '';

  // Extract fenced code blocks first to protect formatting
  const codeBlocks = [];
  let processed = md.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
    const placeholder = `__CODE_BLOCK_${codeBlocks.length}__`;
    codeBlocks.push(`<pre><code class="language-${lang}">${escapeHtml(code)}</code></pre>`);
    return placeholder;
  });

  // Headers
  processed = processed
    .replace(/^#### (.*$)/gim, '<h4>$1</h4>')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>');

  // Blockquotes
  processed = processed.replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>');

  // Horizontal Rules
  processed = processed.replace(/^---$/gim, '<hr style="border:0; border-top:1px solid var(--border-color); margin: 20px 0;">');

  // Bold & Italic
  processed = processed
    .replace(/\*\*\*(.*?)\*\*\*/gim, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>');

  // Inline code
  processed = processed.replace(/`([^`]+)`/g, (m, code) => `<code>${escapeHtml(code)}</code>`);

  // Bullet items
  processed = processed.replace(/^\- (.*$)/gim, '<li>$1</li>');
  processed = processed.replace(/^\* (.*$)/gim, '<li>$1</li>');

  // Paragraph breaks
  processed = processed.replace(/\n\n+/g, '<br><br>');

  // Restore code blocks
  codeBlocks.forEach((block, idx) => {
    processed = processed.replace(`__CODE_BLOCK_${idx}__`, block);
  });

  return processed;
}
