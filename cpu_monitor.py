import time, threading
import subprocess

period = 120
evaluations = 2

def monitor_cluster_cpu(avg_demand, eval_counter):
    cons = 0
    queue_size = 0
    queued_demand = 0.0

    if eval_counter >= evaluations-1:
        if avg_demand/eval_counter > 0.6:
            subprocess.run(["curl", "-X", "POST", "-i", "https://hpc2n.cloud.snic.se:8000/v1/signal/arn%3Aopenstack%3Aheat%3A%3Aad5091c4f42e4defb98eb9550f875f4f%3Astacks%2Fairfoil_asg_stack_g14%2F3a1326b1-1ccd-438a-8bc8-172c07f73fe2%2Fresources%2Fscaleup_policy?Timestamp=2017-10-20T16%3A23%3A51Z&SignatureMethod=HmacSHA256&AWSAccessKeyId=c8fcde5637bd447a942c487ab54caabe&SignatureVersion=2&Signature=JLlpeTgA%2BowAC%2BlW1UZYtAG%2Bx5fSPHfS%2BhPv54bTnBA%3D"])
            print("Scaling up")
        elif avg_demand/eval_counter < 0.3:
            subprocess.run(["curl", "-X", "POST", "-i", "https://hpc2n.cloud.snic.se:8000/v1/signal/arn%3Aopenstack%3Aheat%3A%3Aad5091c4f42e4defb98eb9550f875f4f%3Astacks%2Fairfoil_asg_stack_g14%2F3a1326b1-1ccd-438a-8bc8-172c07f73fe2%2Fresources%2Fscaledown_policy?Timestamp=2017-10-20T16%3A23%3A51Z&SignatureMethod=HmacSHA256&AWSAccessKeyId=12444fc58213478eaa4c7e4f7b1a3487&SignatureVersion=2&Signature=bc8oQOuZ8MSH1ZRy93WDzXvcgnfZzxADjadUA9saLG0%3D"])
            print("Scaling down")
        else:
            print("Idle")

        eval_counter = 0
        avg_demand = 0

    rabbit_output = subprocess.check_output(["rabbitmqctl", "list_queues", "-p", "myvhost", "name", "consumers", "messages"])
    rabbit_list = rabbit_output.decode("UTF-8").splitlines()
    rabbit = (rabbit_list[1].split("\t"))
    cons = int(rabbit[1])
    queue_size = int(rabbit[2]) + cons
    queued_demand = 1.0 - float(cons/queue_size)
    avg_demand += queued_demand
    eval_counter += 1
    threading.Timer(period/evaluations, monitor_cluster_cpu, [avg_demand, eval_counter]).start()

monitor_cluster_cpu(0, 0)

