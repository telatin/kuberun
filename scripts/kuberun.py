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
    
    args.add_argument('CMD', type=str, nargs='+', help='Command to execute')
    args.add_argument('-d', '--docker-container', type=str, help='Docker container (default: $(default)s)', default="ubuntu:latest")
    args.add_argument('-n', '--name', type=str, help='Name of the pod (default: $(default)s)', default="mypod")
    args.add_argument('-m', '--memory', type=str, help='Memory limit (default: $(default)s)', default="1Gi")
    args.add_argument('-t', '--threads', type=int, default='1', help='Number of threads (default: %(default)s)')
    args.add_argument('-w', '--workdir', type=str,  help='Temporary directory (default: %(default)s)', default=currentwd)
    args.add_argument('-c', '--config', type=str,  help='Kuberun configuration file (default: %(default)s)', default=config_file)
    args.add_argument('--verbose', action="store_true", help='Verbose output')
    args = args.parse_args()


    name = makepodname(name=args.name)
    values = {
        "name": name,
        "container_name": args.name,
        "docker": args.docker_container,
        "command": " ".join(args.CMD),
        "cpu": str(args.threads),
        "memory": args.memory,
        "workdir": args.workdir,
    }

    template = k8s_template()
    result = template.substitute(values)

    if args.verbose:
        print(f"Running: {name}", file=sys.stderr)

    # Save YAML file (result) to config['workdir']/name.yaml

    yaml_filename = os.path.join(args.workdir, f"{name}.yaml")
    with open(yaml_filename, "w") as f:
        f.write(result)

    cmd = ["kubectl", "apply", "-f", yaml_filename]
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
