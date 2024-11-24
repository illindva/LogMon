import os
from flask import Flask, render_template, jsonify, request
from generateLog import start_log_generator

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
filename = 'your_log_file.log'
app = Flask(__name__)

last_position = 0  # To keep track of the last read position


def read_log_file(log_file_full_path, position=0):
    """Reads new lines from log file starting from the given position."""
    global last_position
    with open(log_file_full_path, 'r') as f:
        f.seek(position)
        new_data = f.readlines()
        last_position = f.tell()
        return new_data, last_position


@app.route('/')
def index():
    log_file_full_path = os.path.join(BASE_DIR, 'logs', filename)
    initial_log_lines, current_pos = read_log_file(log_file_full_path)
    initial_log_lines.reverse()  # Reverse the log lines
    return render_template('index.html', log_lines=initial_log_lines)


@app.route('/update_log', methods=['GET'])
def update_log():
    log_file_full_path = os.path.join(BASE_DIR, 'logs', filename)
    new_lines, _ = read_log_file(log_file_full_path, position=last_position)
    new_lines.reverse()  # Reverse the log lines before sending to the client
    return jsonify(new_lines)


@app.route('/clear_log', methods=['POST'])
def clear_log():
    log_file_full_path = os.path.join(BASE_DIR, 'logs', filename)
    with open(log_file_full_path, 'w') as f:
        f.truncate(0)
    global last_position
    last_position = 0  # Reset the position tracker
    return jsonify({"status": "ok"})


@app.route('/export_log', methods=['GET'])
def export_log():
    log_file_full_path = os.path.join(BASE_DIR, 'logs', filename)
    with open(log_file_full_path, 'r') as f:
        log_content = f.read()
    export_path = os.path.join(BASE_DIR, 'logs', 'exported_log.txt')
    with open(export_path, 'w') as f:
        f.write(log_content)
    return jsonify({"export_path": export_path})


if __name__ == '__main__':
    start_log_generator()
    app.run(debug=True)
