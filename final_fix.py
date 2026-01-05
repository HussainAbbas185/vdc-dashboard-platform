
import os

file_path = r'c:\Users\Abbas\.gemini\antigravity\scratch\entity_resolution_project\dashboard.py'
with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Look for the damaged section
start_index = -1
for i, line in enumerate(lines):
    if 'if st.button("Add to System (Instant)"): ' in line: # Try to find the button line
        pass 

# Actually, I'll just rewrite the whole section from line 1024
new_section = [
    '        if st.button("Add to System (Instant)"):\n',
    '            import requests\n',
    '            import io\n',
    '            import os\n',
    '            \n',
    '            with st.spinner("🔗 Linking video..."):\n',
    '                try:\n'
]

# The damage is between 1024 and 1030 (1-indexed)
# Index 1023 to 1029
lines[1023:1030] = new_section

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Final fix successful")
