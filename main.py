import asyncio
import sys
import time

from client import BaseClient
from config import Configuration, Environment
from csv_parser import CsvParser
from task_factory import TaskFactory


async def task_runner():
    failed_tasks = 0
    semaphore = asyncio.Semaphore(150)
    event_loop = asyncio.get_event_loop()
    tasks = [event_loop.create_task(task_handler.execute(row, semaphore)) for row in
             csv_parser.iterate()]
    re_try = []
    for coroutine in asyncio.as_completed(tasks):
        result = await coroutine

        if not result.succeed:
            re_try.append(result.req)
            failed_tasks += 1

            continue

        if not result.skip:
            print(result.info)

    if len(re_try) > 0:
        await asyncio.sleep(5)
        re_try = [event_loop.create_task(task_handler.execute(row, semaphore)) for row in re_try]
        for coroutine in asyncio.as_completed(re_try):
            result = await coroutine

            if not result.skip:
                print(result.info)

            if result.succeed:
                failed_tasks -= 1

    print(f'--- Total {len(tasks)} task(s) have been executed ---')
    if failed_tasks:
        print(f'--- {failed_tasks} of them have been failed ---')


def main():
    asyncio.run(task_runner())


if __name__ == '__main__':
    start_time = time.time()

    try:
        _, env, task_name, file_path, delimiter = sys.argv
    except ValueError:
        _, env, task_name, file_path = sys.argv
        delimiter = ','

    print(f'Starting invocation using "{delimiter}" as csv file delimiter')

    env = Environment(env)
    config = Configuration()
    client = BaseClient(env, config)
    factory = TaskFactory(client)
    task_handler = factory.create_task(task_name)
    csv_parser = CsvParser(file_path,
                           delimiter,
                           task_handler.loader)

    main()

    print(f'--- Time elapsed {time.time() - start_time:.1f} seconds ---')
