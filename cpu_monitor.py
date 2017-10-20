import time, threading
import subprocess

period = 600
evaluations = 10

def monitor_cluster_cpu(avg_demand, eval_counter):
    cons = 0
    queue_size = 0
    queued_demand = 0.0

    if eval_counter >= evaluations-1:
        if avg_demand/eval_counter > 0.6:
            subprocess.run(['curl', '-X', 'POST', 'https://hpc2n.cloud.snic.se:8000/v1/signal/arn%3Aopenstack%3Aheat%3A%3Aad5091c4f42e4defb98eb9550f875f4f%3Astacks%2Fairfoil_asg_stack_g14%2F8be3ad1e-d91d-4f90-b355-8a570dc8492d%2Fresources%2Fscaleup_policy?Timestamp=2017-10-20T18%3A16%3A58Z&SignatureMethod=HmacSHA256&AWSAccessKeyId=728253c671ee4e87a70fbcc47e10860f&SignatureVersion=2&Signature=7WHSwpnabGkk5I6b2b1cwx3JxLCVNrvFOJfEG0EeRwk%3D'])
            print("Scaling up")
        elif avg_demand/eval_counter < 0.3:
            subprocess.run(['curl', '-X', 'POST', 'https://hpc2n.cloud.snic.se:8000/v1/signal/arn%3Aopenstack%3Aheat%3A%3Aad5091c4f42e4defb98eb9550f875f4f%3Astacks%2Fairfoil_asg_stack_g14%2F8be3ad1e-d91d-4f90-b355-8a570dc8492d%2Fresources%2Fscaledown_policy?Timestamp=2017-10-20T18%3A16%3A58Z&SignatureMethod=HmacSHA256&AWSAccessKeyId=ba57b09f02184b8d9bad7846e629c38b&SignatureVersion=2&Signature=Hztm%2FE825s267Obud41qPWV%2BmxV7qVNNJ13TZwPJXaw%3D'])
            print("Scaling down")
        else:
            print("Idle")

        eval_counter = 0
        avg_demand = 0

    rabbit_output = subprocess.check_output(["rabbitmqctl", "list_queues", "-p", "myvhost", "name", "consumers", "messages"])
    rabbit_list = rabbit_output.decode("UTF-8").splitlines()
    rabbit = (rabbit_list[2].split("\t"))
    cons = int(rabbit[1])
    queue_size = int(rabbit[2]) + cons
    queued_demand = (1.0 - float(cons/queue_size)) or 0
    avg_demand += queued_demand
    eval_counter += 1

    threading.Timer(period/evaluations, monitor_cluster_cpu, [avg_demand, eval_counter]).start()

monitor_cluster_cpu(0, 0)

