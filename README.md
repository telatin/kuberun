# kuberun CLI

The `kuberun` command line tool is designed to simplify running commands using Kubernetes. 
It helps you create and manage Kubernetes pods to execute commands in a containerized environment.

If you have:
1. A Docker container with the program(s) you want to run
2. A command to run... or a bash script to execute under the container

With **kuberun** you can execute a Pod in Kubernetes and run the command in the container.

```bash
kuberun [resources] -d container:latest "run.py -1 file -2 file > output"
```


## Installation

To use the `kuberun` tool, follow these steps:

```bash
# To install it in a separate environment
mamba create -n kuberun python=3.10
conda activate kuberun
pip install -i https://test.pypi.org/simple/ kuberun
```


## Usage

The kuberun tool allows you to run a command using Kubernetes by creating and managing pods. Here's how to use it:

```bash
usage: kuberun.py [-h] [-d DOCKER_CONTAINER] [-n NAME] [-m MEMORY] [-t THREADS] [-w WORKDIR] [-c CONFIG] [--verbose] CMD [CMD ...]

Run a command using Kubernetes

positional arguments:
  CMD                   Command to execute

optional arguments:
  -h, --help            show this help message and exit
  -d DOCKER_CONTAINER, --docker-container DOCKER_CONTAINER
                        Docker container (default: ubuntu:latest)
  -n NAME, --name NAME  Name of the pod (default: mypod)
  -m MEMORY, --memory MEMORY
                        Memory limit (default: 1Gi)
  -t THREADS, --threads THREADS
                        Number of threads (default: 1)
  -w WORKDIR, --workdir WORKDIR
                        Temporary directory (default: current working directory)
  -c CONFIG, --config CONFIG
                        Kuberun configuration file (default: ~/.config/kuberun.ini)
  --verbose             Verbose output
```

## Examples

Here are a few examples of how to use the kuberun tool:

* Run a simple command using the default Docker container (ubuntu:latest):

```bash
kuberun 'echo "Hello, Kubernetes!" > data.txt'
```

* Specify pod name, memory limit, and threads:

```bash
kuberun -n mypod -m 2Gi -t 2 --verbose bash -c "echo 'Hello from Kubernetes!'"
```

* Run Kraken:

```bash
kuberun -m 16 -c 8 -d quay.io/biocontainers/kraken2:2.1.3--pl5321hdcf5f25_0 \
 "kraken2 --threads 8 --db /shared/public/db/kraken2/k2_pluspf_16gb/ --report kraken.tsv --paired sample1_R1.fastq.gz sample1_R2.fastq.gz > /dev/null"
```


## Configuration

The kuberun tool supports configuration using an INI file. 
By default, it uses the file `~/.config/kuberun.ini` as the configuration file. 
You can customize the behavior of the tool using this configuration.

## Authors

Andrea Telatin, Nabil-Fareed Alikhan