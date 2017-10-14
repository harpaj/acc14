from flask import Flask, jsonify, request
from celery.result import ResultSet
import time
from tasks import one_angle

app = Flask(__name__)


@app.route('/run')
def schedule_run():
    start_time = time.time()
    args = request.args
    try:
        from_angle = int(args.get('from_angle'))
        to_angle = int(args.get('to_angle'))
        step_size = int(args.get('step_size'))
        naca = args.get('naca', '0012')
        assert len(naca) == 4
        nodes = args.get('nodes', '200')
        int(nodes)
        refinements = args.get('refinements', '0')
        assert 0 <= int(refinements) <= 2
        samples = args.get('samples', '10')
        int(samples)
        viscosity = args.get('viscosity', '0.0001')
        float(viscosity)
        speed = args.get('speed', '10.')
        float(speed)
        total_time = args.get('total_time', '1')
        int(total_time)
    except (TypeError, ValueError, AssertionError) as e:
        return jsonify({
            "message": "You delivered invalid parameters.",
            "required_parameters": {
                "from_angle": {"type": "int"},
                "to_angle": {"type": "int"},
                "step_size": {"type": "int"}
            },
            "optional parameters": {
                "naca": {"type": "char[4]", "default": "0012"},
                "nodes": {"type": "int", "default": "20"},
                "refinements": {"type": "[0, 1, 2]", "default": "0"},
                "samples": {"type": "int", "default": "10"},
                "viscosity": {"type": "float", "default": "0.0001"},
                "speed": {"type": "float", "default": "10."},
                "total_time": {"type": "int", "default": "1"}
            },
            "python_error": str(e)
        })

    tasks = []
    for angle in range(from_angle, to_angle+1, step_size):
        tasks.append(one_angle.delay(
            str(angle), *naca, nodes, refinements, samples, viscosity, speed, total_time))

    results = ResultSet(tasks).join_native()

    response = {
        "result": dict(results),
        "duration": time.time() - start_time,
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
