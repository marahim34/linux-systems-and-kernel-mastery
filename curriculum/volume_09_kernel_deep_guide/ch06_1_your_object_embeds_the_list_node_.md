1. Your object embeds the list node directly, rather than the list pointing at your object.
2. container_of takes a pointer to a MEMBER, the containing type, and the member name, and computes the address of
the enclosing struct by subtracting the member's offset. Type-safe generic containers in pure C. Study this macro until it
is obvious — it underpins the whole kernel.