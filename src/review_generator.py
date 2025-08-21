from github_service import GithubService
from diff_analyzer import DiffAnalyzer
from ai_service import AIService

class ReviewGenerator:
    """
    Orchestrates the pull request review process.
    """
    def __init__(self, github_service: GithubService):
        """
        Initializes the ReviewGenerator.

        Args:
            github_service (GithubService): An instance of the GithubService.
        """
        self.github_service = github_service
        self.diff_analyzer = DiffAnalyzer()
        self.ai_service = AIService(config_path='config.yaml')

    def run(self, pr_url):
        """
        Runs the review process for a given pull request URL.

        Args:
            pr_url (str): The URL of the pull request.
        """
        pr_data = self.github_service.get_pr_data(pr_url)
        diff = self.github_service.get_pr_diff(pr_url)
        
        analyzed_diff = self.diff_analyzer.analyze(diff, pr_data)
        review_comment = self.ai_service.generate_review(analyzed_diff)
        
        self.github_service.post_comment(pr_url, review_comment)
        print("Review comment posted successfully.")