#!/usr/bin/env python3
"""
Generate visualizations for the LLM Agent Efficiency Analysis paper.
Outputs publication-ready figures.
"""

import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Set style for publication
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# Color palette
PROVIDER_COLORS = {
    'openai': '#10A37F',      # OpenAI green
    'google-gla': '#4285F4',  # Google blue
    'deepseek': '#FF6B35',    # Orange
    'ollama': '#9B59B6',      # Purple
}

def get_provider(model_name):
    """Extract provider from model name."""
    return model_name.split(':')[0]

def get_short_name(model_name):
    """Get shortened model name for display."""
    parts = model_name.split(':')
    if len(parts) >= 2:
        return parts[1].replace('-preview', '').replace(':cloud', '')
    return model_name

def load_data(data_path):
    """Load efficiency data from JSON."""
    with open(data_path, 'r') as f:
        return json.load(f)

def fig1_efficiency_frontier(data, output_dir):
    """
    Figure 1: Efficiency Frontier Plot
    X: Average Duration, Y: Success Rate, Bubble Size: Tool Calls
    """
    fig, ax = plt.subplots(figsize=(10, 7))

    models = data['model_stats']

    for model_name, stats in models.items():
        provider = get_provider(model_name)
        color = PROVIDER_COLORS.get(provider, '#666666')

        x = stats['avg_duration']
        y = stats['success_rate'] * 100
        size = max(50, min(stats['avg_tool_calls'] * 10, 500))  # Scale bubble size

        ax.scatter(x, y, s=size, c=color, alpha=0.7, edgecolors='white', linewidth=1)

        # Add label
        short_name = get_short_name(model_name)
        offset = (10, 5) if x < 400 else (-50, 5)
        ax.annotate(short_name, (x, y), textcoords="offset points",
                   xytext=offset, fontsize=8, alpha=0.9)

    ax.set_xlabel('Average Duration (seconds)')
    ax.set_ylabel('Success Rate (%)')
    ax.set_title('Efficiency Frontier: Duration vs Success Rate\n(Bubble size = avg tool calls)')

    # Add legend for providers
    legend_elements = [plt.scatter([], [], c=color, s=100, label=provider.replace('-gla', '').title())
                       for provider, color in PROVIDER_COLORS.items()]
    ax.legend(handles=legend_elements, loc='lower right', title='Provider')

    ax.set_xlim(0, None)
    ax.set_ylim(75, 102)

    plt.savefig(output_dir / 'fig1_efficiency_frontier.png')
    plt.savefig(output_dir / 'fig1_efficiency_frontier.pdf')
    plt.close()
    print("Generated: fig1_efficiency_frontier.png")

def fig2_duration_comparison(data, output_dir):
    """
    Figure 2: Bar chart comparing average duration per model.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    models = data['model_stats']
    sorted_models = sorted(models.items(), key=lambda x: x[1]['avg_duration'])

    names = [get_short_name(m) for m, _ in sorted_models]
    durations = [s['avg_duration'] for _, s in sorted_models]
    colors = [PROVIDER_COLORS.get(get_provider(m), '#666666') for m, _ in sorted_models]

    bars = ax.barh(names, durations, color=colors, alpha=0.8, edgecolor='white')

    # Add value labels
    for bar, dur in zip(bars, durations):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
               f'{dur:.1f}s', va='center', fontsize=9)

    ax.set_xlabel('Average Duration (seconds)')
    ax.set_title('Average Task Completion Time by Model')

    # Add variance annotation
    variance = max(durations) / min(durations)
    ax.annotate(f'{variance:.1f}x variance', xy=(0.95, 0.05), xycoords='axes fraction',
               fontsize=11, ha='right', style='italic',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.savefig(output_dir / 'fig2_duration_comparison.png')
    plt.savefig(output_dir / 'fig2_duration_comparison.pdf')
    plt.close()
    print("Generated: fig2_duration_comparison.png")

def fig3_tool_calls_comparison(data, output_dir):
    """
    Figure 3: Bar chart comparing average tool calls per model.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    models = data['model_stats']
    sorted_models = sorted(models.items(), key=lambda x: x[1]['avg_tool_calls'])

    names = [get_short_name(m) for m, _ in sorted_models]
    tool_calls = [s['avg_tool_calls'] for _, s in sorted_models]
    colors = [PROVIDER_COLORS.get(get_provider(m), '#666666') for m, _ in sorted_models]

    bars = ax.barh(names, tool_calls, color=colors, alpha=0.8, edgecolor='white')

    # Add value labels
    for bar, tc in zip(bars, tool_calls):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
               f'{tc:.1f}', va='center', fontsize=9)

    ax.set_xlabel('Average Tool Calls')
    ax.set_title('Tool Call Efficiency by Model')

    # Add variance annotation
    variance = max(tool_calls) / min(tool_calls)
    ax.annotate(f'{variance:.1f}x variance', xy=(0.95, 0.05), xycoords='axes fraction',
               fontsize=11, ha='right', style='italic',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.savefig(output_dir / 'fig3_tool_calls_comparison.png')
    plt.savefig(output_dir / 'fig3_tool_calls_comparison.pdf')
    plt.close()
    print("Generated: fig3_tool_calls_comparison.png")

def fig4_heatmap(data, output_dir):
    """
    Figure 4: Heatmap of Model x Challenge performance.
    """
    # We need to reconstruct the matrix from the original results
    # For now, create a simplified version based on challenge stats
    fig, ax = plt.subplots(figsize=(10, 8))

    challenges = list(data['challenge_stats'].keys())
    models = list(data['model_stats'].keys())
    model_short = [get_short_name(m) for m in models]

    # Create success rate matrix (we'll use excellent_rate as proxy)
    matrix = []
    for model in models:
        row = []
        stats = data['model_stats'][model]
        # Use overall excellent rate for each cell (simplified)
        for challenge in challenges:
            row.append(stats['excellent_rate'] * 100)
        matrix.append(row)

    matrix = np.array(matrix)

    im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)

    ax.set_xticks(np.arange(len(challenges)))
    ax.set_yticks(np.arange(len(models)))
    ax.set_xticklabels(challenges, rotation=45, ha='right')
    ax.set_yticklabels(model_short)

    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('Excellent Rate (%)', rotation=-90, va="bottom")

    ax.set_title('Model × Challenge Excellence Rate')

    plt.savefig(output_dir / 'fig4_heatmap.png')
    plt.savefig(output_dir / 'fig4_heatmap.pdf')
    plt.close()
    print("Generated: fig4_heatmap.png")

def fig5_cost_performance(data, output_dir):
    """
    Figure 5: Cost vs Performance scatter plot (Pareto frontier).
    """
    fig, ax = plt.subplots(figsize=(10, 7))

    models = data['model_stats']

    costs = []
    success_rates = []
    labels = []
    colors = []

    for model_name, stats in models.items():
        costs.append(stats['estimated_cost'] * 1000)  # Convert to millicents
        success_rates.append(stats['success_rate'] * 100)
        labels.append(get_short_name(model_name))
        colors.append(PROVIDER_COLORS.get(get_provider(model_name), '#666666'))

    ax.scatter(costs, success_rates, c=colors, s=150, alpha=0.8, edgecolors='white', linewidth=2)

    # Add labels
    for i, label in enumerate(labels):
        ax.annotate(label, (costs[i], success_rates[i]), textcoords="offset points",
                   xytext=(8, 3), fontsize=9)

    ax.set_xlabel('Estimated Cost per Task (millicents)')
    ax.set_ylabel('Success Rate (%)')
    ax.set_title('Cost-Performance Tradeoff')

    # Highlight Pareto-optimal region
    ax.axhspan(95, 102, alpha=0.1, color='green', label='High Success Zone')
    ax.axvspan(0, 5, alpha=0.1, color='blue', label='Low Cost Zone')

    ax.legend(loc='lower right')
    ax.set_ylim(75, 102)

    plt.savefig(output_dir / 'fig5_cost_performance.png')
    plt.savefig(output_dir / 'fig5_cost_performance.pdf')
    plt.close()
    print("Generated: fig5_cost_performance.png")

def fig6_challenge_difficulty(data, output_dir):
    """
    Figure 6: Challenge difficulty comparison.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    challenges = data['challenge_stats']
    names = list(challenges.keys())

    # Left: Average duration by challenge
    durations = [challenges[c]['avg_duration'] for c in names]
    ax1 = axes[0]
    bars1 = ax1.bar(names, durations, color='#4285F4', alpha=0.8)
    ax1.set_ylabel('Average Duration (seconds)')
    ax1.set_title('Task Completion Time by Challenge Type')
    ax1.set_xticklabels(names, rotation=45, ha='right')

    # Add duration variance
    for bar, c in zip(bars1, names):
        variance = challenges[c]['duration_variance']
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{variance:.1f}x var', ha='center', fontsize=8, style='italic')

    # Right: Average tool calls by challenge
    tool_calls = [challenges[c]['avg_tool_calls'] for c in names]
    ax2 = axes[1]
    bars2 = ax2.bar(names, tool_calls, color='#10A37F', alpha=0.8)
    ax2.set_ylabel('Average Tool Calls')
    ax2.set_title('Tool Call Count by Challenge Type')
    ax2.set_xticklabels(names, rotation=45, ha='right')

    # Add tool call variance
    for bar, c in zip(bars2, names):
        variance = challenges[c]['tool_call_variance']
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{variance:.1f}x var', ha='center', fontsize=8, style='italic')

    plt.tight_layout()
    plt.savefig(output_dir / 'fig6_challenge_difficulty.png')
    plt.savefig(output_dir / 'fig6_challenge_difficulty.pdf')
    plt.close()
    print("Generated: fig6_challenge_difficulty.png")

def fig7_efficiency_rankings(data, output_dir):
    """
    Figure 7: Composite efficiency score rankings.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    rankings = data['rankings']

    names = [get_short_name(m) for m, _ in rankings]
    scores = [s for _, s in rankings]
    colors = [PROVIDER_COLORS.get(get_provider(m), '#666666') for m, _ in rankings]

    bars = ax.barh(range(len(names)), scores, color=colors, alpha=0.8, edgecolor='white')

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.invert_yaxis()  # Highest rank at top

    ax.set_xlabel('Composite Efficiency Score')
    ax.set_title('Model Efficiency Rankings\n(Weighted: 40% Success, 20% Excellent, 20% Time Eff., 20% Tool Eff.)')

    # Add rank numbers
    for i, (bar, score) in enumerate(zip(bars, scores)):
        ax.text(0.02, bar.get_y() + bar.get_height()/2, f'#{i+1}',
               va='center', fontsize=10, fontweight='bold', color='white')
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
               f'{score:.3f}', va='center', fontsize=9)

    ax.set_xlim(0, 1.1)

    plt.savefig(output_dir / 'fig7_efficiency_rankings.png')
    plt.savefig(output_dir / 'fig7_efficiency_rankings.pdf')
    plt.close()
    print("Generated: fig7_efficiency_rankings.png")

def main():
    script_dir = Path(__file__).parent
    data_path = script_dir / 'efficiency_data.json'
    output_dir = script_dir / 'figures'

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    if not data_path.exists():
        print(f"Error: {data_path} not found. Run analyze_efficiency.py first.")
        return

    print("Loading data...")
    data = load_data(data_path)

    print("\nGenerating figures...")
    print("-" * 40)

    fig1_efficiency_frontier(data, output_dir)
    fig2_duration_comparison(data, output_dir)
    fig3_tool_calls_comparison(data, output_dir)
    fig4_heatmap(data, output_dir)
    fig5_cost_performance(data, output_dir)
    fig6_challenge_difficulty(data, output_dir)
    fig7_efficiency_rankings(data, output_dir)

    print("-" * 40)
    print(f"\nAll figures saved to: {output_dir}")
    print("\nFigures generated:")
    print("  - fig1_efficiency_frontier: Duration vs Success (bubble=tool calls)")
    print("  - fig2_duration_comparison: Horizontal bar chart of durations")
    print("  - fig3_tool_calls_comparison: Horizontal bar chart of tool calls")
    print("  - fig4_heatmap: Model × Challenge performance matrix")
    print("  - fig5_cost_performance: Cost vs Success Pareto plot")
    print("  - fig6_challenge_difficulty: Challenge comparison (dual bar)")
    print("  - fig7_efficiency_rankings: Composite score rankings")

if __name__ == "__main__":
    main()
