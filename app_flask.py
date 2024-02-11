from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from Main.System import System
from Main.Simulation import initialize, simulate
import threading
port_id = 5000
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # It's important to set a secret key for session management
socketio = SocketIO(app, cors_allowed_origins="*")

system = None  # Global system variable to manage the simulation state

@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    global system
    if system is None or system.is_stop:
        system = initialize()
        system.is_stop = False

        def simulate_and_emit():
            simulate(system.individuals, system)
            socketio.emit('simulation_update', {'data': 'Simulation completed or updated'})

        thread = threading.Thread(target=simulate_and_emit)
        thread.start()
        return jsonify({"message": "Simulation started"}), 200
    else:
        return jsonify({"message": "Simulation is already running"}), 200

@app.route('/stop_simulation', methods=['POST'])
def stop_simulation():
    global system
    if system and not system.is_stop:
        system.is_stop = True
        socketio.emit('simulation_update', {'data': 'Simulation stopped'})
        return jsonify({"message": "Simulation stopped"}), 200
    else:
        return jsonify({"message": "Simulation is not running or already stopped"}), 200

# SocketIO events
@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=port_id)
