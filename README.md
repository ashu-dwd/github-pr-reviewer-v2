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

### 1. Add the GitHub Workflow

Copy `.github/workflows/main.yml` to your repository.

### 2. Add Secrets

Go to your repository **Settings → Secrets → Actions** and add:

| Secret           | Description                                                                            |
| ---------------- | -------------------------------------------------------------------------------------- |
| `GEMINI_API_KEY` | Your Google AI Studio API key ([Get one here](https://aistudio.google.com/app/apikey)) |

> **Note:** `GITHUB_TOKEN` is automatically provided by GitHub Actions.

### 3. That's It! 🎉

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
