from talon import Module

mod = Module()

# Matches "Work" profile (assuming title includes "Work")
mod.apps.edge_fp = r"""
app: microsoft_edge
and title: /FP/
"""

# Matches "Personal" profile
mod.apps.edge_chatgpt = r"""
app: microsoft_edge
and title: /ChatGPT/
"""

# Add more as neede 