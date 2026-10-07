1. Foundations — What Linux Actually Is
The layers
Linux is technically only the kernel — the core program that talks to hardware, schedules processes, and
manages memory. What you install (Ubuntu, Debian, Fedora) is a distribution: the kernel plus thousands of
tools, a package manager, and defaults. On top of the kernel sits the shell (usually bash), the program that
reads your typed commands and runs them.
Layer

What it does

Example

Hardware

CPU, RAM, disk, network card

Your Hetzner VPS or laptop

Kernel

Talks to hardware, runs processes

Linux 6.x

Shell

Interprets your commands

bash, zsh

Utilities

The commands themselves

ls, grep, systemctl

Applications

What you actually run

nginx, PostgreSQL, Python

Why servers run Linux
Over 90% of cloud servers run Linux for concrete reasons: it is free, it runs for years without reboot,
everything is automatable text, resource usage is tiny (a full server OS in 500 MB of RAM), and security
patching is fast and transparent. When you rent a Hetzner VPS or spin up cPouta, you get a blank Linux
machine and full control — this book teaches you to command it.

Distributions — which one to master
Family

Members

Package tool

Choose when

Debian

Debian, Ubuntu, Mint

apt / .deb

Servers, beginners, most
tutorials — LEARN THIS
FIRST

RedHat

RHEL, Fedora, Rocky

dnf / .rpm

Enterprise jobs, RHCSA
certification

Arch

Arch, Manjaro

pacman

Enthusiasts who want
bleeding edge

Alpine

Alpine

apk

Tiny Docker container
images

Skills transfer ~90% between families — only the package manager and a few paths differ. This book uses
Ubuntu/Debian conventions, matching your WSL and cPouta environments.

Where to practice safely