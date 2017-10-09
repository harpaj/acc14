from flask import Flask, jsonify
import time
from tasks import one_angle

app = Flask(__name__)


@app.route('/run')
def schedule_run():
    start_time = time.time()

    from_angle = 0
    to_angle = 30
    step_size = 10
    naca = '0012'
    nodes = '200'
    refinements = '3'
    samples = "10"
    viscosity = "0.0001"
    speed = "10."
    total = "1"

    for angle in range(from_angle, to_angle+1, step_size):
        task = one_angle.delay(str(angle), *naca, nodes, refinements, samples, viscosity, speed, total)
        break

    result = task.get()
    response = {
        "result": result,
        "duration": time.time() - start_time,
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
