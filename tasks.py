from celery import Celery
from csv import DictReader
import subprocess

celery = Celery(
    'tasks',
    broker='pyamqp://myuser:mypassword@192.168.1.41:5672/myvhost',
    backend='rpc://myuser:mypassword@192.168.1.41:5672/myvhost'
)
celery.conf.task_serializer = 'json'
celery.conf.task_compression = 'gzip'


@celery.task()
def one_angle(
    angle, naca1, naca2, naca3, naca4, nodes, refinements,
    samples, viscosity, speed, time
):
    filename = angle + '_' + nodes + '_' + naca1 + naca2 + naca3 + naca4 + '.geo'

    # create geo file
    with open("results/geo/" + filename, 'w') as geo_fh:
        subprocess.run(
            [
                "/home/ubuntu/acc14/bin/cloudnaca/naca2gmsh_geo.py",
                angle, naca1, naca2, naca3, naca4, nodes
            ],
            stdout=geo_fh
        )

    # create mesh file
    msh_name = filename[:-3] + "msh"
    subprocess.run([
        "gmsh", "-v", '0', '-nopopup', '-2', '-o', "results/msh/"+msh_name, "results/geo/"+filename
    ])

    # refine mesh file
    for _ in range(int(refinements)):
        subprocess.run(["gmsh", "-refine", "-v", "0", "results/msh/"+msh_name])

    # convert mesh file to xml
    xml_name = filename[:-3] + "xml"
    subprocess.run([
        "dolfin-convert", "-i", "gmsh", "-o", "xml",
        "results/msh/" + msh_name, "results/xml/" + xml_name
    ])

    # run airfoil on xml file
    subprocess.run(
        [
            "/home/ubuntu/acc14/bin/airfoil/airfoil",
            samples, viscosity, speed, time, "../../results/xml/" + xml_name
        ],
        cwd="/home/ubuntu/acc14/bin/airfoil"
    )

    result_name = '_'.join([filename[:-4], samples, viscosity, speed, time, 'drag_ligt.m'])

    # read in and return result
    result = []
    with open("/home/ubuntu/acc14/bin/airfoil/results/" + result_name) as f:
        reader = DictReader(f)
        for row in reader:
            result.append(row)

    return angle, result
