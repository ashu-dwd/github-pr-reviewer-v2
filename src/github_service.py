import requests
import yaml

class GithubService:
    """
    A service to interact with the GitHub API.
    """
    def __init__(self, token, config_path='config.yaml'):
        """
        Initializes the GithubService.

        Args:
            token (str): The GitHub API token.
            config_path (str): The path to the configuration file.
        """
        self.token = token
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = "https://api.github.com"
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def get_pr_data(self, pr_url):
        """
        Fetches the data for a given pull request URL.

        Args:
            pr_url (str): The URL of the pull request.

        Returns:
            dict: The pull request data.
        """
        api_url = self._get_api_url(pr_url)
        
        response = requests.get(api_url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_pr_diff(self, pr_url):
        """
        Fetches the diff for a given pull request URL.

        Args:
            pr_url (str): The URL of the pull request.

        Returns:
            str: The diff of the pull request.
        """
        api_url = self._get_api_url(pr_url)
        
        diff_headers = self.headers.copy()
        diff_headers["Accept"] = "application/vnd.github.v3.diff"
        
        response = requests.get(api_url, headers=diff_headers)
        response.raise_for_status()
        return response.text

    def post_comment(self, pr_url, comment):
        """
        Posts a comment to a pull request.

        Args:
            pr_url (str): The URL of the pull request.
            comment (str): The comment to post.
        """
        api_url = self._get_api_url(pr_url).replace("/pulls/", "/issues/") + "/comments"

        data = {"body": comment}
        response = requests.post(api_url, headers=self.headers, json=data)
        response.raise_for_status()

    def _get_api_url(self, pr_url):
        """
        Constructs the API URL from a pull request URL.

        Args:
            pr_url (str): The URL of the pull request.

        Returns:
            str: The API URL for the pull request.
        """
        parts = pr_url.split("/")
        owner = parts[3]
        repo = parts[4]
        pr_number = parts[6]
        return f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"