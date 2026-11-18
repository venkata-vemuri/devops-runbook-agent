# High CPU alert on a service

## Triage
Confirm the alert in the dashboard and check whether CPU rose after a deploy or a traffic spike.
Compare the current release time with the start of the spike.

## Investigate
Look at request rate, latency and error rate together. If traffic is normal but CPU is high, suspect the new release.
Check for a runaway process or a retry storm hitting a dependency.

## Mitigate
Roll back the latest release if the spike started with it. Otherwise scale out the deployment and watch the metrics.

## Follow up
Record the root cause, add or tune the alert threshold, and write a short post-incident note.
