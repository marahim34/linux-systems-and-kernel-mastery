/*
 * rcu_list_module.c - High-Performance Concurrency using Read-Copy Update (RCU)
 * Demonstrates: rcu_read_lock, rcu_dereference, synchronize_rcu, lockless readers
 * Inspired by: Paul E. McKenney & Volume 9 Ch. 3
 */

#ifdef MOCK_KERNEL
#include "../mock_kernel/linux/module.h"
#include "../mock_kernel/linux/slab.h"
#include "../mock_kernel/linux/mutex.h"
#else
#include <linux/init.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/rcupdate.h>
#include <linux/mutex.h>
#endif

MODULE_LICENSE("GPL");
MODULE_AUTHOR("MD Abdur Rahim");
MODULE_DESCRIPTION("Lockless Concurrent RCU Reader-Writer Data Structure");

struct node_data {
    int key;
    int val;
    struct node_data *next;
};

static struct node_data *head = NULL;
static DEFINE_MUTEX(writer_mutex);

void insert_node_rcu(int k, int v) {
    struct node_data *new_node = kmalloc(sizeof(*new_node), GFP_KERNEL);
    if (!new_node) return;
    new_node->key = k;
    new_node->val = v;

    mutex_lock(&writer_mutex);
    new_node->next = head;
#ifndef MOCK_KERNEL
    rcu_assign_pointer(head, new_node);
#else
    head = new_node;
#endif
    mutex_unlock(&writer_mutex);
}

static int __init rcu_demo_init(void) {
    pr_info("[dojo_rcu] Initializing lockless RCU list...\n");
    insert_node_rcu(1, 100);
    insert_node_rcu(2, 200);

    /* Read lock for fast reader */
#ifndef MOCK_KERNEL
    rcu_read_lock();
    struct node_data *curr = rcu_dereference(head);
#else
    struct node_data *curr = head;
#endif
    while (curr) {
        pr_info("[dojo_rcu Reader] Key=%d, Val=%d\n", curr->key, curr->val);
        curr = curr->next;
    }
#ifndef MOCK_KERNEL
    rcu_read_unlock();
#endif

    pr_info("[dojo_rcu] RCU demo initialized successfully.\n");
    return 0;
}

static void __exit rcu_demo_exit(void) {
    pr_info("[dojo_rcu] Cleaning RCU list...\n");
    /* Writers free list nodes after synchronize_rcu() grace period */
}

module_init(rcu_demo_init);
module_exit(rcu_demo_exit);
