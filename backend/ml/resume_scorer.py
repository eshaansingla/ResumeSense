"""
Resume Quality Scorer using ML Model
Loads trained model and predicts resume quality score.
"""
import pickle
import os
from typing import Dict
import numpy as np
from backend.ml.feature_extractor import FeatureExtractor
from backend.config import Config


class ResumeScorer:
    """Score resume quality using trained ML model"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize the scorer with a trained model.
        
        Args:
            model_path: Path to the saved model file
        """
        self.model_path = model_path or Config.ML_MODEL_PATH
        self.model = None
        self.feature_names = FeatureExtractor.get_feature_names()
        self._load_model()
    
    def _load_model(self):
        """Load the trained model from file"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
            else:
                # If model doesn't exist, use a simple rule-based scorer
                self.model = None
                print(f"Model file not found at {self.model_path}. Using rule-based scoring.")
        except Exception as e:
            print(f"Error loading model: {e}. Using rule-based scoring.")
            self.model = None
    
    def score_resume(self, resume_text: str, jd_text: str = "") -> Dict:
        """
        Score resume quality (0-100).
        
        Args:
            resume_text: Resume text
            jd_text: Optional job description text
            
        Returns:
            Dictionary with score and details
        """
        # Extract features
        features = FeatureExtractor.extract_features(resume_text, jd_text)
        
        # Get feature values in correct order
        feature_values = [features[name] for name in self.feature_names]
        feature_array = np.array([feature_values])
        
        # Predict using model or fallback to rule-based
        if self.model is not None:
            try:
                # Get probability or score from model
                if hasattr(self.model, 'predict_proba'):
                    # For classification models
                    proba = self.model.predict_proba(feature_array)[0]
                    score = proba[1] * 100 if len(proba) > 1 else proba[0] * 100
                elif hasattr(self.model, 'predict'):
                    # For regression models
                    score = self.model.predict(feature_array)[0]
                    score = max(0, min(100, score))  # Clamp to 0-100
                else:
                    score = self._rule_based_score(features)
            except Exception as e:
                print(f"Error predicting with model: {e}. Using rule-based scoring.")
                score = self._rule_based_score(features)
        else:
            score = self._rule_based_score(features)
        
        return {
            'quality_score': round(score, 2),
            'features': features,
            'model_used': 'ml_model' if self.model is not None else 'rule_based'
        }
    
    def _rule_based_score(self, features: Dict) -> float:
        """
        Fallback rule-based scoring if model is not available.
        
        Args:
            features: Extracted features
            
        Returns:
            Score between 0-100
        """
        score = 0.0
        
        # ATS score (30 points)
        score += features['ats_score'] * 30
        
        # Section completeness (20 points)
        section_score = (features['has_education'] + features['has_experience'] + 
                        features['has_skills'] + features['has_contact']) / 4.0 * 20
        score += section_score
        
        # Power verbs (15 points)
        score += features['power_verb_ratio'] * 15
        
        # Numbers/metrics (15 points)
        if features['has_numbers']:
            score += min(15, features['numbers_count'] * 0.5)
        
        # Keyword density (10 points)
        score += features['keyword_density'] * 10
        
        # JD match (10 points) - if JD provided
        if features['jd_match_score'] > 0:
            score += features['jd_match_score'] * 10
        
        return min(100.0, max(0.0, score))


