I found the issue: both `google-chrome.list` and `microsoft-edge.list` were pointing to Google Chrome's repository. I've fixed `microsoft-edge.list` to use Microsoft's Edge repository instead.

**What was wrong:**

- Both files had: `deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main`

**What I fixed:**

- `microsoft-edge.list` now has: `deb [arch=amd64] https://packages.microsoft.com/repos/edge/ stable main`

This should resolve the duplicate configuration warnings. After copying the corrected file to `/etc/apt/sources.list.d/microsoft-edge.list`, run `sudo apt update` again; the warnings should be gone.

**Note:** Make sure the Microsoft GPG key is installed. If needed, you can add it with:

```bash
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-edge-stable-archive-keyring.gpg
```

But since this is an automatically configured file, the Microsoft Edge installer likely already handles the GPG key setup.
