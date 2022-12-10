import vcr

from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.task_status import TaskStatusRepository
from tests.conftest import repository_fixtures


class TestTaskStatusRepository:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(repository_fixtures / "task_status/login.yaml"), mode="once"):
            client = BaseRepository("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = TaskStatusRepository(client)

    def test_get(self):
        with vcr.use_cassette(str(repository_fixtures / "task_status/list.yaml"), mode="once"):
            task_id = "2a49f2cf-5508-45d3-b75e-d1dd2489aaf8"
            self.client.get(task_id)
