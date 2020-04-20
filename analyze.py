"""
Script for analyzing an existing Scratch project.
"""

import json
import requests

PROJECT_ID = 383813899

data = requests.get(f"https://projects.scratch.mit.edu/{PROJECT_ID}").json()
print(json.dumps(data, indent=4))
