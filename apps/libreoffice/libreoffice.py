from talon import Context, Module

# --- App definitions ---
mod = Module()

# LibreOffice Writer
mod.apps.libreoffice_writer = """
os: linux
and app.name: Soffice
"""

# LibreOffice Calc
mod.apps.libreoffice_calc = """
os: linux
and app.name: Soffice
title: /Calc/
"""

# LibreOffice Impress
mod.apps.libreoffice_impress = """
os: linux
and app.name: Soffice
title: /Impress/
"""

# General LibreOffice (matches all variants)
mod.apps.libreoffice = """
os: linux
and app.name: Soffice
"""

# Context matching
ctx = Context()
ctx.matches = r"""
app: libreoffice
"""


# --- Define actions ---
@mod.action_class
class LibreOfficeActions:
    def libreoffice_next_paragraph():
        """Move to next paragraph"""

    def libreoffice_previous_paragraph():
        """Move to previous paragraph"""

    def libreoffice_select_paragraph():
        """Select current paragraph"""

    def libreoffice_next_sentence():
        """Move to next sentence"""

    def libreoffice_previous_sentence():
        """Move to previous sentence"""

    def libreoffice_select_sentence():
        """Select current sentence"""

    def libreoffice_select_word():
        """Select current word"""

    def libreoffice_start_of_document():
        """Go to start of document"""

    def libreoffice_end_of_document():
        """Go to end of document"""

    def libreoffice_select_to_start():
        """Select from cursor to start of document"""

    def libreoffice_select_to_end():
        """Select from cursor to end of document"""
