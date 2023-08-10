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
    args.add_argument('POD', type=str, nargs='*', help='Podnames')
    args.add_argument("--verbose", action="store_true", help="Verbose output")
    args.add_argument('-d', '--delete', help="Delete matching pods", action="store_true")
    args.add_argument('-n', '--dry-run', help="Do not actually delete matching pods", action="store_true")
    args = args.parse_args()

    pods = getpodnames()
    cmds = []
    for pod in pods:
        if pod == os.getenv("HOSTNAME"):
            # Do not delete the pod we are running in
            continue
        for query in args.POD:
            if query == pod:
                
                if args.delete:
                    print(pod, " DELETE ")
                    if not args.dry_run:
                        cmd = ["kubectl", "delete", "pod", pod]
                        cmds.append(cmd)
                else:
                    print(pod, " * ")
            elif query in pod:
                if args.delete:
                    print(pod, " DELETE ")
                    if not args.dry_run:
                        cmd = ["kubectl", "delete", "pod", pod]
                        cmds.append(cmd)
                    
            else:
                print(pod)
    
    if args.delete:
        for cmd in cmds:
            try:
                subprocess.run(cmd)
            except Exception as e:
                print(e)
                print("Error running: ", cmd)
                

    


if __name__ == '__main__':
    main()
