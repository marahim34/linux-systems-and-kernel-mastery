4. The EXIT function runs on unload; __exit marks it as cleanup-only.
5. module_init/module_exit REGISTER these functions as the entry and exit points — the kernel calls them.