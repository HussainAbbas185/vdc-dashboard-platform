
import os

file_path = r'c:\Users\Abbas\.gemini\antigravity\scratch\entity_resolution_project\dashboard.py'
with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Line numbers are 1-indexed
lines[833] = '    st.title("📊 Executive Intelligence Hub")\n'
lines[1024] = '            with st.spinner("🔗 Linking video..."):\n'

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Replacement successful")
