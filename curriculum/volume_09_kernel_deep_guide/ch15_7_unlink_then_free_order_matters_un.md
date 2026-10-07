7. Unlink then free — order matters; unlink while the object is still valid.

Red-black trees and hash tables
Structure

Header

Use when

list_head

linux/list.h

Ordered traversal, queues, LRU

hlist

linux/list.h

Hash buckets (single-pointer head
saves memory)

rb_root (red-black tree)

linux/rbtree.h

Sorted data with O(log n) lookup

DECLARE_HASHTABLE

linux/hashtable.h

Fast keyed lookup

xarray / idr

linux/xarray.h

Integer-to-pointer mapping (IDs to
objects)





PRO INSIGHT: These intrusive structures are why the kernel is fast and why it looks alien to application
programmers. Because the linkage lives INSIDE your object, adding to a list needs no allocation and touches no
separate node — the object is the node. One object can even sit in several lists at once by embedding several
list_heads. For a C++ programmer used to std::list allocating wrapper nodes, this is a genuinely better design for
systems code. Learn container_of and list_for_each_entry cold; they appear on nearly every kernel page.
PRACTICE EXERCISES