import subprocess
import os
import re

PDF_FILE = "Linux_Mastery_COMPLETE_LIBRARY_9_Volumes_301_pages.pdf"

# Volume ranges in the PDF (1-indexed page numbers)
VOLUME_RANGES = [
    ("volume_01_the_ultimate_edition", 4, 71, "Volume 1: The Ultimate Edition"),
    ("volume_03_practice_workbook", 72, 105, "Volume 3: The Practice Workbook"),
    ("volume_07_bash_configuration_and_scripting", 106, 130, "Volume 7: Bash Configuration & Scripting"),
    ("volume_06_installing_software", 131, 153, "Volume 6: Installing Software & Finding Things"),
    ("volume_04_internals_and_architecture", 154, 181, "Volume 4: Internals & Architecture"),
    ("volume_05_operating_system_theory", 182, 209, "Volume 5: Operating System Theory"),
    ("volume_02_specialist_topics", 210, 241, "Volume 2: Specialist Topics"),
    ("volume_08_kernel_development", 242, 269, "Volume 8: Kernel Development"),
    ("volume_09_kernel_deep_guide", 270, 301, "Volume 9: Kernel Development Complete Guide")
]

def clean_text(text):
    # Remove form feeds and fix spacing
    lines = text.splitlines()
    clean_lines = []
    for l in lines:
        if "Linux Mastery — From User to Expert" in l or re.match(r"^Page \d+$", l.strip()):
            continue
        clean_lines.append(l)
    return "\n".join(clean_lines).strip()

def main():
    print("Extracting full text from 9 volumes book...")
    res = subprocess.run(["pdftotext", PDF_FILE, "-"], capture_output=True, text=True)
    pages = res.stdout.split("\x0c")
    print(f"Total extracted pages: {len(pages)}")

    for folder_name, start_p, end_p, vol_title in VOLUME_RANGES:
        out_dir = os.path.join("curriculum", folder_name)
        os.makedirs(out_dir, exist_ok=True)
        
        vol_pages = pages[start_p - 1 : end_p]
        vol_text = "\n\n".join(vol_pages)
        
        # Split into chapters based on numbered headings like "1. ", "2. ", "Section 1", etc.
        # Save a master complete volume markdown file
        master_file = os.path.join(out_dir, "00_complete_volume.md")
        with open(master_file, "w", encoding="utf-8") as f:
            f.write(f"# {vol_title}\n\n" + clean_text(vol_text))
        print(f"  -> Generated {master_file} ({len(vol_text)} characters)")

        # Split into individual chapters
        chunks = re.split(r'\n(?=(?:(?:Chapter\s+\d+|Section\s+\d+|\d+\.)\s+[A-Z]))', vol_text)
        ch_idx = 1
        for chunk in chunks:
            chunk_clean = clean_text(chunk)
            if len(chunk_clean) < 150:
                continue
            first_line = chunk_clean.splitlines()[0][:60]
            slug = re.sub(r'[^a-zA-Z0-9_]+', '_', first_line.lower()).strip('_')
            ch_filename = os.path.join(out_dir, f"ch{ch_idx:02d}_{slug[:35]}.md")
            with open(ch_filename, "w", encoding="utf-8") as f:
                f.write(chunk_clean)
            ch_idx += 1
        print(f"     Split into {ch_idx - 1} chapters.")

if __name__ == "__main__":
    main()
