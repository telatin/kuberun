from string import Template

def k8s_template():
    template_string =  """apiVersion: v1
kind: Pod
metadata:
  name: $name
spec:
  securityContext:
    fsGroup: 1000
    runAsUser: 1000
    runAsGroup: 1000
    fsGroupChangePolicy: OnRootMismatch
  automountServiceAccountToken: false
  nodeSelector:
    hub.jupyter.org/node-purpose: user
  volumes:
    - name: shared-team-volume
      persistentVolumeClaim:
        claimName: cephfs-shared-team
    - name: shared-public-volume
      persistentVolumeClaim:
        claimName: cephfs-shared-ro-public
  containers:
    - name: $container_name
      image: $docker
      workingDir: $workdir
      command: ["/bin/bash", "-c"]
      args: ["$command"]
      resources:
        requests:
          cpu: "$cpu"
          memory: "$memory"
      volumeMounts:
        - name: shared-team-volume
          mountPath: /shared/team
        - name: shared-public-volume
          mountPath: /shared/public
          readOnly: true
  restartPolicy: Never
"""
    return Template(template_string)