"""
Synthetic Poll Data Generator
Generates realistic poll/survey data for the Poll Results Visualizer project
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class PollDataGenerator:
    def __init__(self, seed=42):
        """Initialize generator with seed for reproducibility"""
        np.random.seed(seed)
        random.seed(seed)
        
    def generate_poll_data(self, n_responses=500):
        """
        Generate synthetic poll data with realistic patterns
        
        Parameters:
        n_responses: Number of survey responses to generate
        
        Returns:
        DataFrame with synthetic poll data
        """
        
        # Define possible values for each column
        regions = ['North', 'South', 'East', 'West', 'Central']
        age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
        genders = ['Male', 'Female', 'Non-binary', 'Prefer not to say']
        occupations = ['Student', 'Professional', 'Business Owner', 'Retired', 'Unemployed']
        education = ['High School', 'Bachelor\'s', 'Master\'s', 'PhD', 'Other']
        
        # Poll questions and options
        questions = {
            'preferred_tool': {
                'question': 'Which data analysis tool do you prefer?',
                'options': ['Python', 'R', 'Excel', 'Tableau', 'Power BI', 'SPSS']
            },
            'satisfaction_rating': {
                'question': 'How satisfied are you with your current tools?',
                'options': [1, 2, 3, 4, 5]  # 1=Very Unsatisfied, 5=Very Satisfied
            },
            'would_recommend': {
                'question': 'Would you recommend our product to others?',
                'options': ['Definitely Yes', 'Probably Yes', 'Not Sure', 'Probably No', 'Definitely No']
            },
            'support_quality': {
                'question': 'How would you rate our customer support?',
                'options': ['Excellent', 'Good', 'Average', 'Poor', 'Very Poor']
            },
            'feature_importance': {
                'question': 'Which feature is most important to you?',
                'options': ['Ease of Use', 'Performance', 'Price', 'Support', 'Integration', 'Security']
            },
            'usage_frequency': {
                'question': 'How often do you use our product?',
                'options': ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never']
            }
        }
        
        # Generate response data with realistic patterns
        data = []
        start_date = datetime(2024, 1, 1)
        
        # Create regional preferences (biases)
        regional_bias = {
            'North': {'Python': 0.4, 'R': 0.2, 'Excel': 0.15, 'Tableau': 0.15, 'Power BI': 0.05, 'SPSS': 0.05},
            'South': {'Python': 0.25, 'R': 0.15, 'Excel': 0.25, 'Tableau': 0.1, 'Power BI': 0.15, 'SPSS': 0.1},
            'East': {'Python': 0.3, 'R': 0.25, 'Excel': 0.2, 'Tableau': 0.1, 'Power BI': 0.1, 'SPSS': 0.05},
            'West': {'Python': 0.45, 'R': 0.1, 'Excel': 0.1, 'Tableau': 0.2, 'Power BI': 0.1, 'SPSS': 0.05},
            'Central': {'Python': 0.2, 'R': 0.1, 'Excel': 0.35, 'Tableau': 0.1, 'Power BI': 0.15, 'SPSS': 0.1}
        }
        
        # Age group satisfaction bias (younger users more satisfied with modern tools)
        age_satisfaction_bias = {
            '18-24': 4.2, '25-34': 4.0, '35-44': 3.7, '45-54': 3.4, '55+': 3.1
        }
        
        for i in range(n_responses):
            # Generate timestamp (spread across 3 months)
            timestamp = start_date + timedelta(
                days=random.randint(0, 90),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            # Demographics
            region = random.choice(regions)
            age_group = random.choice(age_groups)
            gender = random.choice(genders)
            occupation = random.choice(occupations)
            education_level = random.choice(education)
            
            # Generate response ID
            response_id = f"RES_{i+1:04d}"
            
            # Generate tool preference with regional bias
            tool_probs = regional_bias[region]
            preferred_tool = np.random.choice(
                questions['preferred_tool']['options'],
                p=[tool_probs[tool] for tool in questions['preferred_tool']['options']]
            )
            
            # Generate satisfaction rating (influenced by age and tool)
            base_satisfaction = age_satisfaction_bias[age_group]
            tool_bonus = 0.5 if preferred_tool in ['Python', 'Tableau'] else 0
            satisfaction = min(5, max(1, base_satisfaction + tool_bonus + np.random.normal(0, 0.5)))
            satisfaction = round(satisfaction)
            
            # Generate recommendation (correlated with satisfaction)
            if satisfaction >= 4:
                recommend = np.random.choice(
                    questions['would_recommend']['options'],
                    p=[0.6, 0.25, 0.1, 0.03, 0.02]
                )
            elif satisfaction == 3:
                recommend = np.random.choice(
                    questions['would_recommend']['options'],
                    p=[0.2, 0.3, 0.3, 0.1, 0.1]
                )
            else:
                recommend = np.random.choice(
                    questions['would_recommend']['options'],
                    p=[0.05, 0.1, 0.2, 0.35, 0.3]
                )
            
            # Generate support quality rating
            support_quality = np.random.choice(
                questions['support_quality']['options'],
                p=[0.3, 0.35, 0.2, 0.1, 0.05] if region in ['North', 'West'] 
                  else [0.2, 0.3, 0.3, 0.15, 0.05]
            )
            
            # Generate feature importance (varies by occupation)
            if occupation == 'Student':
                feature_importance = np.random.choice(
                    questions['feature_importance']['options'],
                    p=[0.35, 0.2, 0.2, 0.1, 0.1, 0.05]
                )
            elif occupation == 'Professional':
                feature_importance = np.random.choice(
                    questions['feature_importance']['options'],
                    p=[0.25, 0.25, 0.15, 0.15, 0.15, 0.05]
                )
            else:
                feature_importance = np.random.choice(
                    questions['feature_importance']['options'],
                    p=[0.2, 0.15, 0.3, 0.1, 0.15, 0.1]
                )
            
            # Generate usage frequency
            usage_frequency = np.random.choice(
                questions['usage_frequency']['options'],
                p=[0.4, 0.3, 0.15, 0.1, 0.05]
            )
            
            # Generate open-ended feedback
            feedback_templates = {
                'positive': [
                    "Great product, very user-friendly!",
                    "Excellent tool for data analysis.",
                    "Love the features and support.",
                    "Best tool I've used so far.",
                    "Highly recommended for beginners."
                ],
                'neutral': [
                    "It's okay, does the job.",
                    "Could use some improvements.",
                    "Decent product overall.",
                    "Works as expected.",
                    "Average experience."
                ],
                'negative': [
                    "Needs better documentation.",
                    "Too expensive for what it offers.",
                    "Customer support could be better.",
                    "Some features are buggy.",
                    "Learning curve is too steep."
                ]
            }
            
            if satisfaction >= 4:
                feedback = random.choice(feedback_templates['positive'])
            elif satisfaction == 3:
                feedback = random.choice(feedback_templates['neutral'])
            else:
                feedback = random.choice(feedback_templates['negative'])
            
            # Add some detailed feedback for specific cases
            if preferred_tool == 'Python' and satisfaction >= 4:
                feedback += " Python ecosystem is amazing!"
            elif preferred_tool == 'Excel' and satisfaction <= 2:
                feedback += " Excel is too limiting for big data."
            
            # Create response record
            record = {
                'response_id': response_id,
                'timestamp': timestamp,
                'region': region,
                'age_group': age_group,
                'gender': gender,
                'occupation': occupation,
                'education_level': education_level,
                'preferred_tool': preferred_tool,
                'satisfaction_rating': satisfaction,
                'would_recommend': recommend,
                'support_quality': support_quality,
                'feature_importance': feature_importance,
                'usage_frequency': usage_frequency,
                'feedback': feedback
            }
            
            data.append(record)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        return df, questions
    
    def save_data(self, df, filename='poll_data.csv'):
        """Save generated data to CSV file"""
        df.to_csv(f'data/{filename}', index=False)
        print(f"✅ Data saved to data/{filename}")
        return f'data/{filename}'


# Run generator if executed directly
if __name__ == "__main__":
    generator = PollDataGenerator(seed=42)
    df, questions = generator.generate_poll_data(n_responses=500)
    
    # Display first few rows
    print("\n📊 Generated Poll Data Preview:")
    print(df.head())
    print(f"\n📈 Total responses: {len(df)}")
    print(f"\n📋 Columns: {list(df.columns)}")
    
    # Save data
    generator.save_data(df)
    
    # Display questions
    print("\n📝 Poll Questions:")
    for key, value in questions.items():
        print(f"  • {value['question']}")
        print(f"    Options: {value['options']}")