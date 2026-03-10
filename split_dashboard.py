import os

def split_dashboard():
    dashboard_path = r'C:\Users\Abbas\.gemini\antigravity\scratch\entity_resolution_project\dashboard.py'
    ui_dir = r'C:\Users\Abbas\.gemini\antigravity\scratch\entity_resolution_project\src\ui'
    
    if not os.path.exists(ui_dir):
        os.makedirs(ui_dir)

    with open(dashboard_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Define boundaries (approximate based on my earlier research)
    # I'll use markers like "elif page ==" to find the sections
    sections = {}
    current_page = "Setup"
    current_lines = []

    for line in lines:
        if line.strip().startswith('elif page ==') or line.strip().startswith('if page =='):
            sections[current_page] = current_lines
            # Extract page name
            try:
                current_page = line.split('"')[1]
            except:
                current_page = "Unknown"
            current_lines = [line]
        else:
            current_lines.append(line)
    
    sections[current_page] = current_lines

    # Now write them to modules
    # Mapping pages to files
    mapping = {
        "Global Command Center": "command_center.py",
        "Global Tech News": "tech_news.py",
        "Quantum Orchestrator": "quantum_ui.py",
        "Legacy Dashboard": "data_mgmt.py",
        "Real-Time Monitor": "data_mgmt.py",
        "Data Lab & Mining": "data_mgmt.py",
        "Connect Database": "data_mgmt.py",
        "Venture Intelligence": "intelligence.py",
        "Social Market Intelligence": "intelligence.py",
        "Executive Intelligence Hub": "intelligence.py",
        "Extraction Engine": "tools_ui.py",
        "File Utilities": "tools_ui.py",
        "Visualization Studio": "tools_ui.py",
        "Workflow Automation": "tools_ui.py",
        "Molecular DNA Archival": "advanced_ui.py",
        "Digital Twin Controller": "advanced_ui.py"
    }

    # I'll just save EVERY section to its own render function in its own file
    for page, content in sections.items():
        if page == "Setup": continue
        
        target_file = mapping.get(page, "misc_ui.py")
        full_target = os.path.join(ui_dir, target_file)
        
        func_name = "render_" + page.lower().replace(" ", "_").replace("&", "and").replace("-", "_")
        
        # indent content
        indented_content = "".join(["    " + l if l.strip() else l for l in content[1:]])
        
        with open(full_target, 'a', encoding='utf-8') as f:
            f.write(f"\ndef {func_name}():\n")
            f.write(indented_content)
            f.write("\n")

    print("Split complete.")

if __name__ == "__main__":
    split_dashboard()
