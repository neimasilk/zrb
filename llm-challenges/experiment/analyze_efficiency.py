#!/usr/bin/env python3
"""
Efficiency Analysis Script for LLM Agent Benchmark
Generates insights for research paper with focus on efficiency metrics.
"""

import json
import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

# Estimated cost per 1M tokens (USD) - 2024 pricing
MODEL_PRICING = {
    "openai:gpt-4o": {"input": 2.50, "output": 10.00},
    "openai:gpt-5.1": {"input": 5.00, "output": 15.00},  # Estimated
    "openai:gpt-5.2": {"input": 5.00, "output": 15.00},  # Estimated
    "google-gla:gemini-2.5-flash": {"input": 0.075, "output": 0.30},
    "google-gla:gemini-2.5-pro": {"input": 1.25, "output": 5.00},
    "google-gla:gemini-3-flash-preview": {"input": 0.10, "output": 0.40},  # Estimated
    "google-gla:gemini-3-pro-preview": {"input": 1.50, "output": 6.00},  # Estimated
    "deepseek:deepseek-chat": {"input": 0.14, "output": 0.28},
    "ollama:glm-4.7:cloud": {"input": 0.50, "output": 1.00},  # Estimated
    "ollama:kimi-k2.5:cloud": {"input": 0.50, "output": 1.00},  # Estimated
    "ollama:qwen3-vl:235b-cloud": {"input": 1.00, "output": 2.00},  # Estimated
}

# Estimated tokens per tool call (rough approximation)
TOKENS_PER_TOOL_CALL = 500  # input + output combined


@dataclass
class ModelStats:
    model: str
    total_experiments: int
    excellent_count: int
    pass_count: int
    fail_count: int
    avg_duration: float
    avg_tool_calls: float
    total_tool_calls: int
    min_duration: float
    max_duration: float
    min_tool_calls: int
    max_tool_calls: int
    success_rate: float
    excellent_rate: float
    tool_efficiency_ratio: float  # success_rate / avg_tool_calls
    time_efficiency_ratio: float  # success_rate / avg_duration
    estimated_cost_per_task: float
    challenges_passed: List[str]
    challenges_failed: List[str]


def load_results(results_path: str) -> List[dict]:
    """Load results from JSON file."""
    with open(results_path, "r") as f:
        return json.load(f)


def calculate_model_stats(results: List[dict]) -> Dict[str, ModelStats]:
    """Calculate statistics per model."""
    model_data = defaultdict(list)

    for r in results:
        model_data[r["model"]].append(r)

    stats = {}
    for model, experiments in model_data.items():
        durations = [e["duration"] for e in experiments]
        tool_calls = [e["tool_call_count"] for e in experiments]

        excellent = sum(1 for e in experiments if e["status"] == "EXCELLENT")
        passed = sum(1 for e in experiments if e["status"] in ["PASS", "EXCELLENT"])
        failed = sum(1 for e in experiments if e["status"] not in ["PASS", "EXCELLENT"])

        total = len(experiments)
        avg_duration = sum(durations) / total
        avg_tools = sum(tool_calls) / total

        success_rate = passed / total if total > 0 else 0
        excellent_rate = excellent / total if total > 0 else 0

        # Efficiency ratios (higher is better)
        # Avoid division by zero
        ter = success_rate / avg_tools if avg_tools > 0 else 0
        time_er = success_rate / avg_duration if avg_duration > 0 else 0

        # Estimate cost (rough approximation based on tool calls)
        pricing = MODEL_PRICING.get(model, {"input": 1.0, "output": 2.0})
        estimated_tokens = avg_tools * TOKENS_PER_TOOL_CALL
        est_cost = (estimated_tokens / 1_000_000) * (pricing["input"] + pricing["output"]) / 2

        challenges_passed = [e["challenge_name"] for e in experiments if e["status"] in ["PASS", "EXCELLENT"]]
        challenges_failed = [e["challenge_name"] for e in experiments if e["status"] not in ["PASS", "EXCELLENT"]]

        stats[model] = ModelStats(
            model=model,
            total_experiments=total,
            excellent_count=excellent,
            pass_count=passed,
            fail_count=failed,
            avg_duration=avg_duration,
            avg_tool_calls=avg_tools,
            total_tool_calls=sum(tool_calls),
            min_duration=min(durations),
            max_duration=max(durations),
            min_tool_calls=min(tool_calls),
            max_tool_calls=max(tool_calls),
            success_rate=success_rate,
            excellent_rate=excellent_rate,
            tool_efficiency_ratio=ter,
            time_efficiency_ratio=time_er,
            estimated_cost_per_task=est_cost,
            challenges_passed=challenges_passed,
            challenges_failed=challenges_failed,
        )

    return stats


def calculate_challenge_stats(results: List[dict]) -> Dict[str, dict]:
    """Calculate statistics per challenge."""
    challenge_data = defaultdict(list)

    for r in results:
        challenge_data[r["challenge_name"]].append(r)

    stats = {}
    for challenge, experiments in challenge_data.items():
        durations = [e["duration"] for e in experiments]
        tool_calls = [e["tool_call_count"] for e in experiments]
        passed = sum(1 for e in experiments if e["status"] in ["PASS", "EXCELLENT"])
        excellent = sum(1 for e in experiments if e["status"] == "EXCELLENT")

        stats[challenge] = {
            "challenge": challenge,
            "total_models": len(experiments),
            "pass_count": passed,
            "excellent_count": excellent,
            "success_rate": passed / len(experiments),
            "avg_duration": sum(durations) / len(durations),
            "avg_tool_calls": sum(tool_calls) / len(tool_calls),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "duration_variance": max(durations) / min(durations) if min(durations) > 0 else 0,
            "tool_call_variance": max(tool_calls) / min(tool_calls) if min(tool_calls) > 0 else 0,
        }

    return stats


def find_anomalies(results: List[dict]) -> List[dict]:
    """Find anomalous results for deeper analysis."""
    anomalies = []

    # Calculate global averages
    all_tool_calls = [r["tool_call_count"] for r in results]
    all_durations = [r["duration"] for r in results]
    avg_tools = sum(all_tool_calls) / len(all_tool_calls)
    avg_duration = sum(all_durations) / len(all_durations)

    for r in results:
        reasons = []

        # Extremely high tool calls (>3x average)
        if r["tool_call_count"] > avg_tools * 3:
            reasons.append(f"High tool calls: {r['tool_call_count']} (avg: {avg_tools:.1f})")

        # Extremely long duration (>3x average)
        if r["duration"] > avg_duration * 3:
            reasons.append(f"Long duration: {r['duration']:.1f}s (avg: {avg_duration:.1f}s)")

        # Failed experiments
        if r["status"] not in ["PASS", "EXCELLENT"]:
            reasons.append(f"Failed with status: {r['status']}")

        # Malformed tool calls
        for tc in r.get("tool_calls", []):
            if len(tc) > 30 or tc.count("_") > 5:  # Likely concatenated
                reasons.append(f"Malformed tool call: {tc[:50]}...")
                break

        if reasons:
            anomalies.append({
                "model": r["model"],
                "challenge": r["challenge_name"],
                "status": r["status"],
                "duration": r["duration"],
                "tool_calls": r["tool_call_count"],
                "reasons": reasons,
                "log_path": r["log_path"],
            })

    return anomalies


def generate_efficiency_ranking(stats: Dict[str, ModelStats]) -> List[tuple]:
    """Generate efficiency ranking based on composite score."""
    rankings = []

    for model, s in stats.items():
        # Composite efficiency score (weighted)
        # Success is most important, then time efficiency, then tool efficiency
        composite = (
            s.success_rate * 0.4 +
            s.excellent_rate * 0.2 +
            min(s.time_efficiency_ratio * 100, 1.0) * 0.2 +  # Normalize
            min(s.tool_efficiency_ratio * 10, 1.0) * 0.2     # Normalize
        )
        rankings.append((model, composite, s))

    return sorted(rankings, key=lambda x: x[1], reverse=True)


def generate_report(results: List[dict], output_path: str):
    """Generate comprehensive analysis report."""
    model_stats = calculate_model_stats(results)
    challenge_stats = calculate_challenge_stats(results)
    anomalies = find_anomalies(results)
    rankings = generate_efficiency_ranking(model_stats)

    report = []
    report.append("# LLM Agent Efficiency Analysis Report\n")
    report.append("*Generated for research paper: Beyond Pass/Fail*\n\n")

    # Executive Summary
    report.append("## 1. Executive Summary\n\n")
    report.append(f"- **Total Experiments**: {len(results)}\n")
    report.append(f"- **Models Tested**: {len(model_stats)}\n")
    report.append(f"- **Challenges**: {len(challenge_stats)}\n")

    total_pass = sum(s.pass_count for s in model_stats.values())
    total_excellent = sum(s.excellent_count for s in model_stats.values())
    report.append(f"- **Overall Pass Rate**: {total_pass}/{len(results)} ({total_pass/len(results)*100:.1f}%)\n")
    report.append(f"- **Overall Excellent Rate**: {total_excellent}/{len(results)} ({total_excellent/len(results)*100:.1f}%)\n\n")

    # Key Findings
    report.append("## 2. Key Findings for Paper\n\n")

    # Speed variance
    durations = [s.avg_duration for s in model_stats.values()]
    speed_variance = max(durations) / min(durations) if min(durations) > 0 else 0
    report.append(f"### Finding 1: Speed Variance\n")
    report.append(f"- **{speed_variance:.1f}x** speed difference between fastest and slowest models\n")
    fastest = min(model_stats.values(), key=lambda x: x.avg_duration)
    slowest = max(model_stats.values(), key=lambda x: x.avg_duration)
    report.append(f"- Fastest: `{fastest.model}` ({fastest.avg_duration:.1f}s avg)\n")
    report.append(f"- Slowest: `{slowest.model}` ({slowest.avg_duration:.1f}s avg)\n\n")

    # Tool call variance
    tool_calls = [s.avg_tool_calls for s in model_stats.values()]
    tool_variance = max(tool_calls) / min(tool_calls) if min(tool_calls) > 0 else 0
    report.append(f"### Finding 2: Tool Call Variance\n")
    report.append(f"- **{tool_variance:.1f}x** difference in tool calls between most and least efficient\n")
    most_efficient = min(model_stats.values(), key=lambda x: x.avg_tool_calls)
    least_efficient = max(model_stats.values(), key=lambda x: x.avg_tool_calls)
    report.append(f"- Most efficient: `{most_efficient.model}` ({most_efficient.avg_tool_calls:.1f} avg calls)\n")
    report.append(f"- Least efficient: `{least_efficient.model}` ({least_efficient.avg_tool_calls:.1f} avg calls)\n\n")

    # Cost implications
    costs = [s.estimated_cost_per_task for s in model_stats.values()]
    cost_variance = max(costs) / min(costs) if min(costs) > 0 else 0
    report.append(f"### Finding 3: Estimated Cost Variance\n")
    report.append(f"- **{cost_variance:.1f}x** cost difference between cheapest and most expensive\n")
    cheapest = min(model_stats.values(), key=lambda x: x.estimated_cost_per_task)
    expensive = max(model_stats.values(), key=lambda x: x.estimated_cost_per_task)
    report.append(f"- Cheapest: `{cheapest.model}` (${cheapest.estimated_cost_per_task:.4f}/task)\n")
    report.append(f"- Most expensive: `{expensive.model}` (${expensive.estimated_cost_per_task:.4f}/task)\n\n")

    # Model Rankings
    report.append("## 3. Model Efficiency Rankings\n\n")
    report.append("| Rank | Model | Success Rate | Avg Duration (s) | Avg Tool Calls | Efficiency Score |\n")
    report.append("|------|-------|--------------|------------------|----------------|------------------|\n")
    for i, (model, score, s) in enumerate(rankings, 1):
        report.append(f"| {i} | {model} | {s.success_rate*100:.0f}% | {s.avg_duration:.1f} | {s.avg_tool_calls:.1f} | {score:.3f} |\n")
    report.append("\n")

    # Per-Model Detailed Stats
    report.append("## 4. Detailed Model Statistics\n\n")
    for model, s in sorted(model_stats.items()):
        report.append(f"### {model}\n")
        report.append(f"- Success Rate: {s.success_rate*100:.0f}% ({s.pass_count}/{s.total_experiments})\n")
        report.append(f"- Excellent Rate: {s.excellent_rate*100:.0f}% ({s.excellent_count}/{s.total_experiments})\n")
        report.append(f"- Duration: {s.avg_duration:.1f}s avg (range: {s.min_duration:.1f}-{s.max_duration:.1f}s)\n")
        report.append(f"- Tool Calls: {s.avg_tool_calls:.1f} avg (range: {s.min_tool_calls}-{s.max_tool_calls})\n")
        report.append(f"- Tool Efficiency Ratio: {s.tool_efficiency_ratio:.4f}\n")
        report.append(f"- Time Efficiency Ratio: {s.time_efficiency_ratio:.6f}\n")
        report.append(f"- Estimated Cost/Task: ${s.estimated_cost_per_task:.4f}\n")
        if s.challenges_failed:
            report.append(f"- Failed Challenges: {', '.join(s.challenges_failed)}\n")
        report.append("\n")

    # Challenge Analysis
    report.append("## 5. Challenge Difficulty Analysis\n\n")
    report.append("| Challenge | Success Rate | Avg Duration | Avg Tool Calls | Duration Variance | Tool Variance |\n")
    report.append("|-----------|--------------|--------------|----------------|-------------------|---------------|\n")
    for name, c in sorted(challenge_stats.items(), key=lambda x: x[1]["success_rate"], reverse=True):
        report.append(f"| {name} | {c['success_rate']*100:.0f}% | {c['avg_duration']:.1f}s | {c['avg_tool_calls']:.1f} | {c['duration_variance']:.1f}x | {c['tool_call_variance']:.1f}x |\n")
    report.append("\n")

    # Anomalies
    report.append("## 6. Anomalies for Investigation\n\n")
    if anomalies:
        for a in anomalies:
            report.append(f"### {a['model']} on {a['challenge']}\n")
            report.append(f"- Status: {a['status']}\n")
            report.append(f"- Duration: {a['duration']:.1f}s\n")
            report.append(f"- Tool Calls: {a['tool_calls']}\n")
            report.append(f"- Reasons:\n")
            for reason in a["reasons"]:
                report.append(f"  - {reason}\n")
            report.append(f"- Log: `{a['log_path']}`\n\n")
    else:
        report.append("No significant anomalies detected.\n\n")

    # Paper-Ready Statistics
    report.append("## 7. Paper-Ready Statistics\n\n")
    report.append("```\n")
    report.append("For copy-paste into paper:\n\n")
    report.append(f"Total experiments: {len(results)}\n")
    report.append(f"Models tested: {len(model_stats)}\n")
    report.append(f"Challenge types: {len(challenge_stats)}\n")
    report.append(f"Overall success rate: {total_pass/len(results)*100:.1f}%\n")
    report.append(f"Speed variance: {speed_variance:.1f}x\n")
    report.append(f"Tool efficiency variance: {tool_variance:.1f}x\n")
    report.append(f"Estimated cost variance: {cost_variance:.1f}x\n")
    report.append("```\n\n")

    # Export data for visualizations
    report.append("## 8. Data Export for Visualizations\n\n")
    report.append("JSON data exported to `efficiency_data.json` for creating figures.\n")

    # Write report
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(report))

    # Export data for visualizations
    viz_data = {
        "model_stats": {m: {
            "model": s.model,
            "success_rate": s.success_rate,
            "excellent_rate": s.excellent_rate,
            "avg_duration": s.avg_duration,
            "avg_tool_calls": s.avg_tool_calls,
            "tool_efficiency_ratio": s.tool_efficiency_ratio,
            "time_efficiency_ratio": s.time_efficiency_ratio,
            "estimated_cost": s.estimated_cost_per_task,
        } for m, s in model_stats.items()},
        "challenge_stats": challenge_stats,
        "rankings": [(m, score) for m, score, _ in rankings],
        "anomalies": anomalies,
    }

    viz_path = os.path.join(os.path.dirname(output_path), "efficiency_data.json")
    with open(viz_path, "w") as f:
        json.dump(viz_data, f, indent=2)

    return model_stats, challenge_stats, anomalies


def main():
    script_dir = Path(__file__).parent
    results_path = script_dir / "results.json"
    output_path = script_dir / "EFFICIENCY_ANALYSIS.md"

    if not results_path.exists():
        print(f"Error: {results_path} not found")
        return

    print("Loading results...")
    results = load_results(results_path)

    print(f"Analyzing {len(results)} experiments...")
    model_stats, challenge_stats, anomalies = generate_report(results, output_path)

    print(f"\nReport generated: {output_path}")
    print(f"Visualization data: {script_dir / 'efficiency_data.json'}")

    # Print quick summary
    print("\n" + "="*60)
    print("QUICK SUMMARY")
    print("="*60)

    rankings = generate_efficiency_ranking(model_stats)
    print("\nTop 5 Most Efficient Models:")
    for i, (model, score, s) in enumerate(rankings[:5], 1):
        print(f"  {i}. {model}: {s.success_rate*100:.0f}% success, {s.avg_duration:.1f}s avg, {s.avg_tool_calls:.1f} calls")

    print(f"\nAnomalies Found: {len(anomalies)}")
    for a in anomalies[:3]:
        print(f"  - {a['model']} on {a['challenge']}: {a['reasons'][0]}")


if __name__ == "__main__":
    main()
