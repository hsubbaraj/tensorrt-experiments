import os
import socket
import time
from shlex import split
from subprocess import Popen
import click
import redis
import numpy as np

TOTAL_CORES = 32


class ClientRun:
    def __init__(self, result_path, num_procs):
        self.result_path = result_path
        self.num_proc = num_procs

        self.proc = None

        self.core = None

    def run(self):
        cmd = ["python", "grpc_image_client.py", "-m resnet50_netdef", "-s INCEPTION", "-b 1"]
        cmd += ["--result-path", self.result_path]
        cmd += ["mug.jpg"]

        cmd = split(" ".join(map(str, cmd)))
        print(" ".join(cmd))
        self.proc = Popen(cmd, env=dict(os.environ, CUDA_VISIBLE_DEVICES="0"))

    def wait(self):
        self.proc.wait()




@click.command()
@click.option("--result-dir", required=True)
@click.option("--num-procs", "-n", type=int, required=True)
def master(
    result_dir,
    num_procs,
):

    clients = [
        ClientRun(os.path.join(result_dir, f"{i+1}.pq"), num_procs)
        for i in range(num_procs)
    ]

    [c.run() for c in clients]
    [c.wait() for c in clients]


if __name__ == "__main__":
    master()

