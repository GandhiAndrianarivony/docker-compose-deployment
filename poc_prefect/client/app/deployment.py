from prefect.deployments import Deployment
from flows.flow import test_flow
from prefect.filesystems import LocalFileSystem

block_storage = LocalFileSystem(basepath="/flows")
block_storage.save("local-storages", overwrite=True)

deployment = Deployment.build_from_flow(
    flow=test_flow,
    name="first-attempt",
    work_queue_name="WORK_QUEUE_NAME",
    storage=LocalFileSystem.load("local-storages"),
)

if __name__ == "__main__":
    deployment.apply()
