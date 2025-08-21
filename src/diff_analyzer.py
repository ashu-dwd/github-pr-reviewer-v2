import re

class DiffAnalyzer:
    """
    Analyzes the diff of a pull request.
    """
    def analyze(self, diff, pr_data):
        """
        Analyzes the given diff.

        Args:
            diff (str): The diff string.
            pr_data (dict): The pull request data.

        Returns:
            dict: A dictionary containing the analyzed diff information.
        """
        print(f"Analyzing diff for PR: {pr_data['title']}")

        files = []
        # Split the diff into individual file diffs
        file_diffs = diff.split('diff --git')
        
        for file_diff in file_diffs:
            if not file_diff.strip():
                continue

            lines = file_diff.split('\n')
            file_name_match = re.search(r'a/(.+) b/(.+)', lines[0])
            if not file_name_match:
                continue

            file_name = file_name_match.group(2)
            
            chunks = self._chunk_diff(lines)

            files.append({
                "file_name": file_name,
                "chunks": chunks
            })

        return {
            "pr_title": pr_data["title"],
            "pr_body": pr_data["body"],
            "files": files
        }

    def _chunk_diff(self, lines, max_chunk_size=4000):
        """
        Splits the diff lines into chunks.

        Args:
            lines (list): The lines of the diff.
            max_chunk_size (int): The maximum size of a chunk in characters.

        Returns:
            list: A list of diff chunks.
        """
        chunks = []
        current_chunk = ""
        
        for line in lines:
            redacted_line = self._redact_secrets(line)
            if len(current_chunk) + len(redacted_line) > max_chunk_size:
                chunks.append(current_chunk)
                current_chunk = ""
            current_chunk += redacted_line + "\n"
        
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks

    def _redact_secrets(self, line):
        """
        Redacts potential secrets from a line.

        Args:
            line (str): The line to redact.

        Returns:
            str: The redacted line.
        """
        # This regex looks for common key/secret patterns.
        secret_pattern = re.compile(r'([\'"]?(?:[a-z0-9_]+_)?(?:key|token|secret|password)[\'"]?\s*[:=]\s*[\'"]?)([a-z0-9\-_.~+]{10,})([\'"]?)', re.IGNORECASE)
        return secret_pattern.sub(r'\1[REDACTED_SECRET]\3', line)