# Commit and push housekeeping changes

- **What:** Commit `.gitignore` and docs, untrack `api_keys/`, and push to the remote repository.
- **Why:** Keep repository clean and avoid pushing secrets.
- **Recommended commands:**

```powershell
cd "C:\Users\Cyber Lab\Downloads\ML SEC\DrAttack-Improvment"
# Untrack keys if previously committed
git rm --cached -r api_keys || echo "api_keys not tracked"
# Stage changes
git add .gitignore docs/changes/*.md
git add -A
git commit -m "chore: add .gitignore and docs; stop tracking api_keys" || echo "no changes to commit"
# If remote exists, push; otherwise add remote and push
git push
```

- **Caveats:** If API keys were in history, use `git filter-repo` or BFG to purge them and rotate any exposed keys.
