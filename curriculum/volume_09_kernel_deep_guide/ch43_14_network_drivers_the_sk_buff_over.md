14. Network Drivers & the sk_buff (Overview)
Network drivers move packets between the wire and the kernel's networking stack. The central data structure
is the sk_buff (socket buffer), which carries a packet and its metadata through every layer.
Concept

Role

sk_buff (skb)

Holds one packet plus headroom, headers, metadata

net_device

Represents a network interface (eth0)

NAPI

Interrupt+polling hybrid for high packet rates

ndo_start_xmit

Your TX function: send a packet to the hardware

netif_rx / napi

Your RX path: hand received packets up the stack

A network driver registers a net_device with operations for transmit and receive. On receive, under high load
it uses NAPI — disabling interrupts and POLLING for packets in batches — to avoid interrupt storms
(thousands of interrupts per second would collapse the system). The sk_buff is passed up the stack, gaining
and shedding headers at each layer.
PRO INSIGHT: The sk_buff is the packet's vehicle through the entire network stack, and NAPI is the answer to a
real scaling crisis: at gigabit speeds, one interrupt per packet means hundreds of thousands of interrupts per
second, drowning the CPU. NAPI switches to polling under load — the driver disables RX interrupts and pulls
packets in batches, restoring interrupts only when traffic subsides. This interrupt-mitigation pattern is essential
knowledge, and mirrors the general kernel theme: batch expensive operations, poll when busy, interrupt when idle.