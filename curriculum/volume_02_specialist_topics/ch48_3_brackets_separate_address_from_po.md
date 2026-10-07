3. Brackets separate address from port — everywhere: curl, pg connection strings, ssh (ssh -6 user@[addr]).

PRO INSIGHT: Debugging asymmetry: 'the site is down' for ONE user while fine for you is increasingly a
broken-AAAA story — their network prefers v6, yours prefers v4. Test both explicitly: curl -4 and curl -6.
PRACTICE EXERCISES