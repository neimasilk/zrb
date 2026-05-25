# Anomaly Deep-Dive Analysis

*Investigation of unusual patterns in LLM agent behavior*

## Executive Summary

- Total experiments analyzed: 55
- Anomalies detected: 6

## Anomaly 1: google-gla:gemini-3-flash-preview on bug-fix

### Basic Info
- **Status**: EXCELLENT
- **Duration**: 625.2s
- **Tool Calls**: 917
- **Reasons flagged**: Extreme tool calls: 917 (36.6x avg), Long duration: 625.2s (3.1x avg), Malformed tool: search_internetsearch_internetsearch_internet...

### Tool Usage Breakdown
- Unique tools used: 14
- Most used tools:
  - `run_shell_command`: 349 times (38.2%)
  - `read_file`: 164 times (18.0%)
  - `write_file`: 163 times (17.9%)
  - `replace_in_file`: 88 times (9.6%)
  - `list_files`: 54 times (5.9%)

### Repetition Patterns (Potential Loops)
- `run_shell_command` called 3x consecutively at position 4
- `run_shell_command` called 4x consecutively at position 15
- `replace_in_file` called 6x consecutively at position 34
- `run_shell_command` called 3x consecutively at position 42
- `replace_in_file` called 4x consecutively at position 69

### Malformed Tool Calls
These tool calls appear to be malformed (concatenated or invalid):
- `search_internetsearch_internetsearch_internet`
- `search_internetsearch_internetsearch_internet`
- `search_internetsearch_internetsearch_internet`
- `search_internetsearch_internetsearch_internet`
- `search_internetsearch_internetsearch_internet`

### Detected Loop Patterns
The agent appears to be stuck in these loops:
- Sequence (7 tools): run_shell_command → write_file → run_shell_command → read_file → search_internet → ...
  - Repeated ~6 times
- Sequence (6 tools): run_shell_command → run_shell_command → run_shell_command → run_shell_command → list_files → ...
  - Repeated ~5 times
- Sequence (6 tools): list_files → read_file → list_files → read_file → write_file → ...
  - Repeated ~7 times
- Sequence (6 tools): read_file → replace_in_file → run_shell_command → write_file → run_shell_command → ...
  - Repeated ~8 times
- Sequence (5 tools): write_file → run_shell_command → analyze_file → read_file → read_file
  - Repeated ~6 times

### Diagnosis
**Likely Cause**: Agent entered an infinite or near-infinite loop.
The agent repeatedly tried the same sequence of actions without recognizing failure.

**Evidence**:
- Found 5 consecutive repetition patterns
- Found 5 loop sequences
**Likely Cause**: Parallel/batched tool calls incorrectly serialized.
The model attempted to call multiple tools simultaneously but the framework concatenated them.


---

## Anomaly 2: deepseek:deepseek-chat on refactor

### Basic Info
- **Status**: EXCELLENT
- **Duration**: 750.8s
- **Tool Calls**: 49
- **Reasons flagged**: Long duration: 750.8s (3.7x avg)

### Tool Usage Breakdown
- Unique tools used: 5
- Most used tools:
  - `run_shell_command`: 19 times (38.8%)
  - `write_file`: 15 times (30.6%)
  - `read_file`: 7 times (14.3%)
  - `replace_in_file`: 7 times (14.3%)
  - `glob_files`: 1 times (2.0%)

### Repetition Patterns (Potential Loops)
- `write_file` called 6x consecutively at position 5
- `run_shell_command` called 3x consecutively at position 46

### Detected Loop Patterns
The agent appears to be stuck in these loops:
- Sequence (2 tools): run_shell_command → read_file
  - Repeated ~5 times
- Sequence (2 tools): replace_in_file → run_shell_command
  - Repeated ~5 times
- Sequence (2 tools): write_file → run_shell_command
  - Repeated ~8 times

### Diagnosis

---

## Anomaly 3: ollama:qwen3-vl:235b-cloud on refactor

### Basic Info
- **Status**: EXCELLENT
- **Duration**: 1046.1s
- **Tool Calls**: 12
- **Reasons flagged**: Long duration: 1046.1s (5.1x avg)

### Tool Usage Breakdown
- Unique tools used: 3
- Most used tools:
  - `read_file`: 5 times (41.7%)
  - `write_file`: 4 times (33.3%)
  - `run_shell_command`: 3 times (25.0%)

### Diagnosis

---

## Anomaly 4: ollama:qwen3-vl:235b-cloud on research

### Basic Info
- **Status**: EXCELLENT
- **Duration**: 849.9s
- **Tool Calls**: 6
- **Reasons flagged**: Long duration: 849.9s (4.2x avg)

### Tool Usage Breakdown
- Unique tools used: 3
- Most used tools:
  - `open_web_page`: 4 times (66.7%)
  - `search_internet`: 1 times (16.7%)
  - `write_file`: 1 times (16.7%)

### Repetition Patterns (Potential Loops)
- `open_web_page` called 4x consecutively at position 1

### Diagnosis

---

## Anomaly 5: ollama:kimi-k2.5:cloud on research

### Basic Info
- **Status**: EXECUTION_FAILED
- **Duration**: 34.3s
- **Tool Calls**: 3
- **Reasons flagged**: Failed: EXECUTION_FAILED, Malformed tool: search_internetsearch_internetsearch_internet...

### Tool Usage Breakdown
- Unique tools used: 1
- Most used tools:
  - `search_internetsearch_internetsearch_internet`: 3 times (100.0%)

### Repetition Patterns (Potential Loops)
- `search_internetsearch_internetsearch_internet` called 3x consecutively at position 0

### Malformed Tool Calls
These tool calls appear to be malformed (concatenated or invalid):
- `search_internetsearch_internetsearch_internet`
- `search_internetsearch_internetsearch_internet`
- `search_internetsearch_internetsearch_internet`

### Diagnosis
**Likely Cause**: Parallel/batched tool calls incorrectly serialized.
The model attempted to call multiple tools simultaneously but the framework concatenated them.

**Failure Analysis**: The agent did not complete the task successfully.
Verification output: `FAIL: solid_state_battery_report.md not found
VERIFICATION_RESULT: FAIL

`

---

## Anomaly 6: ollama:qwen3-vl:235b-cloud on bug-fix

### Basic Info
- **Status**: EXCELLENT
- **Duration**: 653.4s
- **Tool Calls**: 3
- **Reasons flagged**: Long duration: 653.4s (3.2x avg)

### Tool Usage Breakdown
- Unique tools used: 3
- Most used tools:
  - `glob_files`: 1 times (33.3%)
  - `read_file`: 1 times (33.3%)
  - `run_shell_command`: 1 times (33.3%)

### Diagnosis

---

## Recommendations for Paper

### Key Findings to Highlight:

1. **Loop Detection**: Some models (especially gemini-3-flash-preview) exhibit pathological looping behavior where they repeat the same sequence of actions hundreds of times before eventually succeeding.

2. **Malformed Tool Calls**: The kimi-k2.5 model shows evidence of attempting parallel tool calls that were incorrectly serialized, suggesting framework incompatibility with certain model output formats.

3. **Success Despite Inefficiency**: Notably, gemini-3-flash-preview achieved EXCELLENT status despite 917 tool calls, suggesting the verification criteria may need efficiency thresholds.

### Implications:

- **Efficiency ≠ Accuracy**: High accuracy doesn't imply efficient problem-solving
- **Cost Implications**: A 100x increase in tool calls translates to ~100x cost increase
- **Framework Design**: Agent frameworks need loop detection and early termination
