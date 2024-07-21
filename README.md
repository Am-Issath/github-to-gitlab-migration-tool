# GitHub to GitLab Migration Tool

Automate the migration of multiple repositories from GitHub to GitLab with this powerful Python script. Designed for developers and organizations looking to effortlessly transfer their projects, including private repositories, without manual intervention.

## Key Features

- Bulk migration of repositories from GitHub to GitLab
- Supports both public and private repositories
- Automated cloning and pushing to GitLab
- Detailed logging for easy monitoring
- Configurable for different GitHub organizations and GitLab groups
- Secure credential management using environment variables

## Quick Start

1. Clone this repository:
```
git clone https://github.com/Am-Issath/github-to-gitlab-migration-tool.git
cd github-to-gitlab-migration-tool
```
2. Install required packages:
```
pip install gitlab PyGithub python-dotenv
```
3. Set up the environment file (see [Environment Setup](#environment-setup))

4. Create a `repositories.txt` file listing repos to migrate

5. Run the script:
```
python github_to_gitlab_migration.py
```

## Environment Setup

To securely manage your credentials, we use environment variables. Follow these steps to set up your environment:

1. Create a file named `.env` in the root directory of the project
2. Add the following content to the `.env` file, replacing the placeholder values with your actual credentials:
```
GITHUB_TOKEN=your_github_token
GITHUB_ORG=your_github_organization
GITLAB_URL=your_gitlab_url
GITLAB_TOKEN=your_gitlab_token
GITLAB_GROUP=your_gitlab_group
```
3. Make sure to add `.env` to your `.gitignore` file to prevent accidentally committing sensitive information:
```
echo ".env" >> .gitignore
```

## Detailed Setup and Usage

- Ensure you have Python 3.x installed on your system.
- Install the required Python packages as mentioned in the Quick Start section.
- Set up your environment file as described in the Environment Setup section.
- Create a `repositories.txt` file in the same directory as the script. List each repository you want to migrate on a separate line.
- Run the script using `python github_to_gitlab_migration.py`.
- The script will process each repository listed in `repositories.txt`, migrating it from GitHub to GitLab.
- Check the console output for progress and any error messages.

## Why Use This Tool?

- **Time-Saving**: Migrate multiple repositories in one go
- **Flexible**: Works with various GitHub organizations and GitLab groups
- **Secure**: Handles private repositories with proper authentication
- **Safe**: Uses environment variables for sensitive information

## Contributing

We welcome contributions! Please check our Contributing Guidelines for more details.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For issues, questions, or contributions, please open an issue in this repository.

**Happy migrating!**
