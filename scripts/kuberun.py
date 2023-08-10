#!/usr/bin/env python3
import os
import sys
import argparse
from kuberun.core import KuberRun
from kuberun.template import k8s_template
from kuberun.pods import getpodnames, makepodname, makefilename
from kuberun.config import loadconfig
import tempfile
from string import Template
import subprocess





def main():

    config_file = os.path.join(os.path.expanduser("~"), ".config", "kuberun.ini")
    config = loadconfig(config_file=config_file)
    currentwd = os.getcwd()
    args = argparse.ArgumentParser(description='Run a command using Kubernetes')
    
    args.add_argument('CMD', type=str, help='Command to execute or script to run')
    args.add_argument('-d', '--docker-container', type=str, help='Docker container (default: %(default)s)', default="ubuntu:latest")
    args.add_argument('-n', '--name', type=str, help='Name of the pod (default: %(default)s)', default="mypod")
    args.add_argument('-m', '--memory', type=str, help='Memory limit in Gb (default: %(default)s)', default="1Gi")
    args.add_argument('-t', '--threads', type=int, default='1', help='Number of threads (default: %(default)s)')
    args.add_argument('-w', '--workdir', type=str,  help='Temporary directory (default: %(default)s)', default=currentwd)
    args.add_argument('-c', '--config', type=str,  help='Kuberun configuration file (default: %(default)s)', default=config_file)
    args.add_argument('--dry', action="store_true", help='Save YAML file but do not run')
    args.add_argument('--verbose', action="store_true", help='Verbose output')
    args = args.parse_args()

    # If memory is a number, add Gi
    if args.memory.isdigit():
        args.memory = f"{args.memory}Gi"

    bash_str = '"bash"' if os.path.exists(args.CMD) else '"/bin/bash", "-c"'
    command  = f"bash '{os.path.abspath(args.CMD)}'" if os.path.exists(args.CMD) else args.CMD

    if not os.path.exists(args.workdir):
        print(f"Error: {args.workdir} does not exist", file=sys.stderr)
        sys.exit(1)


    name = makepodname(name=args.name)

    values = {
        "bash": bash_str,
        "name": name,
        "container_name": args.name,
        "docker": args.docker_container,
        "command": command,
        "cpu": str(args.threads),
        "memory": args.memory,
        "workdir": args.workdir,
    }

    template = k8s_template()
    result = template.substitute(values)
    yaml_filename = makefilename(os.path.join(args.workdir, f"{name}"), ".yaml")
    if args.verbose:
        print(f"Running:  {name}", file=sys.stderr)
        print(f"Saved to: {yaml_filename}", file=sys.stderr)
    # Save YAML file (result) to config['workdir']/name.yaml

    try:
        with open(yaml_filename, "w") as f:
            f.write(result)
    except IOError:
        print(f"Error: Could not write to {yaml_filename}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: while trying write to {yaml_filename}:\n  {e}", file=sys.stderr)
        sys.exit(1)

    cmd = ["kubectl", "apply", "-f", yaml_filename]
    if not args.dry:
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Dry run. Not running: ", " ".join(cmd))
        sys.exit(0)

if __name__ == '__main__':
    main()
