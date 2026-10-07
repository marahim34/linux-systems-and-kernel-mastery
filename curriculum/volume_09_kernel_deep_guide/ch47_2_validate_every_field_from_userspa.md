2. VALIDATE every field from userspace before using it — an unchecked count is an exploit waiting to happen.
3. kmalloc_array checks for multiplication overflow that plain kmalloc(count * size) would miss — a classic
integer-overflow defence.