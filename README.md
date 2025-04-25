# curseforge-modpack-downloader

> cli tool to automatically download modpacks from CurseForge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This script will let you search modpacks from curseforge, it will list them, including their files, and allow you to select featured files for downloads. After searching for the name of the modpack, the script will guide you to come to a choice of which files to download. The files will then be downloaded to the current directory. Once you have downloaded the files, the entire directory this script is in can be safely deleted if you have no further use for it.

### Installation and usage

##### Pre-requisites

- Python 3.10 or higher, you download it from [python.org](https://www.python.org/downloads/)
- pip

Copy, paste and run this command:

> [!IMPORTANT]
> This command is for linux/macos systems or powershell. If using windows, [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) is recommended.

```bash
git clone https://github.com/nocdn/curseforge-modpack-downloader \
&& cd curseforge-modpack-downloader \
&& python3 -m venv curseforge \
&& source curseforge/bin/activate \
&& pip install requests \
&& clear \
&& python main.py ; deactivate
```

Explanation of the commands:

- `git clone https://github.com/nocdn/curseforge-modpack-downloader`: Clones the repository from GitHub.
- `cd curseforge-modpack-downloader`: Changes the directory to the cloned repository.
- `python3 -m venv curseforge`: Creates a virtual environment named `curseforge`.
- `source curseforge/bin/activate`: Activates the virtual environment.
- `pip install requests`: Installs the `requests` library.
- `python main.py ; deactivate`: Runs the `main.py` script and deactivates the virtual environment after it finishes.

All of these are chained with the `&&` operator to ensure that each command is executed sequentially after the previous one completes successfully, except for the last two, combined with the `;` operator to execute the deactivation command regardless of the success or failure of the main script.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to contribute to this project.
