#!/usr/bin/env bash
# Deploy local site/ directory to GitHub Pages without committing to current branch
# Uses a temporary branch and git worktree to avoid affecting your working directory

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# Check if site/ exists
if [ ! -d "site" ]; then
  echo "❌ Error: site/ directory not found. Please build the site first:"
  echo "   just build"
  exit 1
fi

# Get repo info
REPO_OWNER=$(gh repo view --json owner -q '.owner.login')
REPO_NAME=$(gh repo view --json name -q '.name')
BRANCH_NAME="gh-pages-deploy-$(date +%s)"

echo "🚀 Deploying site/ to GitHub Pages (no commits to current branch)"

# Create a temporary worktree in a temp directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf '$TEMP_DIR'" EXIT

echo "📦 Creating temporary worktree..."
git worktree add "$TEMP_DIR" -b "$BRANCH_NAME" 2>/dev/null || {
  # Branch might already exist, try to remove it
  git branch -D "$BRANCH_NAME" 2>/dev/null || true
  git worktree add "$TEMP_DIR" -b "$BRANCH_NAME"
}

# Copy site/ to the worktree
echo "📋 Copying site/ directory..."
rm -rf "$TEMP_DIR/site"
cp -r site "$TEMP_DIR/"

# Commit and push from the worktree
cd "$TEMP_DIR"
git add site/
git commit -m "chore: deploy site/ to GitHub Pages [skip ci]" || {
  echo "⚠️  No changes to commit (site/ is identical)"
}

echo "⬆️  Pushing to temporary branch..."
git push origin "$BRANCH_NAME" --force

# Clean up worktree
cd "$REPO_ROOT"
git worktree remove "$TEMP_DIR" 2>/dev/null || rm -rf "$TEMP_DIR"
git branch -D "$BRANCH_NAME" 2>/dev/null || true

# Trigger the workflow (it will use the pushed branch)
echo "🎯 Triggering deployment workflow..."
gh workflow run deploy-site.yml --ref "$BRANCH_NAME" || {
  echo "⚠️  Workflow trigger failed, but files are pushed. You can trigger manually:"
  echo "   https://github.com/$REPO_OWNER/$REPO_NAME/actions/workflows/deploy-site.yml"
}

echo ""
echo "✅ Deployment initiated!"
echo "   Branch: $BRANCH_NAME"
echo "   Status: https://github.com/$REPO_OWNER/$REPO_NAME/actions"
echo ""
echo "💡 The temporary branch will be cleaned up automatically after deployment."
