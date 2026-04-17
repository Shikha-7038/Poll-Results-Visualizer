"""
Analysis Module for Poll Results Visualizer
Performs statistical analysis and aggregations on poll data
"""

import pandas as pd
import numpy as np

class PollAnalyzer:
    def __init__(self, df):
        """
        Initialize analyzer with cleaned DataFrame
        
        Parameters:
        df: pandas DataFrame containing cleaned poll data
        """
        self.df = df
        self.results = {}
        
    def calculate_vote_shares(self, column='preferred_tool'):
        """
        Calculate vote shares/percentages for a categorical column
        
        Parameters:
        column: Column name to analyze
        
        Returns:
        DataFrame with counts and percentages
        """
        counts = self.df[column].value_counts()
        percentages = (counts / len(self.df)) * 100
        
        result_df = pd.DataFrame({
            'count': counts,
            'percentage': percentages.round(2)
        })
        
        self.results[f'{column}_shares'] = result_df
        return result_df
    
    def analyze_by_demographic(self, demographic_col, value_col='preferred_tool'):
        """
        Analyze preferences by demographic groups
        
        Parameters:
        demographic_col: Demographic column (e.g., 'region', 'age_group')
        value_col: Value column to analyze (e.g., 'preferred_tool')
        
        Returns:
        Cross-tabulation DataFrame
        """
        crosstab = pd.crosstab(
            self.df[demographic_col], 
            self.df[value_col], 
            normalize='index'
        ) * 100
        
        self.results[f'{value_col}_by_{demographic_col}'] = crosstab
        return crosstab.round(2)
    
    def calculate_average_ratings(self):
        """Calculate average ratings for different metrics"""
        rating_cols = ['satisfaction_rating', 'recommendation_score', 'support_score']
        existing_cols = [col for col in rating_cols if col in self.df.columns]
        
        if existing_cols:
            avg_ratings = self.df[existing_cols].mean().round(2)
            self.results['average_ratings'] = avg_ratings
            return avg_ratings
        return None
    
    def analyze_by_satisfaction_level(self):
        """Analyze patterns across different satisfaction levels"""
        if 'satisfaction_category' not in self.df.columns:
            return None
        
        satisfaction_analysis = {}
        
        # Tool preference by satisfaction
        tool_by_satisfaction = pd.crosstab(
            self.df['satisfaction_category'],
            self.df['preferred_tool'],
            normalize='index'
        ) * 100
        
        satisfaction_analysis['tool_preference'] = tool_by_satisfaction.round(2)
        
        # Region by satisfaction
        region_by_satisfaction = pd.crosstab(
            self.df['satisfaction_category'],
            self.df['region'],
            normalize='index'
        ) * 100
        
        satisfaction_analysis['region_distribution'] = region_by_satisfaction.round(2)
        
        # Average feedback length by satisfaction
        if 'feedback_length' in self.df.columns:
            feedback_length_by_satisfaction = self.df.groupby('satisfaction_category')['feedback_length'].mean().round(2)
            satisfaction_analysis['avg_feedback_length'] = feedback_length_by_satisfaction
        
        self.results['satisfaction_analysis'] = satisfaction_analysis
        return satisfaction_analysis
    
    def analyze_temporal_trends(self):
        """Analyze trends over time"""
        if 'date' not in self.df.columns:
            return None
        
        temporal_analysis = {}
        
        # Daily responses
        daily_responses = self.df.groupby('date').size()
        temporal_analysis['daily_responses'] = daily_responses
        
        # Average satisfaction over time
        if 'satisfaction_rating' in self.df.columns:
            daily_satisfaction = self.df.groupby('date')['satisfaction_rating'].mean()
            temporal_analysis['daily_satisfaction'] = daily_satisfaction
        
        # Preferred tool trends over time
        # Get top 3 tools overall
        top_tools = self.df['preferred_tool'].value_counts().head(3).index
        tool_trends = {}
        
        for tool in top_tools:
            tool_data = self.df[self.df['preferred_tool'] == tool]
            daily_tool_counts = tool_data.groupby('date').size()
            tool_trends[tool] = daily_tool_counts
        
        temporal_analysis['tool_trends'] = tool_trends
        
        # Day of week patterns
        if 'day_of_week' in self.df.columns:
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            responses_by_day = self.df['day_of_week'].value_counts()
            responses_by_day = responses_by_day.reindex(day_order)
            temporal_analysis['responses_by_day'] = responses_by_day
        
        self.results['temporal_analysis'] = temporal_analysis
        return temporal_analysis
    
    def analyze_correlations(self):
        """Calculate correlations between numeric variables"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            correlations = self.df[numeric_cols].corr()
            self.results['correlations'] = correlations
            return correlations
        return None
    
    def get_top_insights(self):
        """
        Generate key insights from the analysis
        
        Returns:
        Dictionary of key insights
        """
        insights = {}
        
        # Most preferred tool
        tool_shares = self.calculate_vote_shares('preferred_tool')
        top_tool = tool_shares.iloc[0]
        insights['most_preferred_tool'] = {
            'tool': top_tool.name,
            'percentage': top_tool['percentage']
        }
        
        # Average satisfaction
        if 'satisfaction_rating' in self.df.columns:
            avg_satisfaction = self.df['satisfaction_rating'].mean()
            insights['average_satisfaction'] = round(avg_satisfaction, 2)
        
        # Regional analysis
        region_tool = self.analyze_by_demographic('region', 'preferred_tool')
        for region in region_tool.index:
            top_region_tool = region_tool.loc[region].nlargest(1)
            insights[f'{region}_preference'] = {
                'tool': top_region_tool.index[0],
                'percentage': top_region_tool.values[0]
            }
        
        # Age group analysis
        age_tool = self.analyze_by_demographic('age_group', 'preferred_tool')
        for age_group in age_tool.index:
            top_age_tool = age_tool.loc[age_group].nlargest(1)
            insights[f'{age_group}_preference'] = {
                'tool': top_age_tool.index[0],
                'percentage': top_age_tool.values[0]
            }
        
        # Recommendation rate
        if 'would_recommend' in self.df.columns:
            promoters = self.df[self.df['would_recommend'].isin(['Definitely Yes', 'Probably Yes'])].shape[0]
            promoter_rate = (promoters / len(self.df)) * 100
            insights['promoter_rate'] = round(promoter_rate, 2)
        
        # Satisfaction by region
        if 'satisfaction_rating' in self.df.columns:
            region_satisfaction = self.df.groupby('region')['satisfaction_rating'].mean().sort_values(ascending=False)
            insights['highest_satisfaction_region'] = {
                'region': region_satisfaction.index[0],
                'score': round(region_satisfaction.iloc[0], 2)
            }
            insights['lowest_satisfaction_region'] = {
                'region': region_satisfaction.index[-1],
                'score': round(region_satisfaction.iloc[-1], 2)
            }
        
        return insights
    
    def generate_summary_report(self):
        """
        Generate a comprehensive summary report
        
        Returns:
        Dictionary with all analysis results
        """
        summary = {
            'total_responses': len(self.df),
            'unique_respondents': self.df['response_id'].nunique() if 'response_id' in self.df.columns else len(self.df),
            'date_range': {
                'start': self.df['timestamp'].min() if 'timestamp' in self.df.columns else None,
                'end': self.df['timestamp'].max() if 'timestamp' in self.df.columns else None
            },
            'demographics': {
                'regions': self.df['region'].nunique() if 'region' in self.df.columns else 0,
                'age_groups': self.df['age_group'].nunique() if 'age_group' in self.df.columns else 0,
                'occupations': self.df['occupation'].nunique() if 'occupation' in self.df.columns else 0
            },
            'vote_shares': self.calculate_vote_shares('preferred_tool').to_dict(),
            'average_ratings': self.calculate_average_ratings(),
            'top_insights': self.get_top_insights()
        }
        
        self.results['summary_report'] = summary
        return summary
    
    def get_all_results(self):
        """Return all analysis results"""
        return self.results


# Run analysis if executed directly
if __name__ == "__main__":
    # Load cleaned data
    cleaned_df = pd.read_csv('data/cleaned_poll_data.csv')
    
    # Initialize analyzer
    analyzer = PollAnalyzer(cleaned_df)
    
    print("=" * 60)
    print("📊 POLL RESULTS ANALYSIS")
    print("=" * 60)
    
    # Generate summary report
    print("\n📈 SUMMARY REPORT")
    print("-" * 40)
    summary = analyzer.generate_summary_report()
    print(f"Total Responses: {summary['total_responses']}")
    print(f"Unique Respondents: {summary['unique_respondents']}")
    
    print("\n🏆 VOTE SHARES (Preferred Tools)")
    print("-" * 40)
    vote_shares = analyzer.calculate_vote_shares('preferred_tool')
    print(vote_shares)
    
    print("\n⭐ AVERAGE RATINGS")
    print("-" * 40)
    avg_ratings = analyzer.calculate_average_ratings()
    if avg_ratings is not None:
        print(avg_ratings)
    
    print("\n🌍 REGIONAL PREFERENCES")
    print("-" * 40)
    region_analysis = analyzer.analyze_by_demographic('region', 'preferred_tool')
    print(region_analysis)
    
    print("\n👥 AGE GROUP PREFERENCES")
    print("-" * 40)
    age_analysis = analyzer.analyze_by_demographic('age_group', 'preferred_tool')
    print(age_analysis)
    
    print("\n💡 TOP INSIGHTS")
    print("-" * 40)
    insights = analyzer.get_top_insights()
    for key, value in insights.items():
        print(f"  • {key}: {value}")