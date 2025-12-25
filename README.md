# AI-Powered Pull Request Review Tool

This tool is an AI-powered assistant for reviewing pull requests on GitHub. It analyzes PRs, checks for code quality issues, and provides actionable feedback to the developers.

## Architecture

The application will follow a modular architecture, separating concerns into distinct components. This design ensures maintainability, testability, and extensibility.

### Core Modules

1.  **GitHub Service (`src/github_service.py`)**: This module will be responsible for all interactions with the GitHub API. It will handle fetching PR details, diffs, and posting comments. It will use either the GitHub REST or GraphQL API.

2.  **Diff Analyzer (`src/diff_analyzer.py`)**: This module will contain the logic for parsing and analyzing the diffs from a pull request. It will identify added, modified, and deleted lines, and prepare the data for the AI service.

3.  **AI Service (`src/ai_service.py`)**: This module will be responsible for interacting with a Large Language Model (LLM). It will take the processed diff from the `Diff Analyzer` and generate human-like review comments. It will also handle prompt engineering to get the best results from the LLM.

4.  **Review Generator (`src/review_generator.py`)**: This module will orchestrate the review process. It will use the `GitHub Service` to get PR data, the `Diff Analyzer` to process the diff, and the `AI Service` to generate comments. Finally, it will format the review and use the `GitHub Service` to post it.

5.  **Main/CLI (`src/main.py`)**: This will be the main entry point for the application. It will handle command-line arguments (e.g., PR URL, GitHub token) and trigger the review process. It will also serve as the entry point for the GitHub Action.

6.  **Configuration (`config.yaml`)**: A configuration file will be used to store settings like the LLM to use, token limits, and file inclusion/exclusion patterns.

### Data Flow

1.  The `main.py` script is invoked with a PR URL.
2.  The `Review Generator` fetches the PR data and diff from the `GitHub Service`.
3.  The diff is passed to the `Diff Analyzer` for processing.
4.  The processed diff is sent to the `AI Service` to generate review comments.
5.  The `Review Generator` formats the comments into a Markdown report.
6.  The report is posted as a comment on the PR using the `GitHub Service`.

This architecture provides a solid foundation for building a robust and scalable PR review tool.

## Usage

### Prerequisites

- Python 3.8+
- A GitHub API token with `repo` scope.
- An API key for the selected LLM (e.g., Gemini).

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/ai-pr-reviewer.git
    cd ai-pr-reviewer
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Tool

1.  Set the required environment variables:
    ```bash
    export GITHUB_TOKEN="your_github_token"
    export GEMINI_API_KEY="your_gemini_api_key"
    ```
2.  Run the tool from the command line:
    ```bash
    python src/main.py <pull_request_url>
    ```

### GitHub Action

This tool can also be run as a GitHub Action. To do so, add the `.github/workflows/main.yml` file to your repository. You will also need to add `GEMINI_API_KEY` as a secret to your repository.
