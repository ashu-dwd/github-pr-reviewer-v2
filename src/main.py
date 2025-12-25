import os
import argparse
from github_service import GithubService
from review_generator import ReviewGenerator

# resolving config path relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, '..', 'config.yaml')

def main():
    """
    Main function to run the PR review tool.
    """
    parser = argparse.ArgumentParser(description="AI-Powered Pull Request Review Tool")
    parser.add_argument("pr_url", help="The URL of the pull request to review.")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"), help="GitHub API token.")
    args = parser.parse_args()

    if not args.token:
        raise ValueError("GitHub token not provided. Set the GITHUB_TOKEN environment variable or use the --token flag.")

    github_service = GithubService(args.token, config_path=CONFIG_PATH)
    review_generator = ReviewGenerator(github_service, config_path=CONFIG_PATH)

    review_generator.run(args.pr_url)

if __name__ == "__main__":
    main()