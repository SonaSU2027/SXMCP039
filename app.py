from flask import Flask, render_template, request, jsonify
import json
from mcp_system import run_mcp
from baseline import run_baseline
from metrics import calculate_improvement, calculate_density
from blackboard import init_db, get_full_state
from config import TASK

app = Flask(__name__)

# Initialize the SQLite Bus on startup
init_db()

@app.route('/')
def index():
    return render_template('index.html', default_task=TASK['description'])

@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.json
    task_desc = data.get('task', TASK['description'])
    task_obj = {"task_id": "UI_RUN", "description": task_desc}

    # 1. Run both systems
    baseline_result = run_baseline(task_obj)
    mcp_result = run_mcp(task_obj)

    # 2. Calculate Novelty Metrics
    base_den = calculate_density(baseline_result)
    mcp_den = calculate_density(mcp_result)
    density_gain = ((mcp_den - base_den) / base_den * 100) if base_den > 0 else 0
    
    token_red = calculate_improvement(baseline_result["tokens"], mcp_result["tokens"])
    latency_red = calculate_improvement(baseline_result["latency"], mcp_result["latency"])

    # 3. Get the latest blackboard state
    bus_state = get_full_state("UI_RUN")

    return jsonify({
        "baseline": baseline_result,
        "mcp": mcp_result,
        "metrics": {
            "token_reduction": token_red,
            "latency_improvement": latency_red,
            "density_gain": density_gain
        },
        "bus_history": bus_state['history']
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)