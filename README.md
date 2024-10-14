<img src="./images/badge.png?raw=true" width="128">
<div align="left">
  
[![view - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=for-the-badge)](../../wiki/ "Go to project documentation")

</div>

# OttoUpdater
A plugin for [Endstone](https://github.com/EndstoneMC/endstone) to keep your plugins up-to-date automatically.

# Installation
1) Download the latest [release](../../releases).
2) Drag and drop the file ending with `.whl` into your Endstone plugin folder.
3) Restart or reload your server. Enjoy!

### Demo
<img src="./images/demo.png">

# Features
- Scans for plugins with github links.
  - If one is found, and the latest version does not match, the plugin is updated.
***
# For Developers❗
For your plugin to be found by **OttoUpdater**, make sure you complete the following:
- In your `pyproject.toml` file, add/implement the following with your plugin's repo:

  ```
  [project.urls]
  Homepage = "https://github.com/example/repo"
  ```
- Make sure you have at least one release available, and that one is marked as `latest`.
- Make sure the release's tag has a version matchable to the plugin's version (as defined in your `pyproject.toml`).
  - **Acceptable Examples:** `1.0.0`, `beta-0.2`, `v1.3.2-ReleaseC1`
  - **Will NOT Work:** `newbeta`

***
## That's it!
I hope you enjoy using **OttoUpdater!**

If you experience any issues or have a suggestion, please create an [Issue](../../issues), and I'll try to get to it when I can!

# Feature Roadmap
**Feature**|**Status**
:-----:|:-----:
Update Discovery|✅
Automatic Downloading|✅
Configuration|🔷
Automatic Restart/Reload|🔶
Secondary Link Compatability|🔶

✅ - Complete
🔷 - Work in Progress
🔶 - Planned
