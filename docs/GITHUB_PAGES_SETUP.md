# GitHub Pages & Custom Domain Setup Guide

## Status
- ✅ **GitHub Pages branch:** `gh-pages` pushed with site files (`index.html`, `images/`, `static/`, `CNAME`)
- ⏳ **Pages configuration:** Needs manual setup via GitHub web interface
- ⏳ **DNS setup:** Pending (see instructions below)
- ❌ **Live site:** Currently returns 404 (Pages not yet enabled in repo settings)

## Step 1: Enable GitHub Pages (via Web Interface)

1. Go to: https://github.com/Younas128/DrAttack-Improvment/settings/pages
2. Under **Source**, select:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
3. Under **Custom domain**, enter: `DrAttack.io` (GitHub will look for the `CNAME` file automatically)
4. Click **Save**
5. Wait 1–2 minutes for GitHub to deploy (you'll see a blue banner "Your site is published at...")
6. Verify by visiting: https://younas128.github.io/DrAttack-Improvment/

## Step 2: Configure DNS for Custom Domain (DrAttack.io)

**Important:** Do this AFTER Pages is enabled and publishing successfully.

### Option A: A Records (Recommended for apex domain)

Add these **four A records** at your domain registrar:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | DrAttack.io (or @) | 185.199.108.153 | Default |
| A | DrAttack.io (or @) | 185.199.109.153 | Default |
| A | DrAttack.io (or @) | 185.199.110.153 | Default |
| A | DrAttack.io (or @) | 185.199.111.153 | Default |

### Option B: ALIAS/ANAME Record (if your registrar supports it)

| Type | Name | Value | TTL |
|------|------|-------|-----|
| ALIAS | DrAttack.io (or @) | younas128.github.io | Default |

### For www Subdomain (Optional but Recommended)

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | www | younas128.github.io | Default |

## Step 3: Verify DNS Propagation

After adding DNS records, wait 5 minutes to 48 hours for propagation. Check status:

```powershell
nslookup DrAttack.io
# Should return: 185.199.10x.15x addresses
```

## Step 4: Enable HTTPS (Automatic)

Once DNS is configured:
1. Return to https://github.com/Younas128/DrAttack-Improvment/settings/pages
2. Scroll to **HTTPS** section
3. Check the box: **Enforce HTTPS**
4. GitHub will provision an SSL certificate (automatic, free via Let's Encrypt)
5. Wait 1–5 minutes

## Step 5: Verify Live Site

Once DNS propagates and HTTPS is enabled:

```powershell
# Test both URLs
Invoke-WebRequest -Uri "https://DrAttack.io/" | Select-Object StatusCode
Invoke-WebRequest -Uri "https://younas128.github.io/DrAttack-Improvment/" | Select-Object StatusCode
# Both should return: 200 OK
```

Visit in browser:
- https://DrAttack.io → Should show DrAttack web interface
- https://www.DrAttack.io → Should redirect to https://DrAttack.io

## Troubleshooting

### 404 Error on Pages Site

**Possible causes:**
1. Pages not enabled in Settings → Pages
2. Branch set to `main` instead of `gh-pages`
3. Folder set to `/docs` instead of `/ (root)`
4. `index.html` not at repository root on `gh-pages`

**Fix:**
- Verify branch is `gh-pages` at Settings → Pages
- Check that `index.html` is in the repository root:
  ```powershell
  git ls-tree -r origin/gh-pages | grep index.html
  # Should output: index.html
  ```

### DNS Not Resolving

**Check current DNS:**
```powershell
nslookup DrAttack.io
# Should return A records (185.199.10x.15x)
```

**Propagation time:** DNS changes can take 5 minutes to 48 hours.

### HTTPS Certificate Not Provisioning

**Requirement:** Custom domain must be properly configured in DNS before HTTPS cert can be issued.

**Check status:**
1. Go to Settings → Pages
2. Look for "Your site is live at..." message
3. HTTPS button appears after DNS resolves and domain is verified

## Next Steps (After Setup Complete)

1. **Test mobile & desktop** responsiveness
2. **Check asset loading:** Open browser DevTools (F12) and verify:
   - `images/` load without 404
   - `static/css/` and `static/js/` files load
   - No mixed content warnings (HTTPS only)
3. **Update project README** with live site URL
4. **Share:** DrAttack.io is now your project's public face!

---

**Questions?**  
Refer to [GitHub Pages Documentation](https://docs.github.com/en/pages) or re-run the troubleshooting commands above.
