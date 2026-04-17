"""
Main entry point for Poll Results Visualizer
Runs the complete pipeline: data generation → cleaning → analysis → visualization → insights
"""

import os
import sys
import pandas as pd

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_generator import PollDataGenerator
from src.data_cleaner import DataCleaner
from src.analysis import PollAnalyzer
from src.visualizations import PollVisualizer
from src.insights import InsightsGenerator

def create_directory_structure():
    """Create necessary directories if they don't exist"""
    directories = ['data', 'outputs', 'images', 'notebooks']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directory structure created")

def run_complete_pipeline(n_responses=500, save_intermediate=True):
    """
    Run the complete poll results visualization pipeline
    
    Parameters:
    n_responses: Number of responses to generate
    save_intermediate: Whether to save intermediate files
    """
    
    print("\n" + "=" * 70)
    print("🎯 POLL RESULTS VISUALIZER - COMPLETE PIPELINE")
    print("=" * 70)
    
    # Step 1: Create directory structure
    print("\n📁 STEP 1: Creating directory structure")
    print("-" * 40)
    create_directory_structure()
    
    # Step 2: Generate synthetic data
    print("\n📊 STEP 2: Generating synthetic poll data")
    print("-" * 40)
    generator = PollDataGenerator(seed=42)
    df, questions = generator.generate_poll_data(n_responses=n_responses)
    
    if save_intermediate:
        generator.save_data(df, 'poll_data.csv')
    
    print(f"✅ Generated {len(df)} responses")
    print(f"📋 Columns: {list(df.columns)}")
    
    # Step 3: Clean data
    print("\n🧹 STEP 3: Cleaning and preprocessing data")
    print("-" * 40)
    cleaner = DataCleaner(df)
    cleaner.remove_duplicates() \
           .handle_missing_values() \
           .standardize_text_columns() \
           .convert_data_types() \
           .create_analysis_features() \
           .validate_data()
    
    cleaned_df = cleaner.get_cleaned_data()
    
    if save_intermediate:
        cleaner.save_cleaned_data('cleaned_poll_data.csv')
    
    print(f"✅ Cleaned data: {len(cleaned_df)} rows, {len(cleaned_df.columns)} columns")
    
    # Step 4: Analyze data
    print("\n📈 STEP 4: Analyzing poll data")
    print("-" * 40)
    analyzer = PollAnalyzer(cleaned_df)
    summary = analyzer.generate_summary_report()
    
    print(f"\n📊 Analysis Summary:")
    print(f"   • Total Responses: {summary['total_responses']}")
    print(f"   • Date Range: {summary['date_range']['start']} to {summary['date_range']['end']}")
    print(f"   • Regions Covered: {summary['demographics']['regions']}")
    print(f"   • Age Groups: {summary['demographics']['age_groups']}")
    
    # Display vote shares
    print(f"\n🏆 Vote Shares:")
    vote_shares = analyzer.calculate_vote_shares('preferred_tool')
    for tool, row in vote_shares.iterrows():
        print(f"   • {tool}: {row['count']} votes ({row['percentage']:.1f}%)")
    
    # Step 5: Generate visualizations
    print("\n📊 STEP 5: Generating visualizations")
    print("-" * 40)
    visualizer = PollVisualizer(cleaned_df, output_dir='outputs')
    visualizer.generate_all_visualizations()
    
    # Step 6: Generate insights
    print("\n💡 STEP 6: Generating insights and recommendations")
    print("-" * 40)
    results = analyzer.get_all_results()
    insights_gen = InsightsGenerator(cleaned_df, results)
    insights_gen.print_insights()
    
    # Step 7: Save insights report
    print("\n💾 STEP 7: Saving reports")
    print("-" * 40)
    
    # Save summary report
    report = insights_gen.generate_full_report()
    
    # Save as text file
    with open('outputs/insights_report.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("POLL RESULTS VISUALIZER - INSIGHTS REPORT\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Generated: {report['generated_at']}\n")
        f.write(f"Total Responses: {report['total_responses']}\n\n")
        
        f.write("KEY FINDINGS\n")
        f.write("-" * 40 + "\n")
        for finding in report['key_findings']:
            f.write(f"\n[{finding['category']}]\n")
            f.write(f"Finding: {finding['finding']}\n")
            f.write(f"Recommendation: {finding['recommendation']}\n")
        
        f.write("\n\nRECOMMENDATIONS\n")
        f.write("-" * 40 + "\n")
        for rec in report['recommendations']:
            f.write(f"\n[{rec['priority']}] {rec['action']}\n")
            f.write(f"Impact: {rec['impact']}\n")
        
        f.write("\n\n" + report['executive_summary'])
    
    print("✅ Insights report saved to outputs/insights_report.txt")
    
    # Save summary statistics
    summary_df = pd.DataFrame({
        'Metric': ['Total Responses', 'Unique Respondents', 'Average Satisfaction', 'Promoter Rate'],
        'Value': [
            summary['total_responses'],
            summary['unique_respondents'],
            f"{summary['average_ratings']['satisfaction_rating']:.2f}" if summary['average_ratings'] is not None else 'N/A',
            f"{summary['top_insights'].get('promoter_rate', 'N/A')}"
        ]
    })
    summary_df.to_csv('outputs/summary_statistics.csv', index=False)
    print("✅ Summary statistics saved to outputs/summary_statistics.csv")
    
    print("\n" + "=" * 70)
    print("✅ POLL RESULTS VISUALIZER - PIPELINE COMPLETE!")
    print("=" * 70)
    
    print("\n📁 Output files generated:")
    print("   • data/poll_data.csv - Raw synthetic data")
    print("   • data/cleaned_poll_data.csv - Cleaned data")
    print("   • outputs/*.png - Visualization charts")
    print("   • outputs/interactive_dashboard.html - Interactive dashboard")
    print("   • outputs/insights_report.txt - Detailed insights report")
    print("   • outputs/summary_statistics.csv - Summary statistics")
    
    return cleaned_df, results, report


if __name__ == "__main__":
    # Run the complete pipeline
    df, results, report = run_complete_pipeline(n_responses=500)