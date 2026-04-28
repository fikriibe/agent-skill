#!/usr/bin/env bash
set -e

SKILLS_SRC="$(cd "$(dirname "$0")/skills" && pwd)"
SKILLS_DEST="$HOME/.claude/skills"

echo "Installing skills to $SKILLS_DEST..."
mkdir -p "$SKILLS_DEST"

for skill_dir in "$SKILLS_SRC"/*/; do
  skill_name="$(basename "$skill_dir")"
  mkdir -p "$SKILLS_DEST/$skill_name"
  cp "$skill_dir/SKILL.md" "$SKILLS_DEST/$skill_name/SKILL.md"
  echo "  ✓ $skill_name"
done

echo ""
echo "Done! $(ls "$SKILLS_DEST" | wc -l | tr -d ' ') skills installed."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "External skills (install manually when needed):"
echo ""
echo "  Stitch skills (requires Stitch MCP):"
echo "    npx skills add google-labs-code/stitch-skills --skill stitch-design --global"
echo "    npx skills add google-labs-code/stitch-skills --skill enhance-prompt --global"
echo "    npx skills add google-labs-code/stitch-skills --skill design-md --global"
echo "    npx skills add google-labs-code/stitch-skills --skill react-components --global"
echo ""
echo "  Taste skill:"
echo "    npx skills add https://github.com/Leonxlnx/taste-skill"
echo ""
echo "  Animate skill:"
echo "    npx skills add https://github.com/delphi-ai/animate-skill --skill animate"
echo ""
echo "  Stitch MCP setup: https://stitch.withgoogle.com/docs/mcp/setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
