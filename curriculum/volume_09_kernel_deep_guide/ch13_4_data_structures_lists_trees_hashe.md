4. Data Structures — Lists, Trees, Hashes the Kernel
Way
Intrusive by design
The kernel provides highly optimised, INTRUSIVE data structures: your object embeds the linkage, and
macros operate on it. No allocation for nodes, no templates, cache-friendly. Master these three and you can
read most kernel code.
#include <linux/list.h>
struct task { int id; struct list_head list; };
LIST_HEAD(my_tasks); /* the list head */
struct task *t = kmalloc(sizeof(*t), GFP_KERNEL);
list_add_tail(&t->list, &my_tasks); /* append */
struct task *pos;
list_for_each_entry(pos, &my_tasks, list)
pr_info("task %d\n", pos->id);
list_del(&t->list); kfree(t);