import pathlib

import pytest
import vcr

from doccano_client.models.label_type import LabelType
from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.label_type import CategoryTypeRepository
from tests.conftest import repository_fixtures


@pytest.fixture
def label_type():
    return LabelType(text="Test Label Type")


class TestCategoryTypeRepository:
    @classmethod
    def setup_class(cls):
        with vcr.use_cassette(str(repository_fixtures / "label_type/login.yaml"), mode="once"):
            client = BaseRepository("http://localhost:8000")
            client.login(username="admin", password="password")
        cls.client = CategoryTypeRepository(client)
        cls.project_id = 16

    def test_create(self, label_type):
        with vcr.use_cassette(str(repository_fixtures / "label_type/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, label_type)
        assert response.text == label_type.text

    def test_update(self, label_type):
        with vcr.use_cassette(str(repository_fixtures / "label_type/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, label_type)
        with vcr.use_cassette(str(repository_fixtures / "label_type/update.yaml"), mode="once"):
            response.text = "Updated Type"
            updated = self.client.update(self.project_id, response)
        assert updated.text == "Updated Type"
        assert updated.id == response.id

    def test_delete(self, label_type):
        with vcr.use_cassette(str(repository_fixtures / "label_type/create.yaml"), mode="once"):
            response = self.client.create(self.project_id, label_type)
        with vcr.use_cassette(str(repository_fixtures / "label_type/delete.yaml"), mode="once"):
            self.client.delete(self.project_id, response.id)

    def test_upload(self):
        file_path = pathlib.Path(__file__).parent.parent / "data/labels.json"
        with vcr.use_cassette(str(repository_fixtures / "label_type/upload.yaml"), mode="once"):
            self.client.upload(self.project_id, file_path)
        with vcr.use_cassette(str(repository_fixtures / "label_type/list.yaml"), mode="once"):
            label_types = self.client.list(self.project_id)
            assert len(label_types) == 2
