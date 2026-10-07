4. Cleanup labels unwind in REVERSE order of allocation — freeing exactly what was allocated so far. This goto-ladder
is the standard, correct kernel cleanup pattern, not bad style.