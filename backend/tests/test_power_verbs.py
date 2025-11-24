"""
Unit tests for Power Verb Suggester
"""
import unittest
from backend.nlp.power_verbs import PowerVerbSuggester


class TestPowerVerbSuggester(unittest.TestCase):
    """Test power verb suggestion functionality"""
    
    def test_find_weak_verbs(self):
        """Test finding weak verbs in text"""
        resume = "I did some work. I made a website. I helped the team."
        
        findings = PowerVerbSuggester.find_weak_verbs(resume)
        
        self.assertIsInstance(findings, list)
        # Should find weak verbs like 'did', 'made', 'helped'
        weak_verbs_found = [f['weak_verb'] for f in findings]
        self.assertTrue(any(verb in ['did', 'made', 'helped'] for verb in weak_verbs_found))
    
    def test_get_power_verb_stats(self):
        """Test power verb statistics"""
        resume = "I executed the project. I developed the application. I did some work."
        
        stats = PowerVerbSuggester.get_power_verb_stats(resume)
        
        self.assertIn('weak_verb_count', stats)
        self.assertIn('strong_verb_count', stats)
        self.assertIn('power_verb_score', stats)
        self.assertGreaterEqual(stats['power_verb_score'], 0)
        self.assertLessEqual(stats['power_verb_score'], 100)
    
    def test_find_weak_verbs_no_weak_verbs(self):
        """Test with resume containing only strong verbs"""
        resume = "I executed the project. I developed the application. I implemented the solution."
        
        findings = PowerVerbSuggester.find_weak_verbs(resume)
        
        # Should return empty or minimal findings
        self.assertIsInstance(findings, list)


if __name__ == '__main__':
    unittest.main()


