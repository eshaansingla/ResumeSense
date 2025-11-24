"""
Unit tests for PDF Parser
"""
import unittest
from backend.nlp.pdf_parser import PDFParser


class TestPDFParser(unittest.TestCase):
    """Test PDF parsing functionality"""
    
    def test_clean_text(self):
        """Test text cleaning functionality"""
        dirty_text = "This   is    a    test\n\n\nwith   multiple   spaces"
        cleaned = PDFParser._clean_text(dirty_text)
        
        # Should normalize whitespace
        self.assertNotIn("   ", cleaned)
        self.assertNotIn("\n\n", cleaned)
    
    def test_extract_text_from_bytes_empty(self):
        """Test extraction from empty bytes"""
        result = PDFParser.extract_text_from_bytes(b"")
        # Should handle gracefully
        self.assertIsNotNone(result)
    
    def test_clean_text_preserves_content(self):
        """Test that cleaning preserves important content"""
        text = "Python, JavaScript, and SQL are important skills."
        cleaned = PDFParser._clean_text(text)
        
        self.assertIn("Python", cleaned)
        self.assertIn("JavaScript", cleaned)
        self.assertIn("SQL", cleaned)


if __name__ == '__main__':
    unittest.main()


