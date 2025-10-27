from flask import Flask, render_template_string, jsonify
import time

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DoS Alert Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 20px; }
        h1 { color: #333; }
        canvas { background: #fff; padding: 10px; border: 1px solid #ccc; }
        .refresh { margin-top: 10px; }
    </style>
</head>
<body>
    <h1>🚨 DoS Alert Dashboard</h1>
    <canvas id="alertChart" width="600" height="300"></canvas>
    <script>
        async function loadChart() {
            const res = await fetch('/chart-data');
            const data = await res.json();
            const ctx = document.getElementById('alertChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Alerts per Minute',
                        data: data.values,
                        borderColor: 'red',
                        backgroundColor: 'rgba(255,0,0,0.2)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    scales: {
                        x: { title: { display: true, text: 'Time' }},
                        y: { title: { display: true, text: 'Alert Count' }, beginAtZero: true }
                    }
                }
            });
        }
        loadChart();
    </script>
    <form method="get">
        <button class="refresh">🔄 Refresh</button>
    </form>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chart-data')
def chart_data():
    try:
        with open("alerts.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return jsonify({'labels': [], 'values': []})

    timestamps = []
    for line in lines:
        if line.startswith("["):
            ts = line.split("]")[0][1:]
            timestamps.append(ts)

    counts = {}
    for ts in timestamps:
        minute = ts[:16]  # "YYYY-MM-DD HH:MM"
        counts[minute] = counts.get(minute, 0) + 1

    sorted_data = sorted(counts.items())
    labels = [item[0] for item in sorted_data]
    values = [item[1] for item in sorted_data]

    return jsonify({'labels': labels, 'values': values})

if __name__ == '__main__':
    app.run(debug=True)