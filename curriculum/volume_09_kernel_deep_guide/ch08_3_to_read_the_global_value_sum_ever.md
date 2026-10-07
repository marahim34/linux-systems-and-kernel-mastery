3. To read the global value, sum every CPU's copy. You pay the cost only on the rare read, not the frequent write. This
'shard per CPU' pattern is a cornerstone of kernel scalability.