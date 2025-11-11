from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import threading
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

print("Current working directory:", os.getcwd())

# 🏠 Optional root route (not used by GitHub Pages frontend)
@app.route('/', methods=['GET'])
def index():
    return "DoS Dashboard backend is running."
@app.route('/send_attack', methods=['POST'])
def send_attack():
    try:
        # You can customize count and delay here
        count = 50
        delay = 0.5

        def run_attack():
            subprocess.run(['python', 'client.py', str(count), str(delay)])

        threading.Thread(target=run_attack).start()
        return jsonify({"message": "Attack sent successfully!"})
    except Exception as e:
        print("Attack error:", e)
        return jsonify({"message": "Attack failed", "error": str(e)}), 500

# 🚀 Simulation trigger route
@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        rpm = int(request.form['rpm'])
        count = rpm
        delay = (60 / rpm) * 2

        # Clear alerts.txt before starting new simulation
        open(os.path.join(os.getcwd(), 'alerts.txt'), 'w').close()

        def run_client():
            subprocess.run(['python', 'client.py', str(count), str(delay)])

        threading.Thread(target=run_client).start()

        return jsonify({'status': 'ok'})
    except Exception as e:
        print("Simulation error:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 📊 Data route for graphs
@app.route('/data')
def get_data():
    try:
        with open(os.path.join(os.getcwd(), 'alerts.txt'), 'r') as f:
            lines = f.readlines()[-5:]  # Last 5 alerts
        timestamps = []
        counts = []
        for line in lines:
            if "ALERT" in line:
                parts = line.strip().split()
                timestamps.append(parts[0][1:] + " " + parts[1][:-1])  # Date + Time
                count = int(parts[-3].strip('()'))
                counts.append(count)
        return jsonify({'labels': timestamps, 'data': counts})
    except Exception as e:
        return jsonify({'labels': [], 'data': [], 'error': str(e)})

# 🛠️ Run the app locally (Render handles this automatically)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)