5. Memory Management In Depth — Allocators & the
MM
The allocator zoo
The kernel has several allocators because different needs have different constraints: size, contiguity, speed,
and context. Choosing correctly is a real skill.
Allocator

Returns

Use for

kmalloc

Physically contiguous, small

General small allocations, DMA-able

kzalloc

Same, zeroed

When you need clean memory

vmalloc

Virtually contiguous, large

Big buffers where physical contiguity
is not needed

kmem_cache (slab)

Fixed-size objects from a pool

Many same-size objects (frequent
alloc/free)

alloc_pages

Raw pages

Page-granular allocations, DMA

devm_kmalloc

Managed, auto-freed on unbind

Driver allocations tied to a device
lifetime

Slab caches — for objects you allocate constantly
static struct kmem_cache *my_cache;
/* init: */
my_cache = kmem_cache_create("my_obj", sizeof(struct my_obj),
0, SLAB_HWCACHE_ALIGN, NULL);
/* hot path: */
struct my_obj *o = kmem_cache_alloc(my_cache, GFP_KERNEL);
kmem_cache_free(my_cache, o);
/* exit: */
kmem_cache_destroy(my_cache);