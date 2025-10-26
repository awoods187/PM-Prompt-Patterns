# Git History Rewrite Guide

## Current Situation Analysis

**Good News:** No work email (`andy@cockroachlabs.com`) found in your git history!

### Current Email Distribution:

| Email | Usage | Count |
|-------|-------|-------|
| `awoods187@users.noreply.github.com` | ✅ Most commits | ~20+ |
| `andrew.scott.woods@gmail.com` | ⚠️ 2 merge commits | 2 |
| `andy@cockroachlabs.com` | ❌ Not found | 0 |

### Commits Using Gmail:
```
4472b9b - Merge pull request #3 from awoods187/prompt-library-v1
23e9d98 - Merge pull request #1 from awoods187/add-readme
```

**Note:** These are GitHub-created merge commits, not commits you authored directly.

---

## ✅ Recommendation: NO ACTION NEEDED

Your repository is already properly configured:
- ✅ Personal email configured: `awoods187@users.noreply.github.com`
- ✅ No work email in commit history
- ✅ All commits will show as "awoods187" on GitHub
- ✅ Work is clearly independent from employer

**The 2 Gmail commits are harmless** - they're old merge commits created by GitHub's web interface.

---

## Options

### Option 1: Leave As-Is (Recommended)
**Why:** Your history is already clean. The Gmail address is your personal email, not your work email.

**Action:** None needed!

---

### Option 2: Standardize Everything to GitHub Privacy Email

If you want to change the 2 Gmail commits to use `awoods187@users.noreply.github.com`:

#### ⚠️ WARNINGS BEFORE YOU PROCEED:

1. **History Rewrite:** This changes commit SHAs (identifiers)
2. **Force Push Required:** You'll need to force push to update remote
3. **Collaborators Affected:** Anyone who has pulled your branch will need to re-pull
4. **PR Updates:** The PR will be updated automatically after force push
5. **Cannot Undo Easily:** Make a backup first!

---

## Method 1: Automated Script (Easiest)

I've created `rewrite-history.sh` for you:

```bash
# Make it executable
chmod +x rewrite-history.sh

# Run it
./rewrite-history.sh
```

**What it does:**
1. Shows you what will change
2. Asks for confirmation
3. Creates a backup branch automatically
4. Rewrites history to use `awoods187@users.noreply.github.com`
5. Gives you next steps

---

## Method 2: Manual Commands (Full Control)

### Step 1: Create Backup
```bash
# Create backup branch
git branch improve_repo-backup-$(date +%Y%m%d)

# Verify backup exists
git branch -a | grep backup
```

### Step 2: Rewrite History (Choose One)

#### Option A: Using git filter-branch (older but widely available)

```bash
git filter-branch --env-filter '
OLD_EMAIL="andrew.scott.woods@gmail.com"
CORRECT_NAME="Andy Woods"
CORRECT_EMAIL="awoods187@users.noreply.github.com"

# Update author
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi

# Update committer
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
```

#### Option B: Using git-filter-repo (modern, faster)

First install git-filter-repo:
```bash
# macOS
brew install git-filter-repo

# Or with pip
pip install git-filter-repo
```

Then run:
```bash
git filter-repo --mailmap <(cat <<EOF
Andy Woods <awoods187@users.noreply.github.com> Andy Woods <andrew.scott.woods@gmail.com>
Andy Woods <awoods187@users.noreply.github.com> <andrew.scott.woods@gmail.com>
EOF
)
```

### Step 3: Verify Changes

```bash
# Check all unique emails (should only show awoods187@users.noreply.github.com)
git log --all --pretty=format:"%ae" | sort -u

# Check the 2 commits that were changed
git log --oneline --all | grep -E "(4472b9b|23e9d98)"

# View full details of changed commits
git log --pretty=fuller | head -50
```

### Step 4: Force Push to Update PR

```bash
# Force push with safety check (recommended)
git push --force-with-lease origin improve_repo

# Or regular force push (less safe)
# git push --force origin improve_repo
```

**What `--force-with-lease` does:**
- Safer than `--force`
- Fails if someone else pushed changes to the branch
- Prevents accidentally overwriting others' work

---

## Method 3: Rebase Alternative (Cleanest for Recent Commits)

If you only want to change commits on your current branch:

```bash
# Interactive rebase from main branch
git rebase -i main --exec 'git commit --amend --reset-author --no-edit'
```

This will:
1. Rebase all commits on `improve_repo` from `main`
2. Reset author to your current git config
3. Keep all commit messages

---

## Verification After Rewrite

### Check Email Consistency:
```bash
# Should only show awoods187@users.noreply.github.com
git log --all --pretty=format:"%an <%ae>" | sort -u
git log --all --pretty=format:"%cn <%ce>" | sort -u
```

### Check Specific Commits:
```bash
# View author and committer for recent commits
git log --pretty=fuller -5
```

### Verify on GitHub:
1. Go to your PR: https://github.com/awoods187/PM-Prompt-Patterns/pull/4
2. Check commit author shows as "awoods187"
3. Verify no work email visible

---

## Undo Instructions

If something goes wrong:

```bash
# Find your backup branch
git branch -a | grep backup

# Reset to backup (replace with your backup branch name)
git reset --hard improve_repo-backup-20251026

# Force push the old state back
git push --force origin improve_repo
```

---

## Common Issues & Solutions

### Issue 1: "filter-branch has been deprecated"
**Solution:** Use git-filter-repo instead (Method 2, Option B)

### Issue 2: Force push rejected
**Solution:**
```bash
# Make sure you're on the right branch
git branch --show-current

# Use --force instead of --force-with-lease
git push --force origin improve_repo
```

### Issue 3: PR shows old commits
**Solution:** Wait a few minutes for GitHub to update, then refresh the PR page

### Issue 4: "Cannot rewrite published commits"
This is just a warning. If you're sure:
```bash
# Add -f flag to force it
git filter-branch -f --env-filter '...'
```

---

## Summary

### Your Current Status:
- ✅ Repository: `awoods187/PM-Prompt-Patterns`
- ✅ Branch: `improve_repo`
- ✅ Current email: `awoods187@users.noreply.github.com` (correct)
- ✅ Work email: NOT FOUND in history ✅
- ⚠️ Gmail email: Found in 2 old merge commits (harmless)

### My Recommendation:
**DO NOTHING** - Your history is already clean and professional.

### If You Still Want to Standardize:
1. Use the automated script: `./rewrite-history.sh`
2. Or follow Method 2 (Manual Commands)
3. Force push with: `git push --force-with-lease origin improve_repo`

---

## Questions?

### "Will this affect my GitHub contributions graph?"
Yes, commit dates are preserved but SHAs change. Your contribution count stays the same.

### "Will this show up as activity from my employer?"
No - there's no work email in your history. All commits show your personal identity.

### "Do I need to do this?"
No - your history is already clean. This is optional standardization only.

### "What's the risk?"
Low risk if you:
- Create a backup first ✅
- Only push to your own fork ✅
- Use `--force-with-lease` ✅

---

**Last updated:** 2025-10-26
