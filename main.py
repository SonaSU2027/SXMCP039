from config import TASK
from baseline import run_baseline
from mcp_system import run_mcp
from metrics import calculate_improvement, calculate_density
from utils import print_comparison
from blackboard import init_db

def main():
    init_db()  

    print("\n Running Baseline System...")
    baseline_result = run_baseline(TASK)

    print(" Running MCP Blackboard System...")
    mcp_result = run_mcp(TASK)

    # --- CHANGE 2: NOVELTY CALCULATION (ROBUST) ---
    # Calculate how much 'signal' (useful text) we get per token
    baseline_den = calculate_density(baseline_result)
    mcp_den = calculate_density(mcp_result)
    
    # Calculate the percentage increase in information density
    # Added a guardrail to prevent ZeroDivisionError if the baseline failed
    if baseline_den > 0:
        density_gain = ((mcp_den - baseline_den) / baseline_den) * 100
    else:
        # If baseline density is 0 (API error), we assign 100% gain if MCP succeeded, 
        # or 0% if both failed.
        density_gain = 100.0 if mcp_den > 0 else 0.0
    # -----------------------------------------------

    token_reduction = calculate_improvement(
        baseline_result["tokens"], mcp_result["tokens"]
    )

    latency_reduction = calculate_improvement(
        baseline_result["latency"], mcp_result["latency"]
    )

    print_comparison(
        baseline_result,
        mcp_result,
        token_reduction,
        latency_reduction,
        density_gain
    )
    
if __name__ == "__main__":
    main()