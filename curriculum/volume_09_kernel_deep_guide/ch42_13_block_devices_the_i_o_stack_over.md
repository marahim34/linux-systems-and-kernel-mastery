13. Block Devices & the I/O Stack (Overview)
Block drivers serve storage — disks, SSDs — where data moves in blocks and performance depends on
scheduling and merging requests. The modern interface is blk-mq (multi-queue), built for many-core,
high-IOPS devices.
Layer

Role

Filesystem / page cache

Issues reads/writes as block requests

blk-mq

Per-CPU submission queues; merges and schedules
requests

I/O scheduler

Orders requests (mq-deadline, BFQ, none for NVMe)

Block driver

Your code: takes requests, drives the hardware,
completes them

A block driver registers a request-handling function that receives bio/request structures describing what to
read or write where, programs the hardware (usually via DMA), and signals completion. The complexity
versus char drivers is the performance machinery: queues, merging, and completion handling across many
cores. For most learners, understanding the STACK and where a driver plugs in matters more than writing
one early.
PRO INSIGHT: Key insight for block work: the whole stack exists to turn random, small filesystem operations into
efficient, ordered, merged, parallel hardware transfers. Your driver sits at the bottom, and its job is throughput and
correctness under massive concurrency. NVMe drivers use 'none' scheduling because the device itself parallelises;
spinning disks benefit from ordering. Knowing WHERE your driver sits in this stack, and what the layers above have
already done to the requests, is the foundation of block-device work.