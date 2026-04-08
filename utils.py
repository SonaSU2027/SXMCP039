def print_comparison(baseline, mcp, token_red, latency_red, density_gain):
    print("\n===== PERFORMANCE ANALYTICS =====")

    # 1. Token Metrics
    print(f"Baseline Tokens: {baseline['tokens']}")
    print(f"MCP Tokens: {mcp['tokens']}")
    print(f"Token Efficiency Gain: +{token_red:.2f}% \n")

    # 2. Latency Metrics
    print(f"Baseline Latency: {baseline['latency']:.6f}s")
    print(f"MCP Latency: {mcp['latency']:.6f}s")
    print(f"Latency Improvement: {latency_red:.2f}% \n")

    # 3. NOVELTY METRIC: Information Density
    # This is what sets your project apart!
    print(f"--- NOVELTY: INFORMATION DENSITY ---")
    print(f"Information Density Gain: +{density_gain:.2f}%")
    print("Interpretation: MCP provides higher technical signal per token.\n")

    # 4. Success Status
    print(f"Baseline Success: {baseline['success']}")
    print(f"MCP Success: {mcp['success']}\n")

    # 5. Blackboard State
    print("===== MCP SYSTEM STATE (BLACKBOARD) =====")
    print(f"System Logs: {mcp['progress']}") 
    print(f"Final Status: {'COMPLETED' if mcp['success'] else 'FAILED'}")