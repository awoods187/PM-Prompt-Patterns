#!/bin/bash
# Script to standardize all git commits to use GitHub privacy email
# WARNING: This rewrites git history and requires force push

set -e

echo "🔍 Git History Rewrite Script"
echo "=============================="
echo ""
echo "This will rewrite ALL commits to use:"
echo "  Name:  Andy Woods"
echo "  Email: awoods187@users.noreply.github.com"
echo ""
echo "⚠️  WARNING: This rewrites git history!"
echo "⚠️  You will need to force push after this."
echo ""

# Show what will be changed
echo "Commits that will be updated:"
git log --all --pretty=format:"%h - %an <%ae> - %s" | grep -v "awoods187@users.noreply.github.com" | head -20

echo ""
echo ""
read -p "Do you want to proceed? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "🔄 Rewriting git history..."
echo ""

# Backup current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "📦 Creating backup branch: ${CURRENT_BRANCH}-backup-$(date +%Y%m%d-%H%M%S)"
git branch "${CURRENT_BRANCH}-backup-$(date +%Y%m%d-%H%M%S)"

# Method 1: Using git filter-branch (older, more compatible)
git filter-branch --env-filter '
OLD_EMAIL_1="andrew.scott.woods@gmail.com"
OLD_EMAIL_2="andy@cockroachlabs.com"
CORRECT_NAME="Andy Woods"
CORRECT_EMAIL="awoods187@users.noreply.github.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL_1" ] || [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL_2" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL_1" ] || [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL_2" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags

echo ""
echo "✅ Git history rewritten successfully!"
echo ""
echo "📊 Verification:"
git log --all --pretty=format:"%ae" | sort -u
echo ""
echo ""
echo "Next steps:"
echo "1. Review the changes: git log"
echo "2. Force push to update PR: git push --force-with-lease origin ${CURRENT_BRANCH}"
echo ""
echo "⚠️  To undo this change, run:"
echo "   git reset --hard ${CURRENT_BRANCH}-backup-$(date +%Y%m%d-%H%M%S)"
