from utilities.componentA import ComponentA
from utilities.componentB import ComponentB
import prefect
from prefect import flow, task, get_run_logger

import sys
sys.path.append('app/')


@task
def test_task():
    logger = get_run_logger()
    x = ComponentA(2)
    y = ComponentB(2)
    x = x.n + y.n
    logger.info(f"Test {x}!")  # Should return 4
    return


@flow()
def test_flow():
    test_task()
