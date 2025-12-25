import os
import yaml
from google import genai


# mapping file extensions to language names and review focus areas
LANGUAGE_MAP = {
    # Python
    ".py": {"name": "Python", "focus": ["PEP8 style", "type hints", "docstrings", "pythonic patterns", "exception handling"]},
    # JavaScript/TypeScript
    ".js": {"name": "JavaScript", "focus": ["ES6+ syntax", "async/await", "error handling", "XSS prevention", "null checks"]},
    ".jsx": {"name": "React JSX", "focus": ["component patterns", "hooks usage", "prop validation", "state management"]},
    ".ts": {"name": "TypeScript", "focus": ["type safety", "interface usage", "generics", "strict null checks"]},
    ".tsx": {"name": "React TSX", "focus": ["typed components", "hooks with types", "prop interfaces"]},
    ".vue": {"name": "Vue.js", "focus": ["component structure", "reactivity", "lifecycle hooks", "composition API"]},
    ".svelte": {"name": "Svelte", "focus": ["reactivity", "stores", "component composition"]},
    # Backend/Systems
    ".java": {"name": "Java", "focus": ["null safety", "exception handling", "design patterns", "memory management", "streams API"]},
    ".go": {"name": "Go", "focus": ["error handling", "goroutines", "defer usage", "idiomatic Go", "interface usage"]},
    ".rs": {"name": "Rust", "focus": ["ownership", "lifetimes", "Result/Option handling", "unsafe blocks", "error propagation"]},
    ".c": {"name": "C", "focus": ["memory management", "buffer overflows", "null pointers", "undefined behavior"]},
    ".cpp": {"name": "C++", "focus": ["RAII", "smart pointers", "memory safety", "modern C++ features"]},
    ".hpp": {"name": "C++ Header", "focus": ["header guards", "forward declarations", "template design"]},
    ".h": {"name": "C/C++ Header", "focus": ["header guards", "declarations", "macro safety"]},
    ".cs": {"name": "C#", "focus": ["null safety", "async patterns", "LINQ", "disposal patterns"]},
    # Mobile
    ".kt": {"name": "Kotlin", "focus": ["null safety", "coroutines", "extension functions", "data classes"]},
    ".swift": {"name": "Swift", "focus": ["optionals", "protocol-oriented design", "memory management", "async/await"]},
    # Scripting
    ".rb": {"name": "Ruby", "focus": ["Ruby idioms", "blocks", "error handling", "metaprogramming"]},
    ".php": {"name": "PHP", "focus": ["SQL injection", "XSS", "type declarations", "modern PHP patterns"]},
    ".scala": {"name": "Scala", "focus": ["functional patterns", "immutability", "Option handling", "pattern matching"]},
    ".sh": {"name": "Shell Script", "focus": ["quoting", "error handling", "shellcheck warnings", "portability"]},
    ".bash": {"name": "Bash Script", "focus": ["bash-specific features", "error handling", "quoting", "arrays"]},
    # Config/Data
    ".yaml": {"name": "YAML", "focus": ["syntax correctness", "security (no secrets)", "structure"]},
    ".yml": {"name": "YAML", "focus": ["syntax correctness", "security (no secrets)", "structure"]},
    ".json": {"name": "JSON", "focus": ["valid JSON", "schema compliance", "no sensitive data"]},
    ".toml": {"name": "TOML", "focus": ["syntax correctness", "standard structure"]},
    # SQL
    ".sql": {"name": "SQL", "focus": ["SQL injection", "performance", "indexing", "transactions", "parameterized queries"]},
    # Docker
    "Dockerfile": {"name": "Dockerfile", "focus": ["security", "layer optimization", "non-root user", "no sensitive data", "multi-stage builds"]},
    ".dockerfile": {"name": "Dockerfile", "focus": ["security", "layer optimization", "non-root user", "no sensitive data"]},
}


class AIService:
    """
    A service to interact with a Large Language Model (LLM) using the new Google GenAI SDK.
    Supports multi-language code reviews with language-specific focus areas.
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
        
        # using the new centralized Client object from google-genai SDK
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = self.config['model']

    def _get_language_info(self, file_name):
        """
        Detects the programming language from file extension and returns language-specific info.

        Args:
            file_name (str): The name of the file.

        Returns:
            dict: Language name and focus areas, or defaults if unknown.
        """
        # checking for special files like Dockerfile
        if file_name.endswith("Dockerfile") or "Dockerfile" in file_name:
            return LANGUAGE_MAP.get("Dockerfile", {"name": "Dockerfile", "focus": []})
        
        # extracting extension
        ext = os.path.splitext(file_name)[1].lower()
        
        return LANGUAGE_MAP.get(ext, {"name": "Unknown", "focus": ["general code quality", "security", "best practices"]})

    def generate_review(self, analyzed_diff):
        """
        Generates a review for the given analyzed diff.

        Args:
            analyzed_diff (dict): The analyzed diff information.

        Returns:
            str: The generated review.
        """
        print("Generating AI review...")

        file_reviews = []
        languages_detected = set()
        
        for file in analyzed_diff["files"]:
            lang_info = self._get_language_info(file['file_name'])
            languages_detected.add(lang_info['name'])
            
            for chunk in file["chunks"]:
                prompt = self._build_file_prompt(analyzed_diff, file['file_name'], chunk, lang_info)
                # using the new client.models.generate_content() API
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                file_reviews.append(response.text)
        
        # generating the final formatted review with header and footer
        return self._format_final_review(analyzed_diff, file_reviews, languages_detected)

    def _format_final_review(self, analyzed_diff, file_reviews, languages_detected):
        """
        Formats the final review with a nice header, file reviews, and footer.

        Args:
            analyzed_diff (dict): The analyzed diff information.
            file_reviews (list): List of individual file reviews.
            languages_detected (set): Set of detected programming languages.

        Returns:
            str: The formatted final review.
        """
        num_files = len(analyzed_diff["files"])
        languages_str = ", ".join(sorted(languages_detected)) if languages_detected else "Unknown"
        
        # building the header with summary stats
        header = f"""## 🤖 AI Code Review

> **PR:** {analyzed_diff['pr_title']}
> **Files Reviewed:** {num_files}
> **Languages:** {languages_str}

---

"""
        
        # joining all file reviews
        body = "\n\n---\n\n".join(file_reviews)
        
        # building the footer
        footer = """

---

<details>
<summary>📚 <b>Review Legend</b></summary>

| Severity | Meaning |
|----------|---------|
| 🔴 **Critical** | Must fix before merging - bugs, security issues |
| 🟠 **Warning** | Should fix - potential problems |
| 🟡 **Suggestion** | Nice to have - improvements |
| 🟢 **Praise** | Good practices worth noting |

</details>

---

*This review was generated by an AI assistant. Please verify suggestions before applying.*
"""
        
        return header + body + footer

    def _build_file_prompt(self, analyzed_diff, file_name, chunk, lang_info):
        """
        Builds the prompt for reviewing a specific file chunk with language-specific context.

        Args:
            analyzed_diff (dict): The analyzed diff information.
            file_name (str): The name of the file being reviewed.
            chunk (str): The diff chunk to review.
            lang_info (dict): Language name and focus areas.

        Returns:
            str: The prompt for the LLM.
        """
        language_name = lang_info['name']
        focus_areas = lang_info['focus']
        focus_str = ", ".join(focus_areas) if focus_areas else "general code quality"
        
        prompt = f"""You are an expert {language_name} code reviewer. Review this code change with a focus on quality, security, and best practices.

## Context
- **PR Title:** {analyzed_diff['pr_title']}
- **PR Description:** {analyzed_diff['pr_body'] or 'No description provided'}
- **Language:** {language_name}
- **Focus Areas:** {focus_str}

## File: `{file_name}`

```diff
{chunk}
```

## Language-Specific Review Guidelines for {language_name}

Pay special attention to these {language_name}-specific concerns:
{chr(10).join(f"- {area}" for area in focus_areas)}

## Your Review Format

Please structure your review EXACTLY as follows:

### 📄 `{file_name}` ({language_name})

**Summary:** [One sentence describing what this change does]

**Findings:**

[For each issue found, use this format:]

- 🔴 **Critical:** [Issue description]
  - **Line:** [approximate line number or range]
  - **Problem:** [What's wrong]
  - **Suggestion:** [How to fix it]
  ```{self._get_code_block_lang(file_name)}
  [Code suggestion if applicable]
  ```

- 🟠 **Warning:** [Issue description]
  - **Line:** [approximate line number or range]  
  - **Suggestion:** [How to improve]

- 🟡 **Suggestion:** [Improvement idea]
  - **Why:** [Brief explanation]

- 🟢 **Praise:** [What was done well]

**Checklist:**
- [ ] [Actionable item 1]
- [ ] [Actionable item 2]

---

**Rules:**
1. Be concise but specific
2. Always explain WHY something is an issue
3. Provide {language_name} code suggestions when possible
4. If the code looks good, say so briefly with a 🟢 Praise
5. Focus on: bugs, security, performance, readability, {language_name} best practices
6. Don't nitpick formatting if it's acceptable
7. Skip sections that don't apply (e.g., no Praise if nothing noteworthy)
"""
        return prompt

    def _get_code_block_lang(self, file_name):
        """
        Returns the appropriate markdown code block language for syntax highlighting.

        Args:
            file_name (str): The name of the file.

        Returns:
            str: The language identifier for markdown code blocks.
        """
        ext_to_lang = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "jsx",
            ".ts": "typescript",
            ".tsx": "tsx",
            ".java": "java",
            ".go": "go",
            ".rs": "rust",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".hpp": "cpp",
            ".cs": "csharp",
            ".kt": "kotlin",
            ".swift": "swift",
            ".rb": "ruby",
            ".php": "php",
            ".scala": "scala",
            ".sh": "bash",
            ".bash": "bash",
            ".sql": "sql",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".json": "json",
            ".toml": "toml",
            ".vue": "vue",
            ".svelte": "svelte",
        }
        
        if "Dockerfile" in file_name:
            return "dockerfile"
        
        ext = os.path.splitext(file_name)[1].lower()
        return ext_to_lang.get(ext, "")