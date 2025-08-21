import unittest
from unittest.mock import patch, MagicMock
from src.github_service import GithubService

class TestGithubService(unittest.TestCase):
    def setUp(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data='github_service:\n  include_files:\n    - \"**/*.py\"\n  exclude_files:\n    - \"**/tests/**\"')):
            self.service = GithubService(token="test_token")

    @patch('requests.get')
    def test_get_pr_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"title": "Test PR", "body": "Test Body"}
        mock_get.return_value = mock_response

        pr_url = "https://github.com/owner/repo/pull/123"
        data = self.service.get_pr_data(pr_url)

        self.assertEqual(data["title"], "Test PR")
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/pulls/123",
            headers={
                "Authorization": "token test_token",
                "Accept": "application/vnd.github.v3+json"
            }
        )

    @patch('requests.get')
    def test_get_pr_diff(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = "diff --git a/file.py b/file.py"
        mock_get.return_value = mock_response

        pr_url = "https://github.com/owner/repo/pull/123"
        diff = self.service.get_pr_diff(pr_url)

        self.assertEqual(diff, "diff --git a/file.py b/file.py")
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/pulls/123",
            headers={
                "Authorization": "token test_token",
                "Accept": "application/vnd.github.v3.diff"
            }
        )

    @patch('requests.post')
    def test_post_comment(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        pr_url = "https://github.com/owner/repo/pull/123"
        self.service.post_comment(pr_url, "Test Comment")

        mock_post.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/issues/123/comments",
            headers={
                "Authorization": "token test_token",
                "Accept": "application/vnd.github.v3+json"
            },
            json={"body": "Test Comment"}
        )

if __name__ == '__main__':
    unittest.main()