11. Virtualization & the Cloud — the Theory
What virtualization really is
Volume 2 used Docker; here is the theory. Virtualization lets one physical machine present itself as many
independent virtual machines, each believing it has its own hardware. A hypervisor is the layer that creates
and manages them, playing for whole operating systems the role an OS plays for processes: it shares real
hardware among guests that think they are alone.
Type

Runs on

Examples

Trade-off

Type 1 (bare metal)

Directly on hardware

VMware ESXi, Xen, KVM

Fast; runs the cloud

Type 2 (hosted)

On top of a host OS

VirtualBox, VMware
Workstation

Convenient; a bit slower

Virtual machines versus containers
Two ways to isolate workloads, at different layers. A virtual machine virtualises the HARDWARE — each
VM runs a full guest OS with its own kernel (heavy, strongly isolated). A container (Volume 1 Ch. 19)
virtualises the OPERATING SYSTEM — all containers share the host kernel but get isolated views via
namespaces and cgroups (light, fast, less isolated). Choosing between them is a core cloud-design decision.
Virtual Machine

Container

Virtualises

Hardware

The operating system

Contains

A full guest OS + kernel

Just the app and its libraries

Size / start

Gigabytes / minutes

Megabytes / milliseconds

Isolation

Strong (separate kernels)

Lighter (shared kernel)

Use

Different OSes, strong isolation

Many small services, density

PRO INSIGHT: The cloud in one sentence: providers buy huge physical machines, slice them into VMs with Type-1
hypervisors, and rent you the slices by the hour. Your Hetzner VPS is one such slice. Containers then pack many
services INTO each VM. The entire cloud economy rests on this two-level virtualization — hardware into VMs, VMs
into containers. Understanding it is understanding the industry you are entering.
PRACTICE EXERCISES