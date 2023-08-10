import pytest

def test_import():
    from kuberun.core import KuberRun
    from kuberun.template import k8s_template
    from kuberun.pods import getpodnames, makepodname
    from kuberun.config import loadconfig, saveconfig
    assert True

def test_script():
    # ./scripts/kuberun.py
    import os
    import sys
    import subprocess
    assert os.path.exists("./scripts/kuberun.py")
    cmd = ["./scripts/kuberun.py", "--help"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    assert p.returncode == 0