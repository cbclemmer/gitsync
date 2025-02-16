# Git Sync

A Python script to synchronize (clone or update) all your non-fork GitHub repositories locally. This project fetches repositories from your GitHub account and ensures that each one is either cloned or pulled to a specified folder.

## Features

- **Fetch GitHub username**: Automatically determine your GitHub username from a personal access token.
- **List repositories**: Retrieve and iterate through all repositories in your GitHub account (excluding forks by default, but you can adjust the query as needed).
- **Clone or update**: 
  - **Clone** any missing repositories to the specified local directory.
  - **Pull** changes on any existing local repositories to stay up to date.
- **Graceful error handling**: Detects invalid Git repositories and, if needed, reclones them cleanly.

## Requirements

- **Python 3.7+**  
- **Pip packages**:
  - [requests](https://pypi.org/project/requests/)
  - [GitPython](https://pypi.org/project/GitPython/)

To install dependencies:
```bash
pip install requests GitPython
```

## Setup

1. **Clone or download this repository** (the script itself).
2. **Create a `config.json` file** in the same directory as the script:
   ```json
   {
     "github_api_key": "YOUR_PERSONAL_ACCESS_TOKEN"
   }
   ```
   - Replace `"YOUR_PERSONAL_ACCESS_TOKEN"` with a [GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). Make sure it has the appropriate scopes (e.g., `repo` scope for private repositories).
3. **Create or choose a local directory** where all repositories will be stored (the script defaults to a directory named `github`).

## Usage

1. **Run the main script**:
   ```bash
   python gitsync.py
   ```
   or:
   ```bash
   python gitsync.py
   ```

2. **What the script does**:
   - Reads your GitHub token from `config.json`.
   - Fetches your GitHub username using the token.
   - Searches for your repositories (adjust the search query in `get_repos` if desired).
   - Clones each repository if it’s not present locally.
   - Pulls the latest changes if the repository is already present.

3. **Check the output**:
   - As each repository is processed, you'll see status messages in the console.

## Customizing

- **Search Query**: In `get_repos`, the default search query includes `fork:true`. You can remove it if you only want to work with non-fork repositories.  
- **Repository Storage Path**: Change the `path` argument in `main(config.github_api_key, 'github')` to store repositories in a different folder.  
- **Log Details**: Add or modify `print` statements for more verbose output.

## Troubleshooting

- **Invalid Git Repositories**: If the script encounters a directory that is not a valid Git repository, it deletes and reclones it automatically.
- **Rate Limits**: If you run into GitHub API rate limits, ensure your token has the necessary permissions and that you aren’t making excessive requests.  
- **Permissions**: Verify your personal access token’s scopes (especially if you want to clone private repositories).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and adapt it for your own workflow. Contributions are welcome!
