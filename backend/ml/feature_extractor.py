"""
Feature Extraction for Resume Quality Scoring
Extracts features from resume text for ML model.
"""
import re
from typing import Dict
from backend.nlp.ats_checker import ATSChecker
from backend.nlp.power_verbs import PowerVerbSuggester


class FeatureExtractor:
    """Extract features from resume for ML model"""
    
    @staticmethod
    def extract_features(resume_text: str, jd_text: str = "") -> Dict:
        """
        Extract all features from resume text for ML model.
        
        Args:
            resume_text: Resume text
            jd_text: Optional job description text
            
        Returns:
            Dictionary of extracted features
        """
        features = {}
        
        # Basic text features
        features['text_length'] = len(resume_text)
        features['word_count'] = len(resume_text.split())
        features['sentence_count'] = len(re.split(r'[.!?]+', resume_text))
        
        # Keyword density
        features['keyword_density'] = FeatureExtractor._calculate_keyword_density(resume_text)
        
        # Action verbs count
        verb_stats = PowerVerbSuggester.get_power_verb_stats(resume_text)
        features['action_verbs_count'] = verb_stats['strong_verb_count']
        features['weak_verbs_count'] = verb_stats['weak_verb_count']
        features['power_verb_ratio'] = verb_stats['power_verb_score'] / 100.0
        
        # Numbers/metrics presence
        features['has_numbers'] = 1 if re.search(r'\d+', resume_text) else 0
        features['numbers_count'] = len(re.findall(r'\d+', resume_text))
        features['percentage_mentions'] = len(re.findall(r'\d+%', resume_text))
        
        # ATS features
        ats_result = ATSChecker.check_compliance(resume_text)
        features['ats_score'] = ats_result['ats_score'] / 100.0
        features['has_education'] = 1 if ats_result['section_checks']['education'] else 0
        features['has_experience'] = 1 if ats_result['section_checks']['experience'] else 0
        features['has_skills'] = 1 if ats_result['section_checks']['skills'] else 0
        features['has_contact'] = 1 if ats_result['contact_check']['complete'] else 0
        features['has_bullets'] = 1 if ats_result['formatting_checks']['has_bullets'] else 0
        
        # Section count
        section_count = sum(ats_result['section_checks'].values())
        features['section_count'] = section_count
        
        # JD match features (if JD provided)
        if jd_text:
            from backend.nlp.jd_matcher import JDMatcher
            match_result = JDMatcher.compute_match_score(resume_text, jd_text)
            features['jd_match_score'] = match_result['match_score'] / 100.0
            features['common_keywords'] = len(match_result['common_keywords'])
        else:
            features['jd_match_score'] = 0.0
            features['common_keywords'] = 0
        
        # Professional indicators
        features['has_email'] = 1 if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text) else 0
        features['has_phone'] = 1 if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', resume_text) else 0
        
        # Quantifiable achievements
        achievement_keywords = ['increased', 'decreased', 'improved', 'reduced', 'achieved', 'accomplished']
        features['achievement_keywords'] = sum(1 for kw in achievement_keywords if kw.lower() in resume_text.lower())
        
        return features
    
    @staticmethod
    def _calculate_keyword_density(text: str) -> float:
        """
        Calculate keyword density (ratio of meaningful words to total words).
        
        Args:
            text: Resume text
            
        Returns:
            Keyword density ratio
        """
        words = text.lower().split()
        if len(words) == 0:
            return 0.0
        
        # Common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'may', 'might', 'must', 'can'
        }
        
        meaningful_words = [w for w in words if w not in stop_words and len(w) > 2]
        return len(meaningful_words) / len(words)
    
    @staticmethod
    def get_feature_names() -> list:
        """
        Get list of feature names in the same order as extract_features returns.
        This is used for model training and prediction.
        
        Returns:
            List of feature names
        """
        return [
            'text_length', 'word_count', 'sentence_count', 'keyword_density',
            'action_verbs_count', 'weak_verbs_count', 'power_verb_ratio',
            'has_numbers', 'numbers_count', 'percentage_mentions',
            'ats_score', 'has_education', 'has_experience', 'has_skills',
            'has_contact', 'has_bullets', 'section_count',
            'jd_match_score', 'common_keywords',
            'has_email', 'has_phone', 'achievement_keywords'
        ]


