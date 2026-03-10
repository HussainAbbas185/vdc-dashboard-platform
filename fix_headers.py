import os

ui_dir = r'C:\Users\Abbas\.gemini\antigravity\scratch\entity_resolution_project\src\ui'
for filename in os.listdir(ui_dir):
    if filename.endswith('.py'):
        path = os.path.join(ui_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "import streamlit as st" not in content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write("import streamlit as st\nimport pandas as pd\nimport duckdb\nimport os\nimport time\nimport altair as alt\n")
                # Add some common imports from the original dashboard if they were there
                f.write("from src.audit_logger import log_action\n")
                f.write(content)

print("Header injection complete.")
