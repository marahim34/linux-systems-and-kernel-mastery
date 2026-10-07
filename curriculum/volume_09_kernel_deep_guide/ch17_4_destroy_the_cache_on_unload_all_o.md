4. Destroy the cache on unload (all objects must be freed first). This is how the kernel manages millions of task_structs,
inodes, and dentries efficiently.

Managed allocations — devm_, the closest thing to RAII
For a C++ programmer missing RAII, the devm_ family is the kernel's answer. Memory (and other resources)
allocated with devm_kmalloc, devm_ioremap, etc. are automatically freed when the device unbinds. This





eliminates most cleanup code and a whole class of leak bugs in drivers.
static int my_probe(struct platform_device *pdev)
{
struct my_priv *priv;
priv = devm_kzalloc(&pdev->dev, sizeof(*priv), GFP_KERNEL);
if (!priv) return -ENOMEM;
/* no kfree needed anywhere — freed automatically on unbind */
return 0;
}