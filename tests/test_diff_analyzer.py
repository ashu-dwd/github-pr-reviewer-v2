import unittest
from src.diff_analyzer import DiffAnalyzer

class TestDiffAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = DiffAnalyzer()

    def test_analyze(self):
        diff = """
diff --git a/file1.py b/file1.py
--- a/file1.py
+++ b/file1.py
@@ -1,3 +1,4 @@
 def hello():
     print("Hello")
+    print("World")
 
 def goodbye():
     print("Goodbye")
"""
        pr_data = {
            "title": "Test PR",
            "body": "This is a test PR."
        }
        
        result = self.analyzer.analyze(diff, pr_data)
        
        self.assertEqual(result['pr_title'], 'Test PR')
        self.assertEqual(len(result['files']), 1)
        self.assertEqual(result['files'][0]['file_name'], 'file1.py')
        self.assertIn('def hello():', result['files'][0]['chunks'][0])

    def test_redact_secrets(self):
        line = 'API_KEY = "supersecretkey"'
        redacted_line = self.analyzer._redact_secrets(line)
        self.assertEqual(redacted_line, 'API_KEY = "[REDACTED_SECRET]"')

if __name__ == '__main__':
    unittest.main()