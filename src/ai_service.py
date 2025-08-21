import os
import google.generativeai as genai
import yaml

class AIService:
    """
    A service to interact with a Large Language Model (LLM).
    """
    def __init__(self, config_path='config.yaml'):
        """
        Initializes the AIService.

        Args:
            config_path (str): The path to the configuration file.
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['ai_service']
        
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set the GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.config['model'])

    def generate_review(self, analyzed_diff):
        """
        Generates a review for the given analyzed diff.

        Args:
            analyzed_diff (dict): The analyzed diff information.

        Returns:
            str: The generated review.
        """
        print("Generating AI review...")

        reviews = []
        for file in analyzed_diff["files"]:
            for chunk in file["chunks"]:
                prompt = self._build_prompt(analyzed_diff, file['file_name'], chunk)
                response = self.model.generate_content(prompt)
                reviews.append(response.text)
        
        return "\n\n".join(reviews)

    def _build_prompt(self, analyzed_diff, file_name, chunk):
        """
        Builds the prompt for the LLM.

        Args:
            analyzed_diff (dict): The analyzed diff information.
            file_name (str): The name of the file being reviewed.
            chunk (str): The diff chunk to review.

        Returns:
            str: The prompt for the LLM.
        """
        prompt = (
            "You are an expert software engineer acting as a code reviewer. "
            "Please provide a thorough review of the following pull request.\n\n"
            f"**PR Title:** {analyzed_diff['pr_title']}\n"
            f"**PR Body:**\n{analyzed_diff['pr_body']}\n\n"
            "**File Changed:**\n\n"
        )

        prompt += f"**File:** `{file_name}`\n"
        prompt += "```diff\n"
        prompt += chunk
        prompt += "```\n\n"
        
        prompt += (
            "**Review Checklist:**\n"
            "- **Summary:** Provide a brief summary of the PR.\n"
            "- **Code Quality:** Check for missing tests, security risks, performance issues, and readability.\n"
            "- **File-by-File Notes:** Provide actionable suggestions with severity levels ([Critical], [Medium], [Minor]).\n"
            "- **Action Items:** Produce a checklist of concrete improvements.\n\n"
            "Please provide your review for this chunk in Markdown format."
        )
        return prompt