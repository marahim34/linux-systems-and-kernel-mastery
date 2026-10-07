5. Unload; the device vanishes and the buffer is freed. A complete, working driver you built and understand line by line.

PRO INSIGHT: This one driver is the whole volume made concrete. It registers with the kernel, exposes a file in
/dev, safely exchanges data with user space across the protection boundary, allocates and frees kernel memory
correctly, and cleans up in exact reverse order. Every real character driver — for a sensor, a serial port, a custom
board — has this exact skeleton. You now have a template you understand completely, which is the foundation of
all driver work.