#!/bin/bash

# Branch cleanup script
echo "🌿 Branch Cleanup Utility"
echo "========================"

# List current branches
echo "Current branches:"
git branch -a

echo ""
echo "Cleaning up merged branches..."

# Delete merged branches (except main/master)
git branch --merged | grep -v "\*\|main\|master" | xargs -n 1 git branch -d

# Clean up remote tracking branches
git remote prune origin

echo "✅ Branch cleanup completed"
