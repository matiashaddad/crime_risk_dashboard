import os
import sys

# Import dashboard.py
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import Dash-App and load data
from src.dashboard import app, get_data_from_db

# Output root
OUTPUT_FILENAME = 'index.html'
output_path = os.path.join(os.path.dirname(__file__), OUTPUT_FILENAME)

print(f"Exporting Dash to {OUTPUT_FILENAME}...")

try:
    # Load data before export
    get_data_from_db()

    # 1. Generate string-HTML
    html_content = app.index()

    # 2. Write string-HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Export Successful")
    print("'index.html' ready for GitHub Pages.")

except Exception as e:
    print(f"Error while exporting: {e}")
