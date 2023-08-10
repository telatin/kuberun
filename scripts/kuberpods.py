#!/usr/bin/env python3
import os
import sys
import argparse
from kuberun.core import KuberRun
from kuberun.template import k8s_template
from kuberun.pods import getpodnames, makepodname
from kuberun.config import loadconfig, saveconfig
import tempfile
from string import Template
import subprocess





def main():

    config_file = os.path.join(os.path.expanduser("~"), ".config", "kuberun.ini")
    config = loadconfig(config_file=config_file)
    currentwd = os.getcwd()
    args = argparse.ArgumentParser(description='Run a command using Kubernetes')
    args.add_argument('POD', type=str, nargs='+', help='Podnames')
    args.add_argument("--verbose", action="store_true", help="Verbose output")
    args = args.parse_args()

    pods = getpodnames()
    for pod in pods:
        for query in args.POD:
            if query in pod:
                print(pod, " * ")
            else:
                print(pod)

    


if __name__ == '__main__':
    main()
