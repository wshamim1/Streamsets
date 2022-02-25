from streamsets.sdk import ControlHub

# Replace the argument values according to your setup from prerequisites
## connect to control hub
control_hub = ControlHub(credential_id='****',
                         token='****')


print(control_hub)
## get all Deployments
print(control_hub.deployments.get_all())

### Get all jobs
print(control_hub.jobs.get_all())

jobs=control_hub.jobs
print(jobs)
### Delete all jobs
control_hub.delete_job(jobs)

### get all pipelines and delete

pipeline=control_hub.pipelines
print(pipeline)
control_hub.delete_pipeline(pipeline)
