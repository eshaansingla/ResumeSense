"""
Train ML Model for Resume Quality Scoring
Creates and trains a model using synthetic/example data.
"""
import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from backend.ml.feature_extractor import FeatureExtractor
from backend.config import Config


def generate_training_data():
    """
    Generate synthetic training data for the model.
    In production, this would use real resume data.
    
    Returns:
        Tuple of (features, labels)
    """
    # Sample resume texts with varying quality
    sample_resumes = [
        # High quality resume
        """John Doe
Email: john.doe@email.com | Phone: (555) 123-4567
123 Main Street, City, State 12345

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years developing scalable web applications.
Led cross-functional teams to deliver projects that increased revenue by 30%.
Expert in Python, JavaScript, and cloud technologies.

EXPERIENCE
Senior Software Engineer | Tech Corp | 2020 - Present
• Architected and developed microservices that improved system performance by 40%
• Led team of 5 engineers, reducing deployment time by 50%
• Implemented CI/CD pipelines using Docker and Kubernetes
• Increased code coverage from 60% to 90% through comprehensive testing

Software Engineer | Startup Inc | 2018 - 2020
• Developed RESTful APIs serving 1M+ requests daily
• Optimized database queries, reducing response time by 35%
• Collaborated with product team to deliver features on time

EDUCATION
Bachelor of Science in Computer Science | State University | 2018

SKILLS
Programming: Python, JavaScript, Java, SQL
Technologies: AWS, Docker, Kubernetes, React, Node.js
Tools: Git, Jenkins, JIRA""",
        
        # Medium quality resume
        """Jane Smith
jane.smith@email.com
(555) 987-6543

Summary
Software developer with experience in web development.

Experience
Developer | Company A | 2019 - 2021
• Worked on web applications
• Used Python and JavaScript
• Fixed bugs and added features

Education
BS Computer Science | University | 2019

Skills
Python, JavaScript, HTML, CSS""",
        
        # Low quality resume
        """Bob Johnson
bob@email.com

I did some work at different places. I made websites and fixed things.
I know how to use computers and write code sometimes.

Work History
• Job 1 - did stuff
• Job 2 - worked there
• Job 3 - another job

Education
Went to school""",
    ]
    
    # Generate variations
    all_resumes = []
    all_scores = []
    
    # High quality resumes (score 80-100)
    for i in range(10):
        resume = sample_resumes[0]
        # Add some variation
        if i % 2 == 0:
            resume = resume.replace("5+ years", f"{5+i} years")
        all_resumes.append(resume)
        all_scores.append(85 + np.random.uniform(-5, 15))
    
    # Medium quality resumes (score 50-80)
    for i in range(10):
        resume = sample_resumes[1]
        all_resumes.append(resume)
        all_scores.append(60 + np.random.uniform(-10, 20))
    
    # Low quality resumes (score 20-50)
    for i in range(10):
        resume = sample_resumes[2]
        all_resumes.append(resume)
        all_scores.append(35 + np.random.uniform(-15, 15))
    
    # Extract features
    X = []
    y = []
    
    for resume, score in zip(all_resumes, all_scores):
        try:
            features = FeatureExtractor.extract_features(resume)
            feature_values = [features[name] for name in FeatureExtractor.get_feature_names()]
            X.append(feature_values)
            y.append(score)
        except Exception as e:
            print(f"Error extracting features: {e}")
            continue
    
    return np.array(X), np.array(y)


def train_model():
    """
    Train the resume quality scoring model.
    """
    print("Generating training data...")
    X, y = generate_training_data()
    
    print(f"Training data shape: {X.shape}, Labels shape: {y.shape}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    print("Training Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"Training R² score: {train_score:.4f}")
    print(f"Test R² score: {test_score:.4f}")
    
    # Save model
    model_path = Config.ML_MODEL_PATH
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Model saved to {model_path}")
    
    return model


if __name__ == '__main__':
    train_model()

