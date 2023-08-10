import pytest

def test_import():
    from kuberun.core import KuberRun
    from kuberun.template import k8s_template
    from kuberun.pods import getpodnames, makepodname
    from kuberun.config import loadconfig, saveconfig
    assert True

