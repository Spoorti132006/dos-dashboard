from flask import Flask, render_template, request, jsonify
import subprocess
import threading

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rpm = int(request.form['rpm'])
        print("Form submitted")
        print("RPM value:", rpm)
        count = rpm
        delay = 60 / rpm

        def run_client():
            print(f"Running client.py with count={count}, delay={delay}")
            subprocess.run(['python', '../client.py', str(count), str(delay)])

        threading.Thread(target=run_client).start()

    return render_template('index.html')

@app.route('/data')
def get_data():
    try:
        with open('../alerts.txt', 'r') as f:
            lines = f.readlines()[-10:]  # Last 10 alerts
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

if __name__ == '__main__':
    app.run(debug=True)