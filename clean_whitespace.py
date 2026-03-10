import os

file_path = r'C:\Users\Abbas\.gemini\antigravity\scratch\entity_resolution_project\dashboard.py'
temp_path = r'C:\Users\Abbas\.gemini\antigravity\scratch\entity_resolution_project\dashboard_clean.py'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

clean_lines = []
last_was_empty = False

for line in lines:
    stripped = line.strip()
    if stripped:
        clean_lines.append(line)
        last_was_empty = False
    elif not last_was_empty:
        clean_lines.append(line)
        last_was_empty = True

with open(temp_path, 'w', encoding='utf-8') as f:
    f.writelines(clean_lines)

print(f"Original lines: {len(lines)}")
print(f"Cleaned lines: {len(clean_lines)}")
