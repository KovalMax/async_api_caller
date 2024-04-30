from client import BaseClient
from golden_record.service import GoldenRecordService
from golden_record.task import GoldenRecordTask
from status_change.service import StatusChangeService
from status_change.task import StatusChangeTask


class TaskFactory:
    def __init__(self, base_client: BaseClient):
        self.base_client = base_client

    def create_task(self, task_name: str) -> GoldenRecordTask | StatusChangeTask:
        match task_name:
            case "status_change":
                task = StatusChangeTask(
                    StatusChangeService(self.base_client))
            case "golden_record":
                task = GoldenRecordTask(
                    GoldenRecordService(self.base_client))
            case _:
                raise Exception(f'Task for {task_name} not found')

        return task
