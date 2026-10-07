import subprocess
import os

os.makedirs("curriculum/tlpi_systems_programming", exist_ok=True)
os.makedirs("curriculum/kernel_subsystems_lkd_ulk3", exist_ok=True)

# 1. Extract TLPI Table of Contents & Structure
print("Extracting TLPI TOC...")
tlpi_toc = subprocess.run(["pdftotext", "-f", "10", "-l", "35", "The Linux Programming Interface.pdf", "-"], capture_output=True, text=True).stdout

with open("curriculum/tlpi_systems_programming/00_tlpi_complete_roadmap.md", "w", encoding="utf-8") as f:
    f.write("# The Linux Programming Interface (TLPI) · Michael Kerrisk\n\n")
    f.write("## Complete 64-Chapter Systems Programming Syllabus & Reference\n\n")
    f.write(tlpi_toc)

# 2. Extract Robert Love LKD TOC
print("Extracting Robert Love LKD TOC...")
lkd_toc = subprocess.run(["pdftotext", "-f", "5", "-l", "15", "linux_kernel_development.pdf", "-"], capture_output=True, text=True).stdout

with open("curriculum/kernel_subsystems_lkd_ulk3/00_lkd_complete_roadmap.md", "w", encoding="utf-8") as f:
    f.write("# Linux Kernel Development (3rd Edition) · Robert Love\n\n")
    f.write("## Kernel Subsystems & Core Internals Syllabus\n\n")
    f.write(lkd_toc)

# 3. Extract Bovet & Cesati ULK3 TOC
print("Extracting Bovet & Cesati ULK3 TOC...")
ulk_toc = subprocess.run(["pdftotext", "-f", "7", "-l", "20", "ulk3.pdf", "-"], capture_output=True, text=True).stdout

with open("curriculum/kernel_subsystems_lkd_ulk3/01_ulk3_architecture_roadmap.md", "w", encoding="utf-8") as f:
    f.write("# Understanding the Linux Kernel (3rd Edition) · Bovet & Cesati\n\n")
    f.write("## Hardware Architecture, Paging, Interrupts & VFS Syllabus\n\n")
    f.write(ulk_toc)

print("TLPI and Kernel roadmaps generated successfully!")
