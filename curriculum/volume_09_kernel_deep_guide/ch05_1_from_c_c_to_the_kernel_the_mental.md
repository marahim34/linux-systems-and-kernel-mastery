1. From C/C++ to the Kernel — the Mental Reset
What your C knowledge transfers, and what betrays you
You know C, so the syntax is free. But several habits from application C and especially C++ are actively
dangerous in the kernel. This chapter is the reset.
Your habit

In the kernel

Because

#include <stdio.h>, libc

Gone entirely

The kernel is freestanding; it has its
own headers

malloc/free

kmalloc/kfree, and more

Multiple allocators with context rules

Unbounded recursion, big locals

Forbidden

The kernel stack is ~8–16 KB, fixed

float/double

Effectively banned

FPU state is not saved across kernel
entry by default

Exceptions, RTTI, STL (C++)

None

The kernel is C; no C++ runtime
exists in it

Assume allocation succeeds

Always check

No OOM safety net; failure is normal

Single-threaded assumptions

Never

Your code runs on all CPUs at once

errno

Return -E values directly

Negative errno is the kernel
convention

PRO INSIGHT: The deepest reset for a C++ programmer: there is no runtime beneath you. No new/delete, no
constructors firing automatically, no exceptions unwinding the stack, no STL container managing memory. The
kernel is C with manual everything, running in an environment where a mistake halts the machine. Your C++
instincts for abstraction must be replaced by explicit, defensive, resource-tracked C. The good news: your
understanding of memory, pointers, and undefined behaviour is exactly what keeps you alive here.

The kernel's idioms that replace language features
You would reach for (C++)

Kernel idiom

Templates / generics

void * plus container_of() and macros

Constructors/destructors

explicit init/exit functions and goto cleanup

RAII

manual paired acquire/release; devm_* managed
resources

std::list, std::map

list_head, rb_root, hlist (intrusive structures)

Exceptions

integer error codes checked on every call

dynamic_cast

container_of() to recover the enclosing struct

The single most important idiom to internalise is container_of() and intrusive data structures. Instead of a list
holding pointers to your objects, your objects EMBED a list node, and container_of() recovers the object from
the node. This is how the kernel gets generic containers in C without templates, and it is everywhere.





struct my_item {
int value;
struct list_head node; /* embedded, intrusive */
};
/* given a list_head *p, recover the my_item: */
struct my_item *it = container_of(p, struct my_item, node);