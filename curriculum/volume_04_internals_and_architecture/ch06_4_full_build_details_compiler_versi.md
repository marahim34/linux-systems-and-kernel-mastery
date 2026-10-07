4. Full build details: compiler version, build date. /proc is a live window INTO the kernel, which is itself a fascinating idea
(see below).

The /proc and /sys illusion — the kernel as files
Here is one of Linux's most elegant tricks. The kernel exposes its own internal state as if it were files, under
/proc and /sys. These are not real files on disk; reading them makes the kernel generate the answer on the
spot. This means you can inspect and even reconfigure the running kernel with ordinary commands like cat
and echo.





cat /proc/cpuinfo | grep "model name" | head -1
cat /proc/meminfo | head -3
cat /proc/loadavg
cat /sys/class/thermal/thermal_zone0/temp
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward