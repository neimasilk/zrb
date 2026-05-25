# LLM Agent Efficiency Analysis Report
*Generated for research paper: Beyond Pass/Fail*

## 1. Executive Summary

- **Total Experiments**: 55
- **Models Tested**: 11
- **Challenges**: 5
- **Overall Pass Rate**: 54/55 (98.2%)
- **Overall Excellent Rate**: 46/55 (83.6%)

## 2. Key Findings for Paper

### Finding 1: Speed Variance
- **22.2x** speed difference between fastest and slowest models
- Fastest: `openai:gpt-4o` (33.0s avg)
- Slowest: `ollama:qwen3-vl:235b-cloud` (732.1s avg)

### Finding 2: Tool Call Variance
- **49.5x** difference in tool calls between most and least efficient
- Most efficient: `openai:gpt-5.1` (3.8 avg calls)
- Least efficient: `google-gla:gemini-3-flash-preview` (188.0 avg calls)

### Finding 3: Estimated Cost Variance
- **53.3x** cost difference between cheapest and most expensive
- Cheapest: `google-gla:gemini-2.5-flash` ($0.0007/task)
- Most expensive: `openai:gpt-5.2` ($0.0350/task)

## 3. Model Efficiency Rankings

| Rank | Model | Success Rate | Avg Duration (s) | Avg Tool Calls | Efficiency Score |
|------|-------|--------------|------------------|----------------|------------------|
| 1 | openai:gpt-5.1 | 100% | 44.2 | 3.8 | 1.000 |
| 2 | google-gla:gemini-3-pro-preview | 100% | 107.3 | 10.4 | 0.979 |
| 3 | openai:gpt-4o | 100% | 33.0 | 4.0 | 0.960 |
| 4 | openai:gpt-5.2 | 100% | 85.2 | 7.0 | 0.960 |
| 5 | google-gla:gemini-2.5-flash | 100% | 51.0 | 7.0 | 0.920 |
| 6 | ollama:glm-4.7:cloud | 100% | 355.1 | 7.0 | 0.856 |
| 7 | google-gla:gemini-2.5-pro | 100% | 121.7 | 15.8 | 0.811 |
| 8 | ollama:qwen3-vl:235b-cloud | 100% | 732.1 | 5.4 | 0.787 |
| 9 | deepseek:deepseek-chat | 100% | 306.3 | 20.0 | 0.765 |
| 10 | ollama:kimi-k2.5:cloud | 80% | 245.7 | 7.4 | 0.745 |
| 11 | google-gla:gemini-3-flash-preview | 100% | 155.3 | 188.0 | 0.699 |

## 4. Detailed Model Statistics

### deepseek:deepseek-chat
- Success Rate: 100% (5/5)
- Excellent Rate: 100% (5/5)
- Duration: 306.3s avg (range: 78.3-750.8s)
- Tool Calls: 20.0 avg (range: 5-49)
- Tool Efficiency Ratio: 0.0500
- Time Efficiency Ratio: 0.003265
- Estimated Cost/Task: $0.0021

### google-gla:gemini-2.5-flash
- Success Rate: 100% (5/5)
- Excellent Rate: 60% (3/5)
- Duration: 51.0s avg (range: 11.6-174.9s)
- Tool Calls: 7.0 avg (range: 1-24)
- Tool Efficiency Ratio: 0.1429
- Time Efficiency Ratio: 0.019613
- Estimated Cost/Task: $0.0007

### google-gla:gemini-2.5-pro
- Success Rate: 100% (5/5)
- Excellent Rate: 60% (3/5)
- Duration: 121.7s avg (range: 23.7-378.4s)
- Tool Calls: 15.8 avg (range: 3-53)
- Tool Efficiency Ratio: 0.0633
- Time Efficiency Ratio: 0.008220
- Estimated Cost/Task: $0.0247

### google-gla:gemini-3-flash-preview
- Success Rate: 100% (5/5)
- Excellent Rate: 80% (4/5)
- Duration: 155.3s avg (range: 22.0-625.2s)
- Tool Calls: 188.0 avg (range: 3-917)
- Tool Efficiency Ratio: 0.0053
- Time Efficiency Ratio: 0.006440
- Estimated Cost/Task: $0.0235

### google-gla:gemini-3-pro-preview
- Success Rate: 100% (5/5)
- Excellent Rate: 100% (5/5)
- Duration: 107.3s avg (range: 27.6-330.6s)
- Tool Calls: 10.4 avg (range: 2-31)
- Tool Efficiency Ratio: 0.0962
- Time Efficiency Ratio: 0.009323
- Estimated Cost/Task: $0.0195

### ollama:glm-4.7:cloud
- Success Rate: 100% (5/5)
- Excellent Rate: 100% (5/5)
- Duration: 355.1s avg (range: 181.3-601.4s)
- Tool Calls: 7.0 avg (range: 1-11)
- Tool Efficiency Ratio: 0.1429
- Time Efficiency Ratio: 0.002816
- Estimated Cost/Task: $0.0026

### ollama:kimi-k2.5:cloud
- Success Rate: 80% (4/5)
- Excellent Rate: 80% (4/5)
- Duration: 245.7s avg (range: 34.3-484.8s)
- Tool Calls: 7.4 avg (range: 2-20)
- Tool Efficiency Ratio: 0.1081
- Time Efficiency Ratio: 0.003257
- Estimated Cost/Task: $0.0028
- Failed Challenges: research

### ollama:qwen3-vl:235b-cloud
- Success Rate: 100% (5/5)
- Excellent Rate: 80% (4/5)
- Duration: 732.1s avg (range: 550.5-1046.1s)
- Tool Calls: 5.4 avg (range: 3-12)
- Tool Efficiency Ratio: 0.1852
- Time Efficiency Ratio: 0.001366
- Estimated Cost/Task: $0.0040

### openai:gpt-4o
- Success Rate: 100% (5/5)
- Excellent Rate: 80% (4/5)
- Duration: 33.0s avg (range: 14.6-56.4s)
- Tool Calls: 4.0 avg (range: 1-7)
- Tool Efficiency Ratio: 0.2500
- Time Efficiency Ratio: 0.030347
- Estimated Cost/Task: $0.0125

### openai:gpt-5.1
- Success Rate: 100% (5/5)
- Excellent Rate: 100% (5/5)
- Duration: 44.2s avg (range: 18.8-87.6s)
- Tool Calls: 3.8 avg (range: 1-6)
- Tool Efficiency Ratio: 0.2632
- Time Efficiency Ratio: 0.022607
- Estimated Cost/Task: $0.0190

### openai:gpt-5.2
- Success Rate: 100% (5/5)
- Excellent Rate: 80% (4/5)
- Duration: 85.2s avg (range: 27.1-294.3s)
- Tool Calls: 7.0 avg (range: 1-17)
- Tool Efficiency Ratio: 0.1429
- Time Efficiency Ratio: 0.011738
- Estimated Cost/Task: $0.0350

## 5. Challenge Difficulty Analysis

| Challenge | Success Rate | Avg Duration | Avg Tool Calls | Duration Variance | Tool Variance |
|-----------|--------------|--------------|----------------|-------------------|---------------|
| bug-fix | 100% | 310.3s | 97.6 | 34.8x | 305.7x |
| copywriting | 100% | 118.4s | 2.1 | 47.3x | 5.0x |
| feature | 100% | 148.6s | 7.2 | 21.2x | 8.0x |
| refactor | 100% | 258.0s | 11.7 | 41.3x | 12.2x |
| research | 91% | 181.4s | 6.7 | 44.9x | 8.5x |

## 6. Anomalies for Investigation

### deepseek:deepseek-chat on refactor
- Status: EXCELLENT
- Duration: 750.8s
- Tool Calls: 49
- Reasons:
  - Long duration: 750.8s (avg: 203.3s)
- Log: `experiment/deepseek:deepseek-chat/refactor/combined.log`

### google-gla:gemini-3-flash-preview on bug-fix
- Status: EXCELLENT
- Duration: 625.2s
- Tool Calls: 917
- Reasons:
  - High tool calls: 917 (avg: 25.1)
  - Long duration: 625.2s (avg: 203.3s)
  - Malformed tool call: search_internetsearch_internetsearch_internet...
- Log: `experiment/google-gla:gemini-3-flash-preview/bug-fix/combined.log`

### ollama:kimi-k2.5:cloud on research
- Status: EXECUTION_FAILED
- Duration: 34.3s
- Tool Calls: 3
- Reasons:
  - Failed with status: EXECUTION_FAILED
  - Malformed tool call: search_internetsearch_internetsearch_internet...
- Log: `experiment/ollama:kimi-k2.5:cloud/research/combined.log`

### ollama:qwen3-vl:235b-cloud on bug-fix
- Status: EXCELLENT
- Duration: 653.4s
- Tool Calls: 3
- Reasons:
  - Long duration: 653.4s (avg: 203.3s)
- Log: `experiment/ollama:qwen3-vl:235b-cloud/bug-fix/combined.log`

### ollama:qwen3-vl:235b-cloud on refactor
- Status: EXCELLENT
- Duration: 1046.1s
- Tool Calls: 12
- Reasons:
  - Long duration: 1046.1s (avg: 203.3s)
- Log: `experiment/ollama:qwen3-vl:235b-cloud/refactor/combined.log`

### ollama:qwen3-vl:235b-cloud on research
- Status: EXCELLENT
- Duration: 849.9s
- Tool Calls: 6
- Reasons:
  - Long duration: 849.9s (avg: 203.3s)
- Log: `experiment/ollama:qwen3-vl:235b-cloud/research/combined.log`

## 7. Paper-Ready Statistics

```
For copy-paste into paper:

Total experiments: 55
Models tested: 11
Challenge types: 5
Overall success rate: 98.2%
Speed variance: 22.2x
Tool efficiency variance: 49.5x
Estimated cost variance: 53.3x
```

## 8. Data Export for Visualizations

JSON data exported to `efficiency_data.json` for creating figures.
