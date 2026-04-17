"""
Data Cleaning Module for Poll Results Visualizer
Handles missing values, duplicates, and data standardization
"""

import pandas as pd
import numpy as np
from datetime import datetime

class DataCleaner:
    def __init__(self, df):
        """
        Initialize cleaner with DataFrame
        
        Parameters:
        df: pandas DataFrame containing poll data
        """
        self.df = df.copy()
        self.cleaning_report = {}
        
    def get_initial_report(self):
        """Generate initial data quality report"""
        report = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'duplicates': self.df.duplicated().sum(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'data_types': self.df.dtypes.astype(str).to_dict()
        }
        return report
    
    def remove_duplicates(self):
        """Remove duplicate rows"""
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = initial_count - len(self.df)
        self.cleaning_report['duplicates_removed'] = removed
        print(f"🗑️ Removed {removed} duplicate rows")
        return self
    
    def handle_missing_values(self):
        """Handle missing values in different columns"""
        missing_before = self.df.isnull().sum().sum()
        
        # For numeric columns, fill with median
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            self.df[col] = self.df[col].fillna(self.df[col].median())
        
        # For categorical columns, fill with mode
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            self.df[col] = self.df[col].fillna(self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else 'Unknown')
        
        missing_after = self.df.isnull().sum().sum()
        self.cleaning_report['missing_values_filled'] = missing_before - missing_after
        print(f"📝 Filled {missing_before - missing_after} missing values")
        return self
    
    def standardize_text_columns(self):
        """Standardize text columns (strip spaces, title case, etc.)"""
        text_cols = self.df.select_dtypes(include=['object']).columns
        
        for col in text_cols:
            if col != 'feedback':  # Keep feedback as is but strip spaces
                self.df[col] = self.df[col].str.strip().str.title()
            else:
                self.df[col] = self.df[col].str.strip()
        
        print("✏️ Standardized text columns")
        return self
    
    def convert_data_types(self):
        """Convert columns to appropriate data types"""
        # Convert timestamp to datetime
        if 'timestamp' in self.df.columns:
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            # Extract date and time components
            self.df['date'] = self.df['timestamp'].dt.date
            self.df['hour'] = self.df['timestamp'].dt.hour
            self.df['day_of_week'] = self.df['timestamp'].dt.day_name()
            self.df['month'] = self.df['timestamp'].dt.month_name()
        
        # Ensure satisfaction rating is integer
        if 'satisfaction_rating' in self.df.columns:
            self.df['satisfaction_rating'] = self.df['satisfaction_rating'].astype(int)
        
        print("🔄 Converted data types")
        return self
    
    def create_analysis_features(self):
        """Create additional features for deeper analysis"""
        # Create satisfaction category
        if 'satisfaction_rating' in self.df.columns:
            self.df['satisfaction_category'] = pd.cut(
                self.df['satisfaction_rating'],
                bins=[0, 2, 3, 5],
                labels=['Low', 'Medium', 'High']
            )
        
        # Create feedback length feature
        if 'feedback' in self.df.columns:
            self.df['feedback_length'] = self.df['feedback'].astype(str).apply(len)
        
        # Create recommendation score (numeric)
        if 'would_recommend' in self.df.columns:
            recommend_map = {
                'Definitely Yes': 5,
                'Probably Yes': 4,
                'Not Sure': 3,
                'Probably No': 2,
                'Definitely No': 1
            }
            self.df['recommendation_score'] = self.df['would_recommend'].map(recommend_map)
        
        # Create support quality score
        if 'support_quality' in self.df.columns:
            support_map = {
                'Excellent': 5,
                'Good': 4,
                'Average': 3,
                'Poor': 2,
                'Very Poor': 1
            }
            self.df['support_score'] = self.df['support_quality'].map(support_map)
        
        print("✨ Created analysis features")
        return self
    
    def validate_data(self):
        """Validate data quality after cleaning"""
        validation = {
            'no_missing_values': self.df.isnull().sum().sum() == 0,
            'no_duplicates': self.df.duplicated().sum() == 0,
            'valid_satisfaction': self.df['satisfaction_rating'].between(1, 5).all() if 'satisfaction_rating' in self.df.columns else True,
            'valid_timestamps': pd.api.types.is_datetime64_any_dtype(self.df['timestamp']) if 'timestamp' in self.df.columns else True
        }
        
        self.cleaning_report['validation'] = validation
        
        print("\n✅ Validation Results:")
        for check, passed in validation.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check}: {passed}")
        
        return self
    
    def get_cleaned_data(self):
        """Return cleaned DataFrame"""
        return self.df
    
    def get_cleaning_report(self):
        """Return cleaning report"""
        return self.cleaning_report
    
    def save_cleaned_data(self, filename='cleaned_poll_data.csv'):
        """Save cleaned data to CSV"""
        self.df.to_csv(f'data/{filename}', index=False)
        print(f"\n💾 Cleaned data saved to data/{filename}")
        return f'data/{filename}'


# Run cleaner if executed directly
if __name__ == "__main__":
    # Load raw data
    raw_df = pd.read_csv('data/poll_data.csv')
    
    # Clean data
    cleaner = DataCleaner(raw_df)
    
    print("=" * 50)
    print("📊 INITIAL DATA REPORT")
    print("=" * 50)
    initial_report = cleaner.get_initial_report()
    print(f"Total rows: {initial_report['total_rows']}")
    print(f"Total columns: {initial_report['total_columns']}")
    print(f"Duplicates: {initial_report['duplicates']}")
    print(f"Missing values: {sum(initial_report['missing_values'].values())}")
    
    print("\n" + "=" * 50)
    print("🧹 CLEANING PROCESS")
    print("=" * 50)
    
    cleaner.remove_duplicates() \
           .handle_missing_values() \
           .standardize_text_columns() \
           .convert_data_types() \
           .create_analysis_features() \
           .validate_data()
    
    # Get cleaned data
    cleaned_df = cleaner.get_cleaned_data()
    
    print("\n" + "=" * 50)
    print("📊 CLEANED DATA PREVIEW")
    print("=" * 50)
    print(cleaned_df.head())
    
    print("\n" + "=" * 50)
    print("📊 CLEANED DATA INFO")
    print("=" * 50)
    print(cleaned_df.info())
    
    # Save cleaned data
    cleaner.save_cleaned_data()