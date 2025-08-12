"""
VAD Testing Dashboard - Generate visual reports and comparisons.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import seaborn as sns

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class VADDashboard:
    """Generate visual dashboards and reports for VAD testing results."""
    
    def __init__(self, results_dir: str = "test_results", output_dir: str = "reports"):
        self.results_dir = Path(results_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def load_results(self, filename: str = None) -> List[Dict]:
        """Load test results from JSON file."""
        
        if filename:
            filepath = self.results_dir / filename
        else:
            # Load the most recent results file
            json_files = list(self.results_dir.glob("*.json"))
            if not json_files:
                raise FileNotFoundError("No result files found")
            
            filepath = max(json_files, key=lambda x: x.stat().st_mtime)
            print(f"Loading most recent results: {filepath.name}")
        
        with open(filepath, 'r') as f:
            results = json.load(f)
        
        print(f"Loaded {len(results)} test results")
        return results
    
    def create_performance_comparison(self, results: List[Dict], save_path: str = None) -> str:
        """Create a comprehensive performance comparison chart."""
        
        if not results:
            raise ValueError("No results to plot")
        
        # Extract data for plotting
        scores = [r['overall_score'] for r in results]
        key_words = [r['key_words_detected'] * 100 for r in results]  # Convert to percentage
        sequence_sim = [r['sequence_similarity'] * 100 for r in results]
        word_acc = [r['word_accuracy'] * 100 for r in results]
        
        # Create parameter labels
        param_labels = []
        for r in results:
            params = r['vad_params']
            label = f"A{params['aggressiveness']}_S{params['start_gate_ms']}_E{params['end_gate_ms']}_V{params['volume_threshold']}"
            param_labels.append(label)
        
        # Create the plot
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Overall scores
        ax1.bar(range(len(scores)), scores, color='skyblue', alpha=0.7)
        ax1.set_title('Overall Performance Scores')
        ax1.set_ylabel('Score (0-100)')
        ax1.set_xlabel('Parameter Combinations')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, v in enumerate(scores):
            ax1.text(i, v + 1, f'{v:.1f}', ha='center', va='bottom')
        
        # Key words detection
        ax2.bar(range(len(key_words)), key_words, color='lightgreen', alpha=0.7)
        ax2.set_title('Key Words Detection Rate')
        ax2.set_ylabel('Detection Rate (%)')
        ax2.set_xlabel('Parameter Combinations')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        # Sequence similarity
        ax3.bar(range(len(sequence_sim)), sequence_sim, color='lightcoral', alpha=0.7)
        ax3.set_title('Sequence Similarity')
        ax3.set_ylabel('Similarity (%)')
        ax3.set_xlabel('Parameter Combinations')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Word accuracy
        ax4.bar(range(len(word_acc)), word_acc, color='gold', alpha=0.7)
        ax4.set_title('Word Accuracy')
        ax4.set_ylabel('Accuracy (%)')
        ax4.set_xlabel('Parameter Combinations')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3)
        
        # Adjust layout
        plt.tight_layout()
        plt.suptitle('VAD Performance Comparison Dashboard', fontsize=16, y=1.02)
        
        # Save plot
        if not save_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = self.output_dir / f"vad_performance_comparison_{timestamp}.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📊 Performance comparison saved to {save_path}")
        
        return str(save_path)
    
    def create_parameter_heatmaps(self, results: List[Dict], save_path: str = None) -> str:
        """Create heatmaps showing parameter effects on performance."""
        
        if not results:
            raise ValueError("No results to plot")
        
        # Convert results to DataFrame for easier analysis
        data = []
        for r in results:
            params = r['vad_params']
            data.append({
                'aggressiveness': params['aggressiveness'],
                'start_gate_ms': params['start_gate_ms'],
                'end_gate_ms': params['end_gate_ms'],
                'volume_threshold': params['volume_threshold'],
                'overall_score': r['overall_score'],
                'key_words_detected': r['key_words_detected'] * 100,
                'sequence_similarity': r['sequence_similarity'] * 100,
                'word_accuracy': r['word_accuracy'] * 100
            })
        
        df = pd.DataFrame(data)
        
        # Create heatmaps
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Heatmap 1: Aggressiveness vs Start Gate (Overall Score)
        pivot1 = df.pivot_table(values='overall_score', 
                               index='aggressiveness', 
                               columns='start_gate_ms', 
                               aggfunc='mean')
        
        sns.heatmap(pivot1, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax1)
        ax1.set_title('Overall Score vs Aggressiveness & Start Gate')
        
        # Heatmap 2: End Gate vs Volume Threshold (Overall Score)
        pivot2 = df.pivot_table(values='overall_score',
                               index='end_gate_ms',
                               columns='volume_threshold', 
                               aggfunc='mean')
        
        sns.heatmap(pivot2, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax2)
        ax2.set_title('Overall Score vs End Gate & Volume Threshold')
        
        # Heatmap 3: Aggressiveness vs End Gate (Key Words Detection)
        pivot3 = df.pivot_table(values='key_words_detected',
                               index='aggressiveness',
                               columns='end_gate_ms',
                               aggfunc='mean')
        
        sns.heatmap(pivot3, annot=True, fmt='.1f', cmap='YlGnBu', ax=ax3)
        ax3.set_title('Key Words Detection vs Aggressiveness & End Gate')
        
        # Heatmap 4: Start Gate vs Volume Threshold (Sequence Similarity)
        pivot4 = df.pivot_table(values='sequence_similarity',
                               index='start_gate_ms',
                               columns='volume_threshold',
                               aggfunc='mean')
        
        sns.heatmap(pivot4, annot=True, fmt='.1f', cmap='YlGnBu', ax=ax4)
        ax4.set_title('Sequence Similarity vs Start Gate & Volume Threshold')
        
        plt.tight_layout()
        plt.suptitle('VAD Parameter Effect Heatmaps', fontsize=16, y=1.02)
        
        # Save plot
        if not save_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = self.output_dir / f"vad_parameter_heatmaps_{timestamp}.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"🔥 Parameter heatmaps saved to {save_path}")
        
        return str(save_path)
    
    def create_optimization_curve(self, results: List[Dict], save_path: str = None) -> str:
        """Create optimization curve showing best scores over parameter combinations."""
        
        if not results:
            raise ValueError("No results to plot")
        
        # Sort results by score
        sorted_results = sorted(results, key=lambda x: x['overall_score'], reverse=True)
        
        scores = [r['overall_score'] for r in sorted_results]
        cumulative_best = []
        current_best = 0
        
        for score in scores:
            current_best = max(current_best, score)
            cumulative_best.append(current_best)
        
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Optimization curve
        ax1.plot(range(1, len(scores) + 1), scores, 'b-', alpha=0.6, label='Individual Scores')
        ax1.plot(range(1, len(cumulative_best) + 1), cumulative_best, 'r-', linewidth=3, label='Best Score So Far')
        ax1.set_xlabel('Parameter Combination (ranked by score)')
        ax1.set_ylabel('Overall Score')
        ax1.set_title('VAD Optimization Progress')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Score distribution
        ax2.hist(scores, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.axvline(np.mean(scores), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(scores):.1f}')
        ax2.axvline(np.max(scores), color='green', linestyle='--', linewidth=2, label=f'Best: {np.max(scores):.1f}')
        ax2.set_xlabel('Overall Score')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Score Distribution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        if not save_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = self.output_dir / f"vad_optimization_curve_{timestamp}.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📈 Optimization curve saved to {save_path}")
        
        return str(save_path)
    
    def create_correlation_analysis(self, results: List[Dict], save_path: str = None) -> str:
        """Create correlation analysis between parameters and performance metrics."""
        
        if not results:
            raise ValueError("No results to plot")
        
        # Prepare data
        data = []
        for r in results:
            params = r['vad_params']
            data.append({
                'Aggressiveness': params['aggressiveness'],
                'Start Gate (ms)': params['start_gate_ms'],
                'End Gate (ms)': params['end_gate_ms'],
                'Volume Threshold': params['volume_threshold'],
                'Overall Score': r['overall_score'],
                'Key Words Detected': r['key_words_detected'],
                'Sequence Similarity': r['sequence_similarity'],
                'Word Accuracy': r['word_accuracy'],
            })
        
        df = pd.DataFrame(data)
        
        # Calculate correlation matrix
        corr_matrix = df.corr()
        
        # Create correlation heatmap
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))  # Mask upper triangle
        
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.3f', 
                   cmap='RdBu_r', center=0, square=True, 
                   linewidths=0.5, cbar_kws={"shrink": .8})
        
        plt.title('Parameter-Performance Correlation Matrix', fontsize=16, pad=20)
        plt.tight_layout()
        
        # Save plot
        if not save_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = self.output_dir / f"vad_correlation_analysis_{timestamp}.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"🔗 Correlation analysis saved to {save_path}")
        
        return str(save_path)
    
    def generate_summary_report(self, results: List[Dict], save_path: str = None) -> str:
        """Generate a comprehensive summary report."""
        
        if not results:
            raise ValueError("No results to analyze")
        
        # Calculate statistics
        scores = [r['overall_score'] for r in results]
        best_result = max(results, key=lambda x: x['overall_score'])
        worst_result = min(results, key=lambda x: x['overall_score'])
        
        # Generate report text
        report = []
        report.append("# VAD Performance Analysis Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Tests: {len(results)}")
        report.append("")
        
        # Summary Statistics
        report.append("## Summary Statistics")
        report.append(f"- **Average Score**: {np.mean(scores):.2f}")
        report.append(f"- **Best Score**: {np.max(scores):.2f}")
        report.append(f"- **Worst Score**: {np.min(scores):.2f}")
        report.append(f"- **Standard Deviation**: {np.std(scores):.2f}")
        report.append(f"- **Score Range**: {np.max(scores) - np.min(scores):.2f}")
        report.append("")
        
        # Best Configuration
        report.append("## Best Configuration")
        report.append(f"**Score**: {best_result['overall_score']:.2f}")
        for param, value in best_result['vad_params'].items():
            report.append(f"- **{param.replace('_', ' ').title()}**: {value}")
        
        report.append("")
        report.append("### Performance Breakdown:")
        report.append(f"- **Key Words Detected**: {best_result['key_words_detected']:.3f}")
        report.append(f"- **Sequence Similarity**: {best_result['sequence_similarity']:.3f}")
        report.append(f"- **Word Accuracy**: {best_result['word_accuracy']:.3f}")
        
        if 'fuzzy_ratio' in best_result:
            report.append(f"- **Fuzzy Match**: {best_result['fuzzy_ratio']:.1f}%")
        
        report.append("")
        
        # Worst Configuration (for comparison)
        report.append("## Worst Configuration (for comparison)")
        report.append(f"**Score**: {worst_result['overall_score']:.2f}")
        for param, value in worst_result['vad_params'].items():
            report.append(f"- **{param.replace('_', ' ').title()}**: {value}")
        report.append("")
        
        # Parameter Analysis
        report.append("## Parameter Analysis")
        
        # Group by each parameter and find best values
        params_df = pd.DataFrame([r['vad_params'] for r in results])
        scores_series = pd.Series(scores)
        
        for param in params_df.columns:
            param_performance = params_df.groupby(param).apply(
                lambda x: scores_series[x.index].mean()
            )
            best_value = param_performance.idxmax()
            best_score = param_performance.max()
            
            report.append(f"### {param.replace('_', ' ').title()}")
            report.append(f"- **Best Value**: {best_value} (avg score: {best_score:.2f})")
            
            # Show all values and their performance
            for value, score in param_performance.sort_values(ascending=False).items():
                report.append(f"  - {value}: {score:.2f}")
            report.append("")
        
        # Recommendations
        report.append("## Recommendations")
        
        # Identify patterns in top performers
        top_performers = sorted(results, key=lambda x: x['overall_score'], reverse=True)[:5]
        
        report.append("### Based on Top 5 Performers:")
        
        # Analyze common characteristics
        for param in ['aggressiveness', 'start_gate_ms', 'end_gate_ms', 'volume_threshold']:
            values = [r['vad_params'][param] for r in top_performers]
            if len(set(values)) == 1:
                report.append(f"- **{param.replace('_', ' ').title()}**: Consistently use {values[0]}")
            else:
                most_common = max(set(values), key=values.count)
                report.append(f"- **{param.replace('_', ' ').title()}**: Most often {most_common} (appears {values.count(most_common)}/5 times)")
        
        report.append("")
        report.append("### Next Steps:")
        report.append("1. Test the best configuration with more audio samples")
        report.append("2. Fine-tune parameters around the optimal values found")
        report.append("3. Test with different types of audio (noisy, quiet, different speakers)")
        report.append("4. Consider hybrid approaches combining multiple parameter sets")
        
        # Save report
        if not save_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = self.output_dir / f"vad_analysis_report_{timestamp}.md"
        
        with open(save_path, 'w') as f:
            f.write('\n'.join(report))
        
        print(f"📝 Summary report saved to {save_path}")
        
        return str(save_path)
    
    def create_full_dashboard(self, results_file: str = None) -> Dict[str, str]:
        """Create a complete dashboard with all visualizations and reports."""
        
        print("📊 Creating comprehensive VAD dashboard...")
        
        # Load results
        results = self.load_results(results_file)
        
        if not results:
            raise ValueError("No results to analyze")
        
        # Generate all visualizations and reports
        outputs = {}
        
        try:
            outputs['performance_comparison'] = self.create_performance_comparison(results)
        except Exception as e:
            print(f"❌ Error creating performance comparison: {e}")
        
        try:
            outputs['parameter_heatmaps'] = self.create_parameter_heatmaps(results)
        except Exception as e:
            print(f"❌ Error creating parameter heatmaps: {e}")
        
        try:
            outputs['optimization_curve'] = self.create_optimization_curve(results)
        except Exception as e:
            print(f"❌ Error creating optimization curve: {e}")
        
        try:
            outputs['correlation_analysis'] = self.create_correlation_analysis(results)
        except Exception as e:
            print(f"❌ Error creating correlation analysis: {e}")
        
        try:
            outputs['summary_report'] = self.generate_summary_report(results)
        except Exception as e:
            print(f"❌ Error generating summary report: {e}")
        
        print(f"\n🎉 Dashboard complete! Generated {len(outputs)} outputs:")
        for name, path in outputs.items():
            print(f"  📄 {name}: {path}")
        
        return outputs


def main():
    """Main function for dashboard generation."""
    
    print("📊 VAD Testing Dashboard Generator")
    print("=" * 50)
    
    dashboard = VADDashboard()
    
    try:
        # Check for matplotlib and seaborn
        import matplotlib
        import seaborn
        print("✅ Visualization libraries available")
        
        # Generate dashboard
        outputs = dashboard.create_full_dashboard()
        
        print("\n🎯 Dashboard generation complete!")
        
    except ImportError as e:
        print(f"❌ Missing visualization libraries: {e}")
        print("Install with: pip install matplotlib seaborn pandas")
        
    except Exception as e:
        print(f"❌ Error generating dashboard: {e}")


if __name__ == "__main__":
    main()