# Terraform state lock errors

## Symptoms
`terraform plan` or `apply` fails with "Error acquiring the state lock".

## Cause
Another run holds the lock in the remote backend (for example a DynamoDB table with an S3 backend),
or a previous run crashed and left the lock behind.

## Steps
Check whether a pipeline or colleague is running Terraform right now and wait for it to finish.
If the lock is stale and you are sure no run is active, use `terraform force-unlock <LOCK_ID>`.
Never force-unlock while a real apply is running, because it can corrupt the state.

## Prevention
Run Terraform only through the pipeline, set sensible timeouts, and use one state per environment.
