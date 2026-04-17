"""
Insights Generation Module for Poll Results Visualizer
Generates actionable insights from poll data analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime

class InsightsGenerator:
    def __init__(self, df, analysis_results):
        """
        Initialize insights generator
        
        Parameters:
        df: pandas DataFrame with poll data
        analysis_results: Dictionary from PollAnalyzer
        """
        self.df = df
        self.results = analysis_results
        
    def generate_key_findings(self):
        """
        Generate key findings from the analysis
        
        Returns:
        Dictionary of key findings
        """
        findings = []
        
        # Most popular tool
        if 'preferred_tool_shares' in self.results:
            top_tool = self.results['preferred_tool_shares'].iloc[0]
            findings.append({
                'category': 'Popularity',
                'finding': f"{top_tool.name} is the most preferred tool with {top_tool['percentage']:.1f}% of votes.",
                'recommendation': f"Continue investing in {top_tool.name} features and support."
            })
        
        # Satisfaction analysis
        if 'satisfaction_rating' in self.df.columns:
            avg_sat = self.df['satisfaction_rating'].mean()
            if avg_sat >= 4:
                findings.append({
                    'category': 'Satisfaction',
                    'finding': f"Overall satisfaction is high at {avg_sat:.1f}/5.0.",
                    'recommendation': "Maintain current quality and focus on delighting customers."
                })
            elif avg_sat >= 3:
                findings.append({
                    'category': 'Satisfaction',
                    'finding': f"Overall satisfaction is moderate at {avg_sat:.1f}/5.0.",
                    'recommendation': "Identify key pain points and address them to improve satisfaction."
                })
            else:
                findings.append({
                    'category': 'Satisfaction',
                    'finding': f"Overall satisfaction is low at {avg_sat:.1f}/5.0.",
                    'recommendation': "Urgent action needed to address customer concerns."
                })
        
        # Regional analysis
        if 'region' in self.df.columns and 'satisfaction_rating' in self.df.columns:
            region_sat = self.df.groupby('region')['satisfaction_rating'].mean()
            best_region = region_sat.idxmax()
            worst_region = region_sat.idxmin()
            findings.append({
                'category': 'Regional',
                'finding': f"{best_region} region has highest satisfaction ({region_sat[best_region]:.1f}), while {worst_region} region has lowest ({region_sat[worst_region]:.1f}).",
                'recommendation': f"Investigate what works in {best_region} and apply learnings to {worst_region}."
            })
        
        # Age group analysis
        if 'age_group' in self.df.columns and 'preferred_tool' in self.df.columns:
            age_tool = pd.crosstab(self.df['age_group'], self.df['preferred_tool'], normalize='index')
            for age in age_tool.index:
                top_tool = age_tool.loc[age].nlargest(1)
                findings.append({
                    'category': 'Demographic',
                    'finding': f"{age} age group prefers {top_tool.index[0]} ({top_tool.values[0]:.1f}%).",
                    'recommendation': f"Target {age} demographic with {top_tool.index[0]}-specific marketing."
                })
        
        # Recommendation rate
        if 'would_recommend' in self.df.columns:
            promoters = self.df[self.df['would_recommend'].isin(['Definitely Yes', 'Probably Yes'])].shape[0]
            promoter_rate = (promoters / len(self.df)) * 100
            findings.append({
                'category': 'Loyalty',
                'finding': f"{promoter_rate:.1f}% of respondents would recommend our product.",
                'recommendation': "Encourage promoters to leave reviews and share feedback."
            })
        
        # Feedback analysis
        if 'feedback_length' in self.df.columns and 'satisfaction_rating' in self.df.columns:
            high_sat_feedback = self.df[self.df['satisfaction_rating'] >= 4]['feedback_length'].mean()
            low_sat_feedback = self.df[self.df['satisfaction_rating'] <= 2]['feedback_length'].mean()
            if not pd.isna(high_sat_feedback) and not pd.isna(low_sat_feedback):
                findings.append({
                    'category': 'Feedback',
                    'finding': f"High satisfaction customers provide {high_sat_feedback:.0f} characters of feedback vs {low_sat_feedback:.0f} for low satisfaction.",
                    'recommendation': "Engage with satisfied customers for testimonials; follow up with dissatisfied ones for detailed input."
                })
        
        return findings
    
    def generate_recommendations(self):
        """
        Generate actionable recommendations
        
        Returns:
        List of recommendations
        """
        recommendations = []
        
        # Tool-specific recommendations
        if 'preferred_tool_shares' in self.results:
            tool_shares = self.results['preferred_tool_shares']
            low_perf_tools = tool_shares[tool_shares['percentage'] < 10]
            if len(low_perf_tools) > 0:
                recommendations.append({
                    'priority': 'Medium',
                    'action': f"Evaluate low-performing tools: {', '.join(low_perf_tools.index)}",
                    'impact': "Optimize resource allocation"
                })
        
        # Satisfaction improvement
        if 'satisfaction_rating' in self.df.columns:
            low_sat = self.df[self.df['satisfaction_rating'] <= 2]
            if len(low_sat) > 0:
                recommendations.append({
                    'priority': 'High',
                    'action': f"Contact {len(low_sat)} dissatisfied customers for detailed feedback",
                    'impact': "Improve retention and satisfaction"
                })
        
        # Regional focus
        if 'region' in self.df.columns and 'satisfaction_rating' in self.df.columns:
            region_sat = self.df.groupby('region')['satisfaction_rating'].mean()
            low_region = region_sat.idxmin()
            recommendations.append({
                'priority': 'High',
                'action': f"Launch targeted campaign in {low_region} region",
                'impact': "Improve regional satisfaction scores"
            })
        
        # Training recommendations
        if 'support_quality' in self.df.columns:
            poor_support = self.df[self.df['support_quality'].isin(['Poor', 'Very Poor'])].shape[0]
            if poor_support > 0:
                recommendations.append({
                    'priority': 'High',
                    'action': f"Conduct customer support training (affects {poor_support} respondents)",
                    'impact': "Improve support quality ratings"
                })
        
        # Feature development
        if 'feature_importance' in self.df.columns:
            top_features = self.df['feature_importance'].value_counts().head(2)
            recommendations.append({
                'priority': 'Medium',
                'action': f"Prioritize development of: {', '.join(top_features.index)}",
                'impact': "Address top customer needs"
            })
        
        return recommendations
    
    def generate_comparative_insights(self):
        """
        Generate comparative insights between segments
        
        Returns:
        Dictionary of comparative insights
        """
        comparisons = {}
        
        # Gender comparison
        if 'gender' in self.df.columns and 'satisfaction_rating' in self.df.columns:
            gender_sat = self.df.groupby('gender')['satisfaction_rating'].mean()
            comparisons['gender_satisfaction'] = gender_sat.to_dict()
        
        # Occupation comparison
        if 'occupation' in self.df.columns and 'preferred_tool' in self.df.columns:
            occ_tool = pd.crosstab(self.df['occupation'], self.df['preferred_tool'], normalize='index') * 100
            comparisons['occupation_preferences'] = occ_tool.round(2).to_dict()
        
        # Education comparison
        if 'education_level' in self.df.columns and 'satisfaction_rating' in self.df.columns:
            edu_sat = self.df.groupby('education_level')['satisfaction_rating'].mean()
            comparisons['education_satisfaction'] = edu_sat.sort_values(ascending=False).to_dict()
        
        # Temporal comparison - FIXED: Handle date column properly
        if 'date' in self.df.columns:
            try:
                # Convert date column to datetime if it's not already
                if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
                    self.df['date'] = pd.to_datetime(self.df['date'])
                
                # Convert to numeric timestamp for median calculation
                date_numeric = self.df['date'].astype('int64')
                median_numeric = date_numeric.median()
                median_date = pd.to_datetime(median_numeric)
                
                # Compare first half vs second half
                early = self.df[self.df['date'] <= median_date]
                late = self.df[self.df['date'] > median_date]
                
                if 'satisfaction_rating' in self.df.columns and len(early) > 0 and len(late) > 0:
                    comparisons['temporal_satisfaction'] = {
                        'early_period': early['satisfaction_rating'].mean(),
                        'late_period': late['satisfaction_rating'].mean(),
                        'change': late['satisfaction_rating'].mean() - early['satisfaction_rating'].mean(),
                        'median_date': median_date.strftime('%Y-%m-%d')
                    }
            except Exception as e:
                print(f"Warning: Could not compute temporal comparison: {e}")
                comparisons['temporal_satisfaction'] = {'error': 'Could not compute temporal comparison'}
        
        return comparisons
    
    def generate_full_report(self):
        """
        Generate complete insights report
        
        Returns:
        Dictionary with all insights
        """
        report = {
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_responses': len(self.df),
            'key_findings': self.generate_key_findings(),
            'recommendations': self.generate_recommendations(),
            'comparative_insights': self.generate_comparative_insights(),
            'executive_summary': self.generate_executive_summary()
        }
        
        return report
    
    def generate_executive_summary(self):
        """
        Generate executive summary of findings
        
        Returns:
        String with executive summary
        """
        findings = self.generate_key_findings()
        
        summary = "## EXECUTIVE SUMMARY\n\n"
        
        # Overall sentiment
        if 'satisfaction_rating' in self.df.columns:
            avg_sat = self.df['satisfaction_rating'].mean()
            if avg_sat >= 4:
                summary += "✅ **Overall Customer Sentiment: Very Positive**\n"
            elif avg_sat >= 3:
                summary += "⚠️ **Overall Customer Sentiment: Neutral to Positive**\n"
            else:
                summary += "❌ **Overall Customer Sentiment: Needs Improvement**\n"
        
        summary += f"\n**Key Statistics:**\n"
        summary += f"- Total Responses Analyzed: {len(self.df)}\n"
        
        if 'preferred_tool_shares' in self.results:
            top_tool = self.results['preferred_tool_shares'].iloc[0]
            summary += f"- Most Popular Tool: {top_tool.name} ({top_tool['percentage']:.1f}%)\n"
        
        if 'would_recommend' in self.df.columns:
            promoters = self.df[self.df['would_recommend'].isin(['Definitely Yes', 'Probably Yes'])].shape[0]
            promoter_rate = (promoters / len(self.df)) * 100
            summary += f"- Would Recommend: {promoter_rate:.1f}%\n"
        
        summary += "\n**Top 3 Recommendations:**\n"
        recommendations = self.generate_recommendations()
        for i, rec in enumerate(recommendations[:3], 1):
            summary += f"{i}. [{rec['priority']} Priority] {rec['action']}\n"
        
        return summary
    
    def print_insights(self):
        """
        Print insights in a readable format
        """
        report = self.generate_full_report()
        
        print("\n" + "=" * 70)
        print("📊 POLL RESULTS INSIGHTS REPORT")
        print("=" * 70)
        
        print(f"\n📅 Generated: {report['generated_at']}")
        print(f"📈 Total Responses: {report['total_responses']}")
        
        print("\n" + "-" * 70)
        print("🔍 KEY FINDINGS")
        print("-" * 70)
        
        for finding in report['key_findings']:
            print(f"\n📌 [{finding['category']}]")
            print(f"   Finding: {finding['finding']}")
            print(f"   💡 Recommendation: {finding['recommendation']}")
        
        print("\n" + "-" * 70)
        print("🎯 RECOMMENDATIONS")
        print("-" * 70)
        
        for rec in report['recommendations']:
            print(f"\n   🔹 [{rec['priority']}] {rec['action']}")
            print(f"      Impact: {rec['impact']}")
        
        print("\n" + "-" * 70)
        print("📋 COMPARATIVE INSIGHTS")
        print("-" * 70)
        
        comparisons = report['comparative_insights']
        for key, value in comparisons.items():
            print(f"\n   • {key.replace('_', ' ').title()}:")
            if isinstance(value, dict):
                # Handle error case
                if 'error' in value:
                    print(f"      - {value['error']}")
                else:
                    for sub_key, sub_value in list(value.items())[:5]:  # Limit to 5 items
                        if isinstance(sub_value, float):
                            print(f"      - {sub_key}: {sub_value:.2f}")
                        elif isinstance(sub_value, (int, str)):
                            print(f"      - {sub_key}: {sub_value}")
                        else:
                            print(f"      - {sub_key}: {sub_value}")
        
        print("\n" + "-" * 70)
        print(report['executive_summary'])
        print("=" * 70)


# Run insights if executed directly
if __name__ == "__main__":
    # Load cleaned data
    try:
        cleaned_df = pd.read_csv('data/cleaned_poll_data.csv')
        
        # Load analysis results (or run analysis)
        from analysis import PollAnalyzer
        analyzer = PollAnalyzer(cleaned_df)
        analyzer.generate_summary_report()
        results = analyzer.get_all_results()
        
        # Generate insights
        insights_gen = InsightsGenerator(cleaned_df, results)
        insights_gen.print_insights()
    except FileNotFoundError:
        print("Please run main.py first to generate data!")
    except Exception as e:
        print(f"Error: {e}")