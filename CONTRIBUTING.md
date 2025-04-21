# Contributing to curseforge-modpack-downloader

> guidelines for contributing to this project

Firstly, thank you for your interest in contributing to the project. Your contributions are always highly appreciated :)

### How to report a bug

1. Search existing [issues](https://github.com/nocdn/curseforge-modpack-downloader/issues) to see if it’s already known.
2. If not, open a new issue with:
   - A clear and descriptive title.
   - Steps to reproduce.
   - Expected vs actual behavior.
   - Any relevant logs or screenshots.


### How to suggest an enhancement

1. Check if a similar feature request already exists.
2. Open a new issue titled “Enhancement: …” and include:
   - A summary of the change.
   - Why it would be useful.
   - Any ideas for implementation.

### How to contribute code

1. Fork the repo and clone it locally:
   ```bash
   git clone https://github.com/nocdn/curseforge-modpack-downloader.git
   ```
2. Create a new branch:
   ```bash
   git checkout -b feature/short-description
   ```
3. Make your changes.
   - follow the existing style:
     - comments in lowercase shorthand, no trailing full stop
     - meaningful variable names
     - small, focused commits
4. Test the script in a virtual env to verify nothing breaks:
   ```bash
   python main.py
   ```
5. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add XYZ functionality"
   ```
6. Push and open a pull request back to `main`.
7. Fill in the PR descriptively with what you changed and why.


### Coding style

- target **Python 3.10+**
- keep it simple and readable
- use `requests` for HTTP calls
- write comments in lowercase and shorthand, e.g.
  ```python
  # ensure file is text-based using file command
  ```

### License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).


Once again, thank you for your contribution!
