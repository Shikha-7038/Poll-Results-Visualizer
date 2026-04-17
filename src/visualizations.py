"""
Visualization Module for Poll Results Visualizer
Creates professional charts and graphs for poll data
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Set style for better looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class PollVisualizer:
    def __init__(self, df, output_dir='outputs'):
        """
        Initialize visualizer with DataFrame
        
        Parameters:
        df: pandas DataFrame containing poll data
        output_dir: Directory to save visualizations
        """
        self.df = df
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Set color schemes
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        
    def create_bar_chart(self, column='preferred_tool', title=None, save=True):
        """
        Create bar chart for categorical data
        
        Parameters:
        column: Column to visualize
        title: Chart title
        save: Whether to save the figure
        """
        if title is None:
            title = f'Distribution of {column.replace("_", " ").title()}'
        
        # Calculate counts and percentages
        counts = self.df[column].value_counts()
        percentages = (counts / len(self.df)) * 100
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create bars
        bars = ax.bar(range(len(counts)), counts.values, color=self.colors, edgecolor='black', linewidth=1)
        
        # Add percentage labels on bars
        for i, (bar, pct) in enumerate(zip(bars, percentages.values)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{pct:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Customize chart
        ax.set_xlabel(column.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Responses', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(range(len(counts.index)))
        ax.set_xticklabels(counts.index, rotation=45, ha='right')
        
        # Add grid
        ax.grid(axis='y', alpha=0.3)
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/bar_chart_{column}.png', dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {self.output_dir}/bar_chart_{column}.png")
        
        plt.show()
        return fig
    
    def create_pie_chart(self, column='preferred_tool', title=None, save=True):
        """
        Create pie chart for categorical data
        
        Parameters:
        column: Column to visualize
        title: Chart title
        save: Whether to save the figure
        """
        if title is None:
            title = f'Distribution of {column.replace("_", " ").title()}'
        
        counts = self.df[column].value_counts()
        percentages = (counts / len(self.df)) * 100
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            counts.values, 
            labels=counts.index,
            autopct=lambda pct: f'{pct:.1f}%\n({int(pct*len(self.df)/100)} votes)',
            colors=self.colors,
            startangle=90,
            explode=[0.02] * len(counts)
        )
        
        # Style the text
        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/pie_chart_{column}.png', dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {self.output_dir}/pie_chart_{column}.png")
        
        plt.show()
        return fig
    
    def create_stacked_bar_chart(self, demographic_col, value_col='preferred_tool', save=True):
        """
        Create stacked bar chart for demographic comparison
        
        Parameters:
        demographic_col: Demographic column (e.g., 'region')
        value_col: Value column to compare
        save: Whether to save the figure
        """
        # Create crosstab
        crosstab = pd.crosstab(self.df[demographic_col], self.df[value_col], normalize='index') * 100
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create stacked bars
        crosstab.plot(kind='bar', stacked=True, ax=ax, color=self.colors, edgecolor='black', linewidth=0.5)
        
        # Customize chart
        ax.set_xlabel(demographic_col.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'Tool Preferences by {demographic_col.replace("_", " ").title()}', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(title=value_col.replace('_', ' ').title(), bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Add percentage labels on bars
        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f%%', fontsize=8, label_type='center')
        
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/stacked_bar_{demographic_col}_vs_{value_col}.png', 
                       dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {self.output_dir}/stacked_bar_{demographic_col}_vs_{value_col}.png")
        
        plt.show()
        return fig
    
    def create_satisfaction_histogram(self, save=True):
        """
        Create histogram of satisfaction ratings
        """
        if 'satisfaction_rating' not in self.df.columns:
            print("⚠️ Satisfaction rating column not found")
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create histogram
        n, bins, patches = ax.hist(self.df['satisfaction_rating'], 
                                   bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5],
                                   color=self.colors[0], 
                                   edgecolor='black', 
                                   alpha=0.7,
                                   rwidth=0.8)
        
        # Add count labels
        for i, count in enumerate(n):
            ax.text(bins[i] + 0.5, count + 1, str(int(count)), 
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Customize chart
        ax.set_xlabel('Satisfaction Rating', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Responses', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Satisfaction Ratings', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_xticklabels(['1 (Very Low)', '2', '3 (Neutral)', '4', '5 (Very High)'])
        
        # Add grid
        ax.grid(axis='y', alpha=0.3)
        ax.set_axisbelow(True)
        
        # Add mean line
        mean_rating = self.df['satisfaction_rating'].mean()
        ax.axvline(mean_rating, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_rating:.2f}')
        ax.legend()
        
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/satisfaction_histogram.png', dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {self.output_dir}/satisfaction_histogram.png")
        
        plt.show()
        return fig
    
    def create_trend_line_chart(self, save=True):
        """
        Create line chart showing trends over time
        """
        if 'date' not in self.df.columns:
            print("⚠️ Date column not found")
            return None
        
        # Group by date
        daily_counts = self.df.groupby('date').size()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create line chart
        ax.plot(daily_counts.index, daily_counts.values, marker='o', linewidth=2, 
                markersize=6, color=self.colors[0])
        
        # Customize chart
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Responses', fontsize=12, fontweight='bold')
        ax.set_title('Poll Responses Over Time', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        
        # Add trend line
        x = np.arange(len(daily_counts))
        z = np.polyfit(x, daily_counts.values, 1)
        p = np.poly1d(z)
        ax.plot(daily_counts.index, p(x), "r--", alpha=0.8, label='Trend Line')
        
        ax.legend()
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/trend_line_chart.png', dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {self.output_dir}/trend_line_chart.png")
        
        plt.show()
        return fig
    
    def create_wordcloud(self, column='feedback', save=True):
        """
        Create word cloud from text responses
        """
        if column not in self.df.columns:
            print(f"⚠️ Column '{column}' not found")
            return None
        
        # Combine all feedback
        text = ' '.join(self.df[column].astype(str).tolist())
        
        # Create word cloud
        wordcloud = WordCloud(width=1200, height=600, 
                             background_color='white',
                             colormap='viridis',
                             max_words=100,
                             contour_width=1,
                             contour_color='steelblue').generate(text)
        
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Common Words in Customer Feedback', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/wordcloud.png', dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {self.output_dir}/wordcloud.png")
        
        plt.show()
        return fig
    
    def create_boxplot(self, x_col, y_col, save=True):
        """
        Create boxplot to compare distributions
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create boxplot
        self.df.boxplot(column=y_col, by=x_col, ax=ax, grid=True)
        
        # Customize chart
        ax.set_xlabel(x_col.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_ylabel(y_col.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_title(f'{y_col.replace("_", " ").title()} by {x_col.replace("_", " ").title()}', 
                    fontsize=14, fontweight='bold', pad=20)
        plt.suptitle('')  # Remove automatic title
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/boxplot_{x_col}_vs_{y_col}.png', dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {self.output_dir}/boxplot_{x_col}_vs_{y_col}.png")
        
        plt.show()
        return fig
    
    def create_interactive_dashboard(self):
        """
        Create interactive dashboard using Plotly
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Tool Preferences', 'Satisfaction Distribution', 
                          'Responses Over Time', 'Regional Preferences'),
            specs=[[{'type': 'pie'}, {'type': 'xy'}],
                   [{'type': 'xy'}, {'type': 'bar'}]]
        )
        
        # 1. Pie chart for tool preferences
        tool_counts = self.df['preferred_tool'].value_counts()
        fig.add_trace(
            go.Pie(labels=tool_counts.index, values=tool_counts.values, 
                  hole=0.3, name="Tools"),
            row=1, col=1
        )
        
        # 2. Histogram for satisfaction
        satisfaction_counts = self.df['satisfaction_rating'].value_counts().sort_index()
        fig.add_trace(
            go.Bar(x=satisfaction_counts.index, y=satisfaction_counts.values,
                  name="Satisfaction", marker_color=self.colors[0]),
            row=1, col=2
        )
        
        # 3. Line chart for trends
        if 'date' in self.df.columns:
            daily_counts = self.df.groupby('date').size()
            fig.add_trace(
                go.Scatter(x=daily_counts.index, y=daily_counts.values,
                          mode='lines+markers', name="Trends",
                          line=dict(color=self.colors[1], width=2)),
                row=2, col=1
            )
        
        # 4. Bar chart for regional preferences
        region_pref = pd.crosstab(self.df['region'], self.df['preferred_tool'])
        top_tools = self.df['preferred_tool'].value_counts().head(3).index
        for tool in top_tools:
            fig.add_trace(
                go.Bar(x=region_pref.index, y=region_pref[tool], name=tool),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title_text="Poll Results Dashboard",
            showlegend=True,
            height=800,
            template='plotly_white'
        )
        
        # Save as HTML
        fig.write_html(f'{self.output_dir}/interactive_dashboard.html')
        print(f"✅ Saved: {self.output_dir}/interactive_dashboard.html")
        
        return fig
    
    def generate_all_visualizations(self):
        """
        Generate all visualizations at once
        """
        print("\n" + "=" * 50)
        print("📊 GENERATING VISUALIZATIONS")
        print("=" * 50)
        
        # Basic charts
        self.create_bar_chart('preferred_tool')
        self.create_pie_chart('preferred_tool')
        
        # Demographic analysis
        if 'region' in self.df.columns:
            self.create_stacked_bar_chart('region', 'preferred_tool')
        
        if 'age_group' in self.df.columns:
            self.create_stacked_bar_chart('age_group', 'preferred_tool')
        
        # Satisfaction analysis
        if 'satisfaction_rating' in self.df.columns:
            self.create_satisfaction_histogram()
            if 'region' in self.df.columns:
                self.create_boxplot('region', 'satisfaction_rating')
        
        # Temporal analysis
        if 'date' in self.df.columns:
            self.create_trend_line_chart()
        
        # Text analysis
        if 'feedback' in self.df.columns:
            self.create_wordcloud('feedback')
        
        # Interactive dashboard
        self.create_interactive_dashboard()
        
        print("\n✅ All visualizations generated successfully!")


# Run visualizations if executed directly
if __name__ == "__main__":
    # Load cleaned data
    cleaned_df = pd.read_csv('data/cleaned_poll_data.csv')
    
    # Initialize visualizer
    visualizer = PollVisualizer(cleaned_df)
    
    # Generate all visualizations
    visualizer.generate_all_visualizations()