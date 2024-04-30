import asyncio

from csv_parser import ClassLoader
from status_change.csv_row import CsvRow
from status_change.request import StatusChangeRequest
from status_change.service import StatusChangeService


class StatusChangeTask:
    def __init__(self, service: StatusChangeService):
        self.loader = ClassLoader('status_change',
                                  'csv_row',
                                  'CsvRow')
        self.service = service

    async def execute(self,
                      change_status: CsvRow | StatusChangeRequest,
                      semaphore: asyncio.Semaphore):
        if isinstance(change_status, CsvRow):
            change_status = StatusChangeRequest(**change_status.__dict__())

        async with semaphore:
            return await self.service.change_status(change_status)
