import os
import subprocess
import gitlab
from github import Github
from dotenv import load_dotenv
import os

load_dotenv()

# GitHub credentials
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_ORG = os.getenv('GITHUB_ORG')

# GitLab credentials
GITLAB_URL = os.getenv('GITLAB_URL')
GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')
GITLAB_GROUP = os.getenv('GITLAB_GROUP')

# File containing repository names
REPO_LIST_FILE = 'repositories.txt'

# Initialize GitHub and GitLab clients
github_client = Github(GITHUB_TOKEN)
gitlab_client = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)

def migrate_repo(github_repo, gitlab_group):
    print(f"Migrating {github_repo.name}...")
    
    try:
        # Create a new project in GitLab
        gitlab_project = gitlab_client.projects.create({
            'name': github_repo.name,
            'namespace_id': gitlab_group.id
        })
        
        # Clone the GitHub repository
        clone_command = f"git clone --mirror {github_repo.clone_url} {github_repo.name}"
        print(f"Cloning with command: {clone_command}")
        clone_result = subprocess.run(clone_command, shell=True, capture_output=True, text=True)
        print(clone_result.stdout)
        if clone_result.returncode != 0:
            print(f"Error cloning: {clone_result.stderr}")
            return

        # Change to the cloned directory
        os.chdir(github_repo.name)
        
        # Push to GitLab
        push_command = f"git push --mirror {gitlab_project.http_url_to_repo}"
        print(f"Pushing to GitLab with command: {push_command}")
        push_result = subprocess.run(push_command, shell=True, capture_output=True, text=True)
        print(push_result.stdout)
        if push_result.returncode != 0:
            print(f"Error pushing to GitLab: {push_result.stderr}")
        else:
            print(f"Successfully pushed {github_repo.name} to GitLab")
        
        # Clean up
        os.chdir('..')
        os.system(f"rm -rf {github_repo.name}")
        
        print(f"Migration of {github_repo.name} completed.")
    except Exception as e:
        print(f"Error migrating {github_repo.name}: {str(e)}")
    finally:
        # Ensure we're back in the original directory
        if os.getcwd().endswith(github_repo.name):
            os.chdir('..')

def main():
    # Test GitLab authentication
    try:
        gitlab_client.auth()
        print("Successfully authenticated with GitLab")
    except gitlab.exceptions.GitlabAuthenticationError:
        print("Failed to authenticate with GitLab. Check your token and URL.")
        return

    # Get GitLab user information
    try:
        user = gitlab_client.user
        if user:
            print(f"Authenticated as GitLab user: {user.name}")
        else:
            print("Authenticated with GitLab, but unable to retrieve user information")
    except Exception as e:
        print(f"Warning: Authenticated with GitLab, but encountered an error retrieving user information: {e}")

    # Get GitHub organization
    try:
        github_org = github_client.get_organization(GITHUB_ORG)
        print(f"Successfully connected to GitHub organization: {GITHUB_ORG}")
    except Exception as e:
        print(f"Error connecting to GitHub organization: {e}")
        return

    # Get GitLab group
    try:
        gitlab_group = gitlab_client.groups.get(GITLAB_GROUP)
        print(f"Successfully got GitLab group: {gitlab_group.full_path}")
    except gitlab.exceptions.GitlabGetError as e:
        print(f"Error getting GitLab group: {e}")
        return

    # Read repository names from file
    try:
        with open(REPO_LIST_FILE, 'r') as file:
            repo_names = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {REPO_LIST_FILE} not found.")
        return
    except Exception as e:
        print(f"Error reading repository list file: {e}")
        return

    # Iterate through specified repositories in the GitHub organization
    for repo_name in repo_names:
        try:
            repo = github_org.get_repo(repo_name)
            if repo.private:
                migrate_repo(repo, gitlab_group)
            else:
                print(f"Skipping {repo_name} as it is not a private repository.")
        except Github.GithubException as e:
            print(f"Error accessing GitHub repository {repo_name}: {e}")
        except Exception as e:
            print(f"Unexpected error processing {repo_name}: {str(e)}")

    print("Migration process completed.")

if __name__ == "__main__":
    main()