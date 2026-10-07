# Linux Kernel Development (3rd Edition) · Robert Love

## Kernel Subsystems & Core Internals Syllabus

Acquisitions Editor
Mark Taber

Linux Kernel Development
Third Edition

Copyright © 2010 Pearson Education, Inc.
All rights reserved. Printed in the United States of America. This publication is protected by
copyright, and permission must be obtained from the publisher prior to any prohibited reproduction, storage in a retrieval system, or transmission in any form or by any means, electronic, mechanical, photocopying, recording, or likewise.
ISBN-13: 978-0-672-32946-3
ISBN-10: 0-672-32946-8
Library of Congress Cataloging-in-Publication Data:
Love, Robert.
Linux kernel development / Robert Love. — 3rd ed.
p. cm.

Development
Editor
Michael Thurston
Technical Editor
Robert P. J. Day
Managing Editor
Sandra Schroeder
Senior Project
Editor
Tonya Simpson
Copy Editor
Apostrophe Editing
Services

Includes bibliographical references and index.

Indexer
Brad Herriman

ISBN 978-0-672-32946-3 (pbk. : alk. paper) 1. Linux. 2. Operating systems (Computers)
I. Title.

Proofreader
Debbie Williams

QA76.76.O63L674 2010

Publishing
Coordinator
Vanessa Evans

005.4’32—dc22
2010018961
Text printed in the United States on recycled paper at RR Donnelley, Crawfordsville, Indiana.
First printing June 2010
Many of the designations used by manufacturers and sellers to distinguish their products
are claimed as trademarks. Where those designations appear in this book, and the publisher was aware of a trademark claim, the designations have been printed with initial capital
letters or in all capitals.
The author and publisher have taken care in the preparation of this book, but make no
expressed or implied warranty of any kind and assume no responsibility for errors or omissions. No liability is assumed for incidental or consequential damages in connection with or
arising out of the use of the information or programs contained herein.
The publisher offers excellent discounts on this book when ordered in quantity for bulk purchases or special sales, which may include electronic versions and/or custom covers and
content particular to your business, training goals, marketing focus, and branding interests.
For more information, please contact:
U.S. Corporate and Government Sales
(800) 382-3419
corpsales@pearsontechgroup.com
For sales outside the United States please contact:
International Sales
international@pearson.com
Visit us on the Web: informit.com/aw

www.it-ebooks.info

Book Designer
Gary Adair
Compositor
Mark Shirar

❖
For Doris and Helen.
❖

www.it-ebooks.info

Contents at a Glance
1 Introduction to the Linux Kernel

1

2 Getting Started with the Kernel

11

3 Process Management
4 Process Scheduling
5 System Calls

23
41

69

6 Kernel Data Structures

85

7 Interrupts and Interrupt Handlers

113

8 Bottom Halves and Deferring Work

133

9 An Introduction to Kernel Synchronization
10 Kernel Synchronization Methods
11 Timers and Time Management
12 Memory Management

231

13 The Virtual Filesystem

261

14 The Block I/O Layer

175
207

289

15 The Process Address Space

305

16 The Page Cache and Page Writeback
17 Devices and Modules
18 Debugging

363

19 Portability

379

Index

323

337

20 Patches, Hacking, and the Community

Bibliography

161

395

407

411

www.it-ebooks.info

Table of Contents
1 Introduction to the Linux Kernel
History of Unix

1

1

Along Came Linus: Introduction to Linux

3

Overview of Operating Systems and Kernels
Linux Versus Classic Unix Kernels
Linux Kernel Versions

8

The Linux Kernel Development Community
Before We Begin

10

2 Getting Started with the Kernel
Obtaining the Kernel Source
Using Git

11

11

11

Installing the Kernel Source
Using Patches

12

12

The Kernel Source Tree
Building the Kernel

12

13

Configuring the Kernel

14

Minimizing Build Noise

15

Spawning Multiple Build Jobs

16

Installing the New Kernel

16

A Beast of a Different Nature

16

No libc or Standard Headers
GNU C

17

18

Inline Functions

18

Inline Assembly

19

Branch Annotation

19

No Memory Protection

20

No (Easy) Use of Floating Point
Small, Fixed-Size Stack
Importance of Portability
21

www.it-ebooks.info

20

20

Synchronization and Concurrency
Conclusion

4

6

21

21

10

viii

Contents

3 Process Management
The Process

23

23

Process Descriptor and the Task Structure
Allocating the Process Descriptor
Storing the Process Descriptor
Process State

25
26

27

Manipulating the Current Process State
Process Context
Process Creation

31

Copy-on-Write

31

29

32

vfork()

33

The Linux Implementation of Threads
Creating Threads
Kernel Threads

33

34
35

Process Termination

36

Removing the Process Descriptor

37

The Dilemma of the Parentless Task
Conclusion

41

41

Linux’s Process Scheduler
Policy

38

40

4 Process Scheduling
Multitasking

29

29

The Process Family Tree

Forking

24

42

43

I/O-Bound Versus Processor-Bound Processes
Process Priority
Timeslice

44

45

The Scheduling Policy in Action
The Linux Scheduling Algorithm
Scheduler Classes

45

46

46

Process Scheduling in Unix Systems
Fair Scheduling

The Linux Scheduling Implementation
Time Accounting

47

48
50

50

The Scheduler Entity Structure
The Virtual Runtime

50

51

www.it-ebooks.info

43

Contents

Process Selection

52

Picking the Next Task

53

Adding Processes to the Tree

54

Removing Processes from the Tree
The Scheduler Entry Point

57

Sleeping and Waking Up

58

Wait Queues
Waking Up

56

58
61

Preemption and Context Switching
User Preemption
Kernel Preemption

62

62
63

Real-Time Scheduling Policies

64

Scheduler-Related System Calls

65

Scheduling Policy and Priority-Related
System Calls 66
Processor Affinity System Calls
Yielding Processor Time
Conclusion

67

5 System Calls

69

Communicating with the Kernel

69

APIs, POSIX, and the C Library

70

Syscalls

66

66

71

System Call Numbers

72

System Call Performance
System Call Handler

72

73

Denoting the Correct System Call
Parameter Passing

System Call Implementation

74

Implementing System Calls
Verifying the Parameters
System Call Context

73

74
74

75

78

Final Steps in Binding a System Call

79

Accessing the System Call from User-Space
Why Not to Implement a System Call
Conclusion

83

www.it-ebooks.info

82

81

ix

x

Contents

6 Kernel Data Structures
Linked Lists

85

85

Singly and Doubly Linked Lists
Circular Linked Lists

85

86

Moving Through a Linked List

87

The Linux Kernel’s Implementation
The Linked List Structure
Defining a Linked List
List Heads

88

88

89

90

Manipulating Linked Lists

90

Adding a Node to a Linked List

90

Deleting a Node from a Linked List

91

Moving and Splicing Linked List Nodes
Traversing Linked Lists

93

The Basic Approach

93

The Usable Approach

93

Iterating Through a List Backward
Iterating While Removing
Other Linked List Methods
Queues

96

kfifo

97

Creating a Queue

94

95
96

97

Enqueuing Data

98

Dequeuing Data

98

Obtaining the Size of a Queue

98

Resetting and Destroying the Queue
Example Queue Usage
Maps

92

99

99

100

Initializing an idr

101

Allocating a New UID

101

Looking Up a UID

102

Removing a UID

103

Destroying an idr

103

Binary Trees

103

Binary Search Trees

104

Self-Balancing Binary Search Trees
Red-Black Trees
rbtrees

105

105

106

www.it-ebooks.info

Contents

What Data Structure to Use, When
Algorithmic Complexity
Algorithms

109

109

Big-O Notation

109

Big Theta Notation
Time Complexity
Conclusion

108

109
110

111

7 Interrupts and Interrupt Handlers
Interrupts

113

113

Interrupt Handlers

114

Top Halves Versus Bottom Halves

115

Registering an Interrupt Handler
Interrupt Handler Flags

116

116

An Interrupt Example

117

Freeing an Interrupt Handler
Writing an Interrupt Handler
Shared Handlers

118

118

119

A Real-Life Interrupt Handler
Interrupt Context

120

122

Implementing Interrupt Handlers
/proc/interrupts

Interrupt Control

123

126

127

Disabling and Enabling Interrupts

127

Disabling a Specific Interrupt Line

129

Status of the Interrupt System
Conclusion

130

131

8 Bottom Halves and Deferring Work
Bottom Halves

134

Why Bottom Halves?

134

A World of Bottom Halves

135

The Original “Bottom Half”
Task Queues

135

135

Softirqs and Tasklets

136

Dispelling the Confusion

www.it-ebooks.info

137

133

xi

xii

Contents

Softirqs

137

Implementing Softirqs

137

The Softirq Handler

138

Executing Softirqs

138

Using Softirqs

140

Assigning an Index

140

Registering Your Handler
Raising Your Softirq
Tasklets

141

141

142

Implementing Tasklets

142

The Tasklet Structure

142

Scheduling Tasklets

143

Using Tasklets

144

Declaring Your Tasklet

144

Writing Your Tasklet Handler
Scheduling Your Tasklet
ksoftirqd

145

146

The Old BH Mechanism
Work Queues

145

148

149

Implementing Work Queues

149

Data Structures Representing the Threads

149

Data Structures Representing the Work

150

Work Queue Implementation Summary

152

Using Work Queues
Creating Work

153
153

Your Work Queue Handler
Scheduling Work
Flushing Work

153

153
154

Creating New Work Queues

154

The Old Task Queue Mechanism
Which Bottom Half Should I Use?

155
156

Locking Between the Bottom Halves
Disabling Bottom Halves
Conclusion

157

157

159

9 An Introduction to Kernel Synchronization
Critical Regions and Race Conditions
Why Do We Need Protection?
The Single Variable

161

162

162

163

www.it-ebooks.info

Contents

Locking

165

Causes of Concurrency

167

Knowing What to Protect

168

Deadlocks

169

Contention and Scalability
Conclusion

171

172

10 Kernel Synchronization Methods
Atomic Operations

175

175

Atomic Integer Operations

176

64-Bit Atomic Operations

180

Atomic Bitwise Operations

181

Spin Locks

183

Spin Lock Methods

184

Other Spin Lock Methods

186

Spin Locks and Bottom Halves
Reader-Writer Spin Locks
Semaphores

187

188

190

Counting and Binary Semaphores

191

Creating and Initializing Semaphores
Using Semaphores

193

Reader-Writer Semaphores
Mutexes

194

195

Semaphores Versus Mutexes
Spin Locks Versus Mutexes
Completion Variables

197

BKL: The Big Kernel Lock
Sequential Locks

198

200

Preemption Disabling

201

Ordering and Barriers

203

Conclusion

197
197

206

11 Timers and Time Management
Kernel Notion of Time
The Tick Rate: HZ

207

208

208

The Ideal HZ Value

210

Advantages with a Larger HZ

210

Disadvantages with a Larger HZ

www.it-ebooks.info

211

192

xiii

xiv

Contents

Jiffies

212

Internal Representation of Jiffies
Jiffies Wraparound

214

User-Space and HZ

216

Hardware Clocks and Timers
Real-Time Clock
System Timer

216

217
217

The Timer Interrupt Handler
The Time of Day
Timers

213

217

220

222

Using Timers

222

Timer Race Conditions

224

Timer Implementation

224

Delaying Execution

225

Busy Looping

225

Small Delays

226
227

schedule_timeout()

schedule_timeout() Implementation

228

Sleeping on a Wait Queue, with a Timeout
Conclusion

230

12 Memory Management
Pages

231

Zones

233

Getting Pages

231

235

Getting Zeroed Pages
Freeing Pages
kmalloc()

236

237

238

gfp_mask Flags

238

Action Modifiers

239

Zone Modifiers

240

Type Flags
kfree()

241

243

vmalloc()

244

Slab Layer

245

Design of the Slab Layer

246

www.it-ebooks.info

229

