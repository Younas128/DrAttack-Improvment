# Stop tracking `api_keys/` and local credentials

- **What:** Documented the action to stop tracking `api_keys/` and other local secrets.
- **Why:** Prevent exposure of API keys and credentials on GitHub.
- **Files:** `api_keys/` (directory)
- **Next steps:** Run `git rm --cached -r api_keys` then commit and push. If keys were previously committed, consider history rewrite with `git filter-repo` or BFG.
