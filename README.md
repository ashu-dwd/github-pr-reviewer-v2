# 🤖 AI-Powered Pull Request Review Tool

An AI-powered assistant for reviewing pull requests on GitHub. It analyzes PRs, checks for code quality issues, security vulnerabilities, and provides actionable feedback.

## ✨ Features

- 🔄 **Automatic Reviews** - Reviews PRs automatically when opened or updated
- 💬 **Re-review Command** - Comment `/review` on any PR to trigger a fresh review
- � **Multi-Language Support** - Smart reviews for 20+ programming languages
- �🎯 **Structured Feedback** - Clear severity levels (🔴 Critical, 🟠 Warning, 🟡 Suggestion, 🟢 Praise)
- 🔒 **Security Scanning** - Detects potential security issues
- 📝 **Actionable Checklists** - Provides concrete improvement items
- 🛡️ **Secret Redaction** - Automatically redacts potential secrets from diffs

### Supported Languages

| Category        | Languages                                               |
| --------------- | ------------------------------------------------------- |
| **Web**         | JavaScript, TypeScript, React (JSX/TSX), Vue.js, Svelte |
| **Backend**     | Python, Java, Go, Rust, C#, PHP, Ruby, Scala            |
| **Systems**     | C, C++                                                  |
| **Mobile**      | Kotlin, Swift                                           |
| **Scripts**     | Shell, Bash                                             |
| **Data/Config** | SQL, YAML, JSON, TOML                                   |
| **DevOps**      | Dockerfile                                              |

## 🚀 Quick Start

Choose one of the two options below:

---

### Option 1: Copy Files (Simple Setup)

Best for single repositories or when you want full control.

**Step 1:** Copy these files to your repository:

- `.github/workflows/main.yml`
- `src/` folder
- `config.yaml`
- `requirements.txt`

**Step 2:** Add the `GEMINI_API_KEY` secret (see below).

---

### Option 2: Reusable Workflow (Recommended for Multiple Repos)

Best when you want to use this tool across many repositories without duplicating code.

**Step 1:** Create `.github/workflows/pr-review.yml` in your target repository:

```yaml
name: AI PR Review

on:
  pull_request:
    types: [opened, synchronize]
  issue_comment:
    types: [created]

permissions:
  pull-requests: write
  contents: read

jobs:
  review:
    runs-on: ubuntu-latest
    if: |
      github.event_name == 'pull_request' ||
      (github.event_name == 'issue_comment' &&
       github.event.issue.pull_request &&
       contains(github.event.comment.body, '/review'))

    steps:
      - name: Checkout reviewer tool
        uses: actions/checkout@v4
        with:
          repository: ashu-dwd/github-pr-reviewer-v2
          path: reviewer

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r reviewer/requirements.txt

      - name: Add reaction to comment
        if: github.event_name == 'issue_comment'
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.reactions.createForIssueComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              comment_id: context.payload.comment.id,
              content: 'eyes'
            });

      - name: Get PR URL
        id: get_pr_url
        uses: actions/github-script@v7
        with:
          script: |
            let prUrl;
            if (context.eventName === 'pull_request') {
              prUrl = context.payload.pull_request.html_url;
            } else {
              const pr = await github.rest.pulls.get({
                owner: context.repo.owner,
                repo: context.repo.repo,
                pull_number: context.payload.issue.number
              });
              prUrl = pr.data.html_url;
            }
            core.setOutput('pr_url', prUrl);

      - name: Run AI Review
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python reviewer/src/main.py "${{ steps.get_pr_url.outputs.pr_url }}"

      - name: Add success reaction
        if: github.event_name == 'issue_comment' && success()
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.reactions.createForIssueComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              comment_id: context.payload.comment.id,
              content: 'rocket'
            });
```

**Step 2:** Add the `GEMINI_API_KEY` secret (see below).

---

### Add Secrets (Required for Both Options)

Go to your repository **Settings → Secrets and variables → Actions** and add:

| Secret           | Description                                                                            |
| ---------------- | -------------------------------------------------------------------------------------- |
| `GEMINI_API_KEY` | Your Google AI Studio API key ([Get one here](https://aistudio.google.com/app/apikey)) |

> **Note:** `GITHUB_TOKEN` is automatically provided by GitHub Actions.

### That's It! 🎉

The bot will now automatically review all new PRs.

## 💡 Usage

### Automatic Review

The bot automatically reviews PRs when:

- A new PR is **opened**
- New commits are **pushed** to an existing PR

### Manual Re-review

Comment on any PR to trigger a fresh review:

```
/review
```

The bot will react with 👀 when it starts and 🚀 when complete.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      main.py (CLI)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   review_generator.py                        │
│              (Orchestrates the review process)               │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ github_service  │  │  diff_analyzer  │  │   ai_service    │
│ (GitHub API)    │  │ (Parse diffs)   │  │ (Gemini AI)     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Core Modules

| Module                | Description                                                |
| --------------------- | ---------------------------------------------------------- |
| `github_service.py`   | Handles GitHub API interactions (fetch PRs, post comments) |
| `diff_analyzer.py`    | Parses diffs, chunks large files, redacts secrets          |
| `ai_service.py`       | Generates AI reviews using Google Gemini                   |
| `review_generator.py` | Orchestrates the entire review workflow                    |
| `main.py`             | CLI entry point                                            |
| `config.yaml`         | Configuration settings                                     |

## ⚙️ Configuration

Edit `config.yaml` to customize behavior:

```yaml
ai_service:
  model: "gemini-2.5-flash" # AI model to use
  max_tokens: 2048 # Max response length

github_service:
  include_files: # Files to review (glob patterns)
    - "**/*.py"
    - "**/*.js"
    - "**/*.ts"
  exclude_files: # Files to skip
    - "**/tests/**"
    - "**/node_modules/**"
    - "**/dist/**"
```

## 🖥️ Local Development

### Prerequisites

- Python 3.8+
- GitHub Personal Access Token with `repo` scope
- Gemini API Key

### Installation

```bash
# clone the repo
git clone https://github.com/ashu-dwd/github-pr-reviewer-v2.git
cd github-pr-reviewer-v2

# create virtual environment
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
# set environment variables
export GITHUB_TOKEN="your_github_token"
export GEMINI_API_KEY="your_gemini_api_key"

# review a specific PR
python src/main.py "https://github.com/owner/repo/pull/123"
```

## 📋 Review Output Example

```markdown
## 🤖 AI Code Review

> **PR:** Add user authentication
> **Files Reviewed:** 3

---

### 📄 `auth.py`

**Summary:** Adds login function with password validation.

**Findings:**

- 🔴 **Critical:** SQL Injection vulnerability

  - **Line:** 45
  - **Problem:** User input directly in SQL query
  - **Suggestion:** Use parameterized queries

- 🟢 **Praise:** Good use of context managers

**Checklist:**

- [ ] Fix SQL injection
- [ ] Add input validation
```

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a PR.

## 📄 License

MIT License - feel free to use this in your own projects!
