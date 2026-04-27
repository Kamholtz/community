# My Changes

## (1) Edit

### (1.1) Replace Edit Action Cut With Carve

See header

## (2) Agent Skills

### (2.1) Flatten Community Skill Layout

Moved active Talon agent skills from `.agents/skills/skills/` to `.agents/skills/` and removed redundant or empty skill directories. General Talon syntax/customization guidance is now expected to come from the canonical `~/.agents/skills/talon-skill` skill, while this repository keeps local Talon workflow/debugging skills.

### (2.2) Add Agent Skill Gates

Added `.agents/scripts/check_talon_config.py` and `.githooks/pre-commit` to enforce skill metadata, changed/staged text linting, Python compilation, and pytest when available. Updated agent docs to explain when to use each Talon skill and how to run the validation workflow.
