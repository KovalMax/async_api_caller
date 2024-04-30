import asyncio

from csv_parser import ClassLoader
from golden_record.csv_row import CsvRow
from golden_record.request import GoldenRecordRequest
from golden_record.service import GoldenRecordService


class GoldenRecordTask:
    def __init__(self, service: GoldenRecordService):
        self.loader = ClassLoader('golden_record',
                                  'csv_row',
                                  'CsvRow')
        self.service = service

    async def execute(self,
                      golden_record: CsvRow | GoldenRecordRequest,
                      semaphore: asyncio.Semaphore):
        if isinstance(golden_record, CsvRow):
            golden_record = GoldenRecordRequest(**golden_record.__dict__())

        async with semaphore:
            return await self.service.get_no_gr(golden_record)
