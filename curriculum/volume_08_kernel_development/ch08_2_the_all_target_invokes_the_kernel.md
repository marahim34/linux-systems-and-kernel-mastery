2. The all target invokes the KERNEL's build system (-C into its build dir) and points it back at your directory
(M=$(PWD)). This is how modules are always built.
3. clean removes the build artifacts. Note: Makefiles require real TAB characters, not spaces, before commands.