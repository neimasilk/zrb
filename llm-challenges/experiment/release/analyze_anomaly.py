#!/usr/bin/env python3
"""
Deep analysis of anomalous experiments, particularly:
1. gemini-3-flash-preview with 917 tool calls on bug-fix
2. kimi-k2.5 failure on research (malformed tool calls)
"""

import json
from collections import Counter
from pathlib import Path


def analyze_tool_call_patterns(tool_calls: list) -> dict:
    """Analyze patterns in tool call sequence."""
    if not tool_calls:
        return {"error": "No tool calls"}

    # Count tool usage
    tool_counts = Counter(tool_calls)

    # Detect repetition patterns
    repetitions = []
    i = 0
    while i < len(tool_calls) - 1:
        # Check for immediate repetition
        if tool_calls[i] == tool_calls[i + 1]:
            count = 1
            while i + count < len(tool_calls) and tool_calls[i] == tool_calls[i + count]:
                count += 1
            if count >= 3:  # 3+ consecutive same calls
                repetitions.append({
                    "tool": tool_calls[i],
                    "count": count,
                    "position": i
                })
            i += count
        else:
            i += 1

    # Detect malformed tool names
    malformed = [tc for tc in tool_calls if len(tc) > 25 or tc.count('_') > 4]

    # Detect loops (repeated sequences)
    # Look for patterns like [A, B, C, A, B, C, A, B, C]
    sequence_str = '|'.join(tool_calls)
    loops_found = []

    for seq_len in range(2, 10):  # Check sequences of length 2-10
        for start in range(len(tool_calls) - seq_len * 2):
            seq = tool_calls[start:start + seq_len]
            seq_str = '|'.join(seq)
            # Count occurrences
            count = sequence_str.count(seq_str)
            if count >= 5:  # Repeated 5+ times
                loops_found.append({
                    "sequence": seq,
                    "length": seq_len,
                    "occurrences": count
                })

    # Deduplicate loops (keep longest)
    unique_loops = []
    for loop in sorted(loops_found, key=lambda x: -x['length']):
        is_subset = False
        for existing in unique_loops:
            if set(loop['sequence']).issubset(set(existing['sequence'])):
                is_subset = True
                break
        if not is_subset:
            unique_loops.append(loop)

    return {
        "total_calls": len(tool_calls),
        "unique_tools": len(tool_counts),
        "tool_counts": dict(tool_counts.most_common(10)),
        "repetitions": repetitions[:5],  # Top 5
        "malformed_calls": malformed[:10],  # First 10
        "detected_loops": unique_loops[:5],  # Top 5
    }


def analyze_experiment(result: dict) -> dict:
    """Analyze a single experiment result."""
    analysis = {
        "model": result["model"],
        "challenge": result["challenge_name"],
        "status": result["status"],
        "duration": result["duration"],
        "tool_call_count": result["tool_call_count"],
    }

    if result.get("tool_calls"):
        analysis["pattern_analysis"] = analyze_tool_call_patterns(result["tool_calls"])

    return analysis


def find_anomalies(results: list) -> list:
    """Find anomalous experiments."""
    # Calculate thresholds
    tool_counts = [r["tool_call_count"] for r in results]
    durations = [r["duration"] for r in results]

    avg_tools = sum(tool_counts) / len(tool_counts)
    avg_duration = sum(durations) / len(durations)

    anomalies = []
    for r in results:
        reasons = []

        # High tool calls (>5x average)
        if r["tool_call_count"] > avg_tools * 5:
            reasons.append(f"Extreme tool calls: {r['tool_call_count']} ({r['tool_call_count']/avg_tools:.1f}x avg)")

        # Very long duration (>3x average)
        if r["duration"] > avg_duration * 3:
            reasons.append(f"Long duration: {r['duration']:.1f}s ({r['duration']/avg_duration:.1f}x avg)")

        # Failed
        if r["status"] not in ["PASS", "EXCELLENT"]:
            reasons.append(f"Failed: {r['status']}")

        # Malformed tool calls
        for tc in r.get("tool_calls", []):
            if len(tc) > 30:
                reasons.append(f"Malformed tool: {tc[:50]}...")
                break

        if reasons:
            anomalies.append({
                "result": r,
                "reasons": reasons
            })

    return anomalies


def generate_anomaly_report(results: list, output_path: str):
    """Generate detailed anomaly analysis report."""
    anomalies = find_anomalies(results)

    report = []
    report.append("# Anomaly Deep-Dive Analysis\n\n")
    report.append("*Investigation of unusual patterns in LLM agent behavior*\n\n")

    report.append("## Executive Summary\n\n")
    report.append(f"- Total experiments analyzed: {len(results)}\n")
    report.append(f"- Anomalies detected: {len(anomalies)}\n\n")

    # Sort by severity (tool calls)
    anomalies.sort(key=lambda x: x['result']['tool_call_count'], reverse=True)

    for i, anomaly in enumerate(anomalies, 1):
        r = anomaly['result']
        report.append(f"## Anomaly {i}: {r['model']} on {r['challenge_name']}\n\n")

        report.append("### Basic Info\n")
        report.append(f"- **Status**: {r['status']}\n")
        report.append(f"- **Duration**: {r['duration']:.1f}s\n")
        report.append(f"- **Tool Calls**: {r['tool_call_count']}\n")
        report.append(f"- **Reasons flagged**: {', '.join(anomaly['reasons'])}\n\n")

        # Pattern analysis
        analysis = analyze_experiment(r)
        if 'pattern_analysis' in analysis:
            pa = analysis['pattern_analysis']

            report.append("### Tool Usage Breakdown\n")
            report.append(f"- Unique tools used: {pa['unique_tools']}\n")
            report.append("- Most used tools:\n")
            for tool, count in list(pa['tool_counts'].items())[:5]:
                pct = count / pa['total_calls'] * 100
                report.append(f"  - `{tool}`: {count} times ({pct:.1f}%)\n")
            report.append("\n")

            if pa['repetitions']:
                report.append("### Repetition Patterns (Potential Loops)\n")
                for rep in pa['repetitions']:
                    report.append(f"- `{rep['tool']}` called {rep['count']}x consecutively at position {rep['position']}\n")
                report.append("\n")

            if pa['malformed_calls']:
                report.append("### Malformed Tool Calls\n")
                report.append("These tool calls appear to be malformed (concatenated or invalid):\n")
                for mc in pa['malformed_calls'][:5]:
                    report.append(f"- `{mc[:60]}{'...' if len(mc) > 60 else ''}`\n")
                report.append("\n")

            if pa['detected_loops']:
                report.append("### Detected Loop Patterns\n")
                report.append("The agent appears to be stuck in these loops:\n")
                for loop in pa['detected_loops']:
                    seq_str = " → ".join(loop['sequence'][:5])
                    if len(loop['sequence']) > 5:
                        seq_str += " → ..."
                    report.append(f"- Sequence ({loop['length']} tools): {seq_str}\n")
                    report.append(f"  - Repeated ~{loop['occurrences']} times\n")
                report.append("\n")

        # Diagnosis
        report.append("### Diagnosis\n")

        if r['tool_call_count'] > 100:
            report.append("**Likely Cause**: Agent entered an infinite or near-infinite loop.\n")
            report.append("The agent repeatedly tried the same sequence of actions without recognizing failure.\n\n")
            report.append("**Evidence**:\n")
            if pa.get('repetitions'):
                report.append(f"- Found {len(pa['repetitions'])} consecutive repetition patterns\n")
            if pa.get('detected_loops'):
                report.append(f"- Found {len(pa['detected_loops'])} loop sequences\n")

        if any('malformed' in r.lower() for r in anomaly['reasons']):
            report.append("**Likely Cause**: Parallel/batched tool calls incorrectly serialized.\n")
            report.append("The model attempted to call multiple tools simultaneously but the framework concatenated them.\n\n")

        if r['status'] not in ['PASS', 'EXCELLENT']:
            report.append("**Failure Analysis**: The agent did not complete the task successfully.\n")
            if 'verification_output' in r and r['verification_output']:
                report.append(f"Verification output: `{r['verification_output'][:200]}`\n")

        report.append("\n---\n\n")

    # Recommendations
    report.append("## Recommendations for Paper\n\n")
    report.append("### Key Findings to Highlight:\n\n")
    report.append("1. **Loop Detection**: Some models (especially gemini-3-flash-preview) exhibit ")
    report.append("pathological looping behavior where they repeat the same sequence of actions ")
    report.append("hundreds of times before eventually succeeding.\n\n")
    report.append("2. **Malformed Tool Calls**: The kimi-k2.5 model shows evidence of attempting ")
    report.append("parallel tool calls that were incorrectly serialized, suggesting framework ")
    report.append("incompatibility with certain model output formats.\n\n")
    report.append("3. **Success Despite Inefficiency**: Notably, gemini-3-flash-preview achieved ")
    report.append("EXCELLENT status despite 917 tool calls, suggesting the verification criteria ")
    report.append("may need efficiency thresholds.\n\n")

    report.append("### Implications:\n\n")
    report.append("- **Efficiency ≠ Accuracy**: High accuracy doesn't imply efficient problem-solving\n")
    report.append("- **Cost Implications**: A 100x increase in tool calls translates to ~100x cost increase\n")
    report.append("- **Framework Design**: Agent frameworks need loop detection and early termination\n")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(report))

    return anomalies


def main():
    script_dir = Path(__file__).parent
    results_path = script_dir / "results.json"
    output_path = script_dir / "ANOMALY_ANALYSIS.md"

    print("Loading results...")
    with open(results_path, 'r') as f:
        results = json.load(f)

    print(f"Analyzing {len(results)} experiments for anomalies...")
    anomalies = generate_anomaly_report(results, output_path)

    print(f"\nFound {len(anomalies)} anomalies")
    print(f"Report saved to: {output_path}")

    # Print summary
    print("\n" + "="*60)
    print("ANOMALY SUMMARY")
    print("="*60)

    for i, a in enumerate(anomalies[:5], 1):
        r = a['result']
        print(f"\n{i}. {r['model']} on {r['challenge_name']}")
        print(f"   Status: {r['status']}, Tools: {r['tool_call_count']}, Duration: {r['duration']:.1f}s")
        for reason in a['reasons']:
            print(f"   → {reason}")


if __name__ == "__main__":
    main()
