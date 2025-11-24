"""
Unit tests for JD Matcher
"""
import unittest
from backend.nlp.jd_matcher import JDMatcher


class TestJDMatcher(unittest.TestCase):
    """Test JD matching functionality"""
    
    def test_compute_match_score(self):
        """Test match score computation"""
        resume = "Python JavaScript SQL Flask React"
        jd = "Python JavaScript SQL Flask React Docker"
        
        result = JDMatcher.compute_match_score(resume, jd)
        
        self.assertIn('match_score', result)
        self.assertGreaterEqual(result['match_score'], 0)
        self.assertLessEqual(result['match_score'], 100)
    
    def test_compute_match_score_no_jd(self):
        """Test match score with empty JD"""
        resume = "Python JavaScript SQL"
        jd = ""
        
        result = JDMatcher.compute_match_score(resume, jd)
        
        self.assertEqual(result['match_score'], 0.0)
    
    def test_tokenize(self):
        """Test tokenization"""
        text = "Python, JavaScript, and SQL!"
        tokens = JDMatcher._tokenize(text)
        
        self.assertIn('python', tokens)
        self.assertIn('javascript', tokens)
        self.assertIn('sql', tokens)
    
    def test_extract_keywords(self):
        """Test keyword extraction"""
        tokens = ['python', 'javascript', 'the', 'a', 'and', 'sql']
        keywords = JDMatcher._extract_keywords(tokens)
        
        self.assertIn('python', keywords)
        self.assertIn('javascript', keywords)
        self.assertIn('sql', keywords)
        self.assertNotIn('the', keywords)
        self.assertNotIn('a', keywords)


if __name__ == '__main__':
    unittest.main()


