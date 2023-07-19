import asyncio
import sys
import time

from client import StatusChangeService, BaseClient, StatusChangeModel as Model
from config import Configuration, Environment
from csv_parser import CsvParser, Row


async def task(row: Row, semaphore: asyncio.Semaphore):
    async with semaphore:
        return await change_status_service.change_status(Model(**row.__dict__()))


async def task_runner():
    failed_tasks = 0
    semaphore = asyncio.Semaphore(150)
    event_loop = asyncio.get_event_loop()
    tasks = [event_loop.create_task(task(row, semaphore)) for row in csv_parser.iterate()]
    for coroutine in asyncio.as_completed(tasks):
        result = await coroutine

        print(result.info)
        if not result.succeed:
            failed_tasks += 1

    print(f'Total {len(tasks)} task(s) has been executed')
    if failed_tasks:
        print(f'And {failed_tasks} of them has been failed')


def main():
    asyncio.run(task_runner())


if __name__ == '__main__':
    start_time = time.time()

    try:
        _, env, file_path, delimiter = sys.argv
    except ValueError:
        _, env, file_path = sys.argv
        delimiter = ','

    print(f'Starting invocation using "{delimiter}" as csv file delimiter')
    env = Environment(env)
    config = Configuration()
    csv_parser = CsvParser(file_path, delimiter)
    client = BaseClient(env, config)
    change_status_service = StatusChangeService(config.change_status_uri(), client)
    main()
    print(f'--- Time elapsed {time.time() - start_time:.1f} seconds ---')
