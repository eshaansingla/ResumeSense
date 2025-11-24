"""
Unit tests for ATS Checker
"""
import unittest
from backend.nlp.ats_checker import ATSChecker


class TestATSChecker(unittest.TestCase):
    """Test ATS compliance checking"""
    
    def test_check_compliance_complete_resume(self):
        """Test ATS check on complete resume"""
        resume = """
        John Doe
        Email: john@email.com
        Phone: 555-123-4567
        
        EDUCATION
        Bachelor of Science in Computer Science
        
        EXPERIENCE
        Software Engineer at Tech Corp
        
        SKILLS
        Python, JavaScript, SQL
        """
        
        result = ATSChecker.check_compliance(resume)
        
        self.assertIn('ats_score', result)
        self.assertGreaterEqual(result['ats_score'], 0)
        self.assertLessEqual(result['ats_score'], 100)
        self.assertIn('section_checks', result)
    
    def test_check_contact_info(self):
        """Test contact information detection"""
        resume = "Email: test@email.com Phone: 555-123-4567"
        result = ATSChecker.check_compliance(resume)
        
        self.assertTrue(result['contact_check']['has_email'])
        self.assertTrue(result['contact_check']['has_phone'])
    
    def test_check_sections(self):
        """Test section detection"""
        resume = "EDUCATION: Bachelor's degree. EXPERIENCE: 5 years. SKILLS: Python"
        result = ATSChecker.check_compliance(resume)
        
        self.assertTrue(result['section_checks']['education'])
        self.assertTrue(result['section_checks']['experience'])
        self.assertTrue(result['section_checks']['skills'])


if __name__ == '__main__':
    unittest.main()


