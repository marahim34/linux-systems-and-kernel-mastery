# Understanding the Linux Kernel (3rd Edition) · Bovet & Cesati

## Hardware Architecture, Paging, Interrupts & VFS Syllabus

Table of Contents

Preface . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xi
1. Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1
Linux Versus Other Unix-Like Kernels
Hardware Dependency
Linux Versions
Basic Operating System Concepts
An Overview of the Unix Filesystem
An Overview of Unix Kernels

2
6
7
8
12
19

2. Memory Addressing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35
Memory Addresses
Segmentation in Hardware
Segmentation in Linux
Paging in Hardware
Paging in Linux

35
36
41
45
57

3. Processes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 79
Processes, Lightweight Processes, and Threads
Process Descriptor
Process Switch
Creating Processes
Destroying Processes

79
81
102
114
126

4. Interrupts and Exceptions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 131
The Role of Interrupt Signals
Interrupts and Exceptions

132
133

v

Nested Execution of Exception and Interrupt Handlers
Initializing the Interrupt Descriptor Table
Exception Handling
Interrupt Handling
Softirqs and Tasklets
Work Queues
Returning from Interrupts and Exceptions

143
145
148
151
171
180
183

5. Kernel Synchronization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 189
How the Kernel Services Requests
Synchronization Primitives
Synchronizing Accesses to Kernel Data Structures
Examples of Race Condition Prevention

189
194
217
222

6. Timing Measurements . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 227
Clock and Timer Circuits
The Linux Timekeeping Architecture
Updating the Time and Date
Updating System Statistics
Software Timers and Delay Functions
System Calls Related to Timing Measurements

228
232
240
241
244
252

7. Process Scheduling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 258
Scheduling Policy
The Scheduling Algorithm
Data Structures Used by the Scheduler
Functions Used by the Scheduler
Runqueue Balancing in Multiprocessor Systems
System Calls Related to Scheduling

258
262
266
270
284
290

8. Memory Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 294
Page Frame Management
Memory Area Management
Noncontiguous Memory Area Management

294
323
342

9. Process Address Space . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 351
The Process’s Address Space
The Memory Descriptor
Memory Regions

vi

|

Table of Contents

352
353
357

Page Fault Exception Handler
Creating and Deleting a Process Address Space
Managing the Heap

376
392
395

10. System Calls . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 398
POSIX APIs and System Calls
System Call Handler and Service Routines
Entering and Exiting a System Call
Parameter Passing
Kernel Wrapper Routines

398
399
401
409
418

11. Signals . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 420
The Role of Signals
Generating a Signal
Delivering a Signal
System Calls Related to Signal Handling

420
433
439
450

12. The Virtual Filesystem . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 456
The Role of the Virtual Filesystem (VFS)
VFS Data Structures
Filesystem Types
Filesystem Handling
Pathname Lookup
Implementations of VFS System Calls
File Locking

456
462
481
483
495
505
510

13. I/O Architecture and Device Drivers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 519
I/O Architecture
The Device Driver Model
Device Files
Device Drivers
Character Device Drivers

519
526
536
540
552

14. Block Device Drivers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 560
Block Devices Handling
The Generic Block Layer
The I/O Scheduler
Block Device Drivers
Opening a Block Device File

560
566
572
585
595

Table of Contents

|

vii

15. The Page Cache . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 599
The Page Cache
Storing Blocks in the Page Cache
Writing Dirty Pages to Disk
The sync( ), fsync( ), and fdatasync() System Calls

600
611
622
629

16. Accessing Files . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 631
Reading and Writing a File
Memory Mapping
Direct I/O Transfers
Asynchronous I/O

632
657
668
671

17. Page Frame Reclaiming . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 676
The Page Frame Reclaiming Algorithm
Reverse Mapping
Implementing the PFRA
Swapping

676
680
689
712

18. The Ext2 and Ext3 Filesystems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 738
General Characteristics of Ext2
Ext2 Disk Data Structures
Ext2 Memory Data Structures
Creating the Ext2 Filesystem
Ext2 Methods
Managing Ext2 Disk Space
The Ext3 Filesystem

738
741
750
753
755
757
766

19. Process Communication . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 775
Pipes
FIFOs
System V IPC
POSIX Message Queues

776
787
789
806

20. Program Execution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 808
Executable Files
Executable Formats
Execution Domains
The exec Functions

viii

|

Table of Contents

809
824
827
828

A. System Startup . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 835
B. Modules . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 842
Bibliography . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 852
Source Code Index . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 857
Index . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 905

Table of Contents

|

ix

Preface

In the spring semester of 1997, we taught a course on operating systems based on
Linux 2.0. The idea was to encourage students to read the source code. To achieve
this, we assigned term projects consisting of making changes to the kernel and performing tests on the modified version. We also wrote course notes for our students
about a few critical features of Linux such as task switching and task scheduling.
Out of this work—and with a lot of support from our O’Reilly editor Andy Oram—
came the first edition of Understanding the Linux Kernel at the end of 2000, which
covered Linux 2.2 with a few anticipations on Linux 2.4. The success encountered by
this book encouraged us to continue along this line. At the end of 2002, we came out
with a second edition covering Linux 2.4. You are now looking at the third edition,
which covers Linux 2.6.
As in our previous experiences, we read thousands of lines of code, trying to make
sense of them. After all this work, we can say that it was worth the effort. We learned
a lot of things you don’t find in books, and we hope we have succeeded in conveying
some of this information in the following pages.

The Audience for This Book
All people curious about how Linux works and why it is so efficient will find answers
here. After reading the book, you will find your way through the many thousands of
lines of code, distinguishing between crucial data structures and secondary ones—in
short, becoming a true Linux hacker.
Our work might be considered a guided tour of the Linux kernel: most of the significant data structures and many algorithms and programming tricks used in the kernel
are discussed. In many cases, the relevant fragments of code are discussed line by
line. Of course, you should have the Linux source code on hand and should be willing to expend some effort deciphering some of the functions that are not, for sake of
brevity, fully described.

xi
This is the Title of the Book, eMatter Edition
Copyright © 2007 O’Reilly & Associates, Inc. All rights reserved.

On another level, the book provides valuable insight to people who want to know
more about the critical design issues in a modern operating system. It is not specifically addressed to system administrators or programmers; it is mostly for people who
want to understand how things really work inside the machine! As with any good
guide, we try to go beyond superficial features. We offer a background, such as the
history of major features and the reasons why they were used.

Organization of the Material
When we began to write this book, we were faced with a critical decision: should we
refer to a specific hardware platform or skip the hardware-dependent details and
concentrate on the pure hardware-independent parts of the kernel?
Others books on Linux kernel internals have chosen the latter approach; we decided
to adopt the former one for the following reasons:
• Efficient kernels take advantage of most available hardware features, such as
addressing techniques, caches, processor exceptions, special instructions, processor control registers, and so on. If we want to convince you that the kernel
indeed does quite a good job in performing a specific task, we must first tell
what kind of support comes from the hardware.
• Even if a large portion of a Unix kernel source code is processor-independent
and coded in C language, a small and critical part is coded in assembly language. A thorough knowledge of the kernel, therefore, requires the study of a
few assembly language fragments that interact with the hardware.
When covering hardware features, our strategy is quite simple: only sketch the features
that are totally hardware-driven while detailing those that need some software support. In fact, we are interested in kernel design rather than in computer architecture.
Our next step in choosing our path consisted of selecting the computer system to
describe. Although Linux is now running on several kinds of personal computers and
workstations, we decided to concentrate on the very popular and cheap IBM-compatible personal computers—and thus on the 80×86 microprocessors and on some support chips included in these personal computers. The term 80 × 86 microprocessor
will be used in the forthcoming chapters to denote the Intel 80386, 80486, Pentium,
Pentium Pro, Pentium II, Pentium III, and Pentium 4 microprocessors or compatible
models. In a few cases, explicit references will be made to specific models.
One more choice we had to make was the order to follow in studying Linux components. We tried a bottom-up approach: start with topics that are hardwaredependent and end with those that are totally hardware-independent. In fact, we’ll
make many references to the 80×86 microprocessors in the first part of the book,
while the rest of it is relatively hardware-independent. Significant exceptions are
made in Chapter 13 and Chapter 14. In practice, following a bottom-up approach
is not as simple as it looks, because the areas of memory management, process
xii

|

Preface
This is the Title of the Book, eMatter Edition
Copyright © 2007 O’Reilly & Associates, Inc. All rights reserved.

management, and filesystems are intertwined; a few forward references—that is,
references to topics yet to be explained—are unavoidable.
Each chapter starts with a theoretical overview of the topics covered. The material is
then presented according to the bottom-up approach. We start with the data structures needed to support the functionalities described in the chapter. Then we usually move from the lowest level of functions to higher levels, often ending by showing
how system calls issued by user applications are supported.

Level of Description
Linux source code for all supported architectures is contained in more than 14,000 C
and assembly language files stored in about 1000 subdirectories; it consists of
roughly 6 million lines of code, which occupy over 230 megabytes of disk space. Of
course, this book can cover only a very small portion of that code. Just to figure out
how big the Linux source is, consider that the whole source code of the book you are
reading occupies less than 3 megabytes. Therefore, we would need more than 75
books like this to list all code, without even commenting on it!
So we had to make some choices about the parts to describe. This is a rough assessment of our decisions:
• We describe process and memory management fairly thoroughly.
• We cover the Virtual Filesystem and the Ext2 and Ext3 filesystems, although
many functions are just mentioned without detailing the code; we do not discuss other filesystems supported by Linux.
• We describe device drivers, which account for roughly 50% of the kernel, as far
as the kernel interface is concerned, but do not attempt analysis of each specific
driver.
The book describes the official 2.6.11 version of the Linux kernel, which can be
downloaded from the web site http://www.kernel.org.
Be aware that most distributions of GNU/Linux modify the official kernel to implement new features or to improve its efficiency. In a few cases, the source code provided by your favorite distribution might differ significantly from the one described
in this book.
In many cases, we show fragments of the original code rewritten in an easier-to-read
but less efficient way. This occurs at time-critical points at which sections of programs are often written in a mixture of hand-optimized C and assembly code. Once
again, our aim is to provide some help in studying the original Linux code.
While discussing kernel code, we often end up describing the underpinnings of many
familiar features that Unix programmers have heard of and about which they may be
curious (shared and mapped memory, signals, pipes, symbolic links, and so on).

Preface |
This is the Title of the Book, eMatter Edition
Copyright © 2007 O’Reilly & Associates, Inc. All rights reserved.

xiii

Overview of the Book
To make life easier, Chapter 1, Introduction, presents a general picture of what is
inside a Unix kernel and how Linux competes against other well-known Unix systems.
The heart of any Unix kernel is memory management. Chapter 2, Memory Addressing,
explains how 80×86 processors include special circuits to address data in memory and
how Linux exploits them.
Processes are a fundamental abstraction offered by Linux and are introduced in
Chapter 3, Processes. Here we also explain how each process runs either in an unprivileged User Mode or in a privileged Kernel Mode. Transitions between User Mode and
Kernel Mode happen only through well-established hardware mechanisms called interrupts and exceptions. These are introduced in Chapter 4, Interrupts and Exceptions.
In many occasions, the kernel has to deal with bursts of interrupt signals coming from
different devices and processors. Synchronization mechanisms are needed so that all
these requests can be serviced in an interleaved way by the kernel: they are discussed in
Chapter 5, Kernel Synchronization, for both uniprocessor and multiprocessor systems.
One type of interrupt is crucial for allowing Linux to take care of elapsed time; further details can be found in Chapter 6, Timing Measurements.
Chapter 7, Process Scheduling, explains how Linux executes, in turn, every active
process in the system so that all of them can progress toward their completions.
Next we focus again on memory. Chapter 8, Memory Management, describes the
sophisticated techniques required to handle the most precious resource in the system (besides the processors, of course): available memory. This resource must be
granted both to the Linux kernel and to the user applications. Chapter 9, Process
Address Space, shows how the kernel copes with the requests for memory issued by
greedy application programs.
Chapter 10, System Calls, explains how a process running in User Mode makes
requests to the kernel, while Chapter 11, Signals, describes how a process may send
synchronization signals to other processes. Now we are ready to move on to another
essential topic, how Linux implements the filesystem. A series of chapters cover this
topic. Chapter 12, The Virtual Filesystem, introduces a general layer that supports
many different filesystems. Some Linux files are special because they provide trapdoors to reach hardware devices; Chapter 13, I/O Architecture and Device Drivers,
and Chapter 14, Block Device Drivers, offer insights on these special files and on the
corresponding hardware device drivers.
Another issue to consider is disk access time; Chapter 15, The Page Cache, shows
how a clever use of RAM reduces disk accesses, therefore improving system performance significantly. Building on the material covered in these last chapters, we can
now explain in Chapter 16, Accessing Files, how user applications access normal
files. Chapter 17, Page Frame Reclaiming, completes our discussion of Linux memory management and explains the techniques used by Linux to ensure that enough
xiv |

Preface
This is the Title of the Book, eMatter Edition
Copyright © 2007 O’Reilly & Associates, Inc. All rights reserved.

memory is always available. The last chapter dealing with files is Chapter 18, The
Ext2 and Ext3 Filesystems, which illustrates the most frequently used Linux filesystem, namely Ext2 and its recent evolution, Ext3.
The last two chapters end our detailed tour of the Linux kernel: Chapter 19, Process
Communication, introduces communication mechanisms other than signals available to User Mode processes; Chapter 20, Program Execution, explains how user
applications are started.
Last, but not least, are the appendixes: Appendix A, System Startup, sketches out
how Linux is booted, while Appendix B, Modules, describes how to dynamically
reconfigure the running kernel, adding and removing functionalities as needed.
The Source Code Index includes all the Linux symbols referenced in the book; here
you will find the name of the Linux file defining each symbol and the book’s page
number where it is explained. We think you’ll find it quite handy.

Background Information
No prerequisites are required, except some skill in C programming language and perhaps some knowledge of an assembly language.

Conventions in This Book
The following is a list of typographical conventions used in this book:
Constant Width

Used to show the contents of code files or the output from commands, and to
indicate source code keywords that appear in code.
Italic
Used for file and directory names, program and command names, command-line
options, and URLs, and for emphasizing new terms.

How to Contact Us
Please address comments and questions concerning this book to the publisher:
O’Reilly Media, Inc.
1005 Gravenstein Highway North
Sebastopol, CA 95472
(800) 998-9938 (in the United States or Canada)
(707) 829-0515 (international or local)
(707) 829-0104 (fax)
We have a web page for this book, where we list errata, examples, or any additional
information. You can access this page at:
http://www.oreilly.com/catalog/understandlk/
Preface |
This is the Title of the Book, eMatter Edition
Copyright © 2007 O’Reilly & Associates, Inc. All rights reserved.

xv

To comment or ask technical questions about this book, send email to:
bookquestions@oreilly.com
For more information about our books, conferences, Resource Centers, and the
O’Reilly Network, see our web site at:
http://www.oreilly.com

Safari® Enabled
When you see a Safari® Enabled icon on the cover of your favorite technology book, it means the book is available online through the O’Reilly
Network Safari Bookshelf.
Safari offers a solution that’s better than e-books. It’s a virtual library that lets you
easily search thousands of top technology books, cut and paste code samples, download chapters, and find quick answers when you need the most accurate, current
information. Try it for free at http://safari.oreilly.com.

Acknowledgments
This book would not have been written without the precious help of the many students of the University of Rome school of engineering “Tor Vergata” who took our
course and tried to decipher lecture notes about the Linux kernel. Their strenuous
efforts to grasp the meaning of the source code led us to improve our presentation
and correct many mistakes.
Andy Oram, our wonderful editor at O’Reilly Media, deserves a lot of credit. He was
the first at O’Reilly to believe in this project, and he spent a lot of time and energy
deciphering our preliminary drafts. He also suggested many ways to make the book
more readable, and he wrote several excellent introductory paragraphs.
We had some prestigious reviewers who read our text quite carefully. The first edition was checked by (in alphabetical order by first name) Alan Cox, Michael Kerrisk,
Paul Kinzelman, Raph Levien, and Rik van Riel.
The second edition was checked by Erez Zadok, Jerry Cooperstein, John Goerzen,
Michael Kerrisk, Paul Kinzelman, Rik van Riel, and Walt Smith.
This edition has been reviewed by Charles P. Wright, Clemens Buchacher, Erez
Zadok, Raphael Finkel, Rik van Riel, and Robert P. J. Day. Their comments, together
with those of many readers from all over the world, helped us to remove several
errors and inaccuracies and have made this book stronger.
—Daniel P. Bovet
Marco Cesati
July 2005

xvi |

Preface
This is the Title of the Book, eMatter Edition
Copyright © 2007 O’Reilly & Associates, Inc. All rights reserved.

Chapter 1

CHAPTER 1

Introduction

Linux* is a member of the large family of Unix-like operating systems. A relative newcomer experiencing sudden spectacular popularity starting in the late 1990s, Linux
joins such well-known commercial Unix operating systems as System V Release 4
(SVR4), developed by AT&T (now owned by the SCO Group); the 4.4 BSD release
from the University of California at Berkeley (4.4BSD); Digital UNIX from Digital
Equipment Corporation (now Hewlett-Packard); AIX from IBM; HP-UX from
Hewlett-Packard; Solaris from Sun Microsystems; and Mac OS X from Apple Computer, Inc. Beside Linux, a few other opensource Unix-like kernels exist, such as
FreeBSD, NetBSD, and OpenBSD.
Linux was initially developed by Linus Torvalds in 1991 as an operating system for
IBM-compatible personal computers based on the Intel 80386 microprocessor. Linus
remains deeply involved with improving Linux, keeping it up-to-date with various
hardware developments and coordinating the activity of hundreds of Linux developers around the world. Over the years, developers have worked to make Linux available on other architectures, including Hewlett-Packard’s Alpha, Intel’s Itanium,
AMD’s AMD64, PowerPC, and IBM’s zSeries.
One of the more appealing benefits to Linux is that it isn’t a commercial operating
system: its source code under the GNU General Public License (GPL)† is open and
available to anyone to study (as we will in this book); if you download the code (the
official site is http://www.kernel.org) or check the sources on a Linux CD, you will be
able to explore, from top to bottom, one of the most successful modern operating
systems. This book, in fact, assumes you have the source code on hand and can
apply what we say to your own explorations.

* LINUX® is a registered trademark of Linus Torvalds.
† The GNU project is coordinated by the Free Software Foundation, Inc. (http://www.gnu.org); its aim is to
implement a whole operating system freely usable by everyone. The availability of a GNU C compiler has
been essential for the success of the Linux project.

1
This is the Title of the Book, eMatter Edition
Copyright © 2007 O’Reilly & Associates, Inc. All rights reserved.

Technically speaking, Linux is a true Unix kernel, although it is not a full Unix operating system because it does not include all the Unix applications, such as filesystem
utilities, windowing systems and graphical desktops, system administrator commands, text editors, compilers, and so on. However, because most of these programs
are freely available under the GPL, they can be installed in every Linux-based system.
Because the Linux kernel requires so much additional software to provide a useful
environment, many Linux users prefer to rely on commercial distributions, available on
CD-ROM, to get the code included in a standard Unix system. Alternatively, the code
may be obtained from several different sites, for instance http://www.kernel.org. Several distributions put the Linux source code in the /usr/src/linux directory. In the rest of
this book, all file pathnames will refer implicitly to the Linux source code directory.

Linux Versus Other Unix-Like Kernels
The various Unix-like systems on the market, some of which have a long history and
show signs of archaic practices, differ in many important respects. All commercial
variants were derived from either SVR4 or 4.4BSD, and all tend to agree on some
common standards like IEEE’s Portable Operating Systems based on Unix (POSIX)
and X/Open’s Common Applications Environment (CAE).
The current standards specify only an application programming interface (API)—
that is, a well-defined environment in which user programs should run. Therefore,
the standards do not impose any restriction on internal design choices of a compliant kernel.*
To define a common user interface, Unix-like kernels often share fundamental design
ideas and features. In this respect, Linux is comparable with the other Unix-like
operating systems. Reading this book and studying the Linux kernel, therefore, may
help you understand the other Unix variants, too.
The 2.6 version of the Linux kernel aims to be compliant with the IEEE POSIX standard. This, of course, means that most existing Unix programs can be compiled and
executed on a Linux system with very little effort or even without the need for
patches to the source code. Moreover, Linux includes all the features of a modern
Unix operating system, such as virtual memory, a virtual filesystem, lightweight processes, Unix signals, SVR4 interprocess communications, support for Symmetric
Multiprocessor (SMP) systems, and so on.
When Linus Torvalds wrote the first kernel, he referred to some classical books on
Unix internals, like Maurice Bach’s The Design of the Unix Operating System (Prentice Hall, 1986). Actually, Linux still has some bias toward the Unix baseline

* As a matter of fact, several non-Unix operating systems, such as Windows NT and its descendents, are
POSIX-compliant.

2 |

Chapter 1: Introduction
This is the Title of the Book, eMatter Edition
Copyright © 2007 O’Reilly & Associates, Inc. All rights reserved.

