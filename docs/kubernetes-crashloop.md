# Pod in CrashLoopBackOff

## Symptoms
A pod restarts repeatedly and `kubectl get pods` shows the status CrashLoopBackOff.

## First checks
Run `kubectl describe pod <name>` and look at the Events section and the last state exit code.
Run `kubectl logs <name> --previous` to see the logs from the crashed container.

## Common causes
Exit code 137 usually means the container was killed for exceeding its memory limit (OOMKilled).
A failing liveness probe restarts the container; check the probe path, port and timeout.
A missing ConfigMap or Secret keeps the container from starting; confirm the names match.

## Fix
Raise the memory limit or fix the leak, correct the probe settings, or add the missing config, then redeploy.
