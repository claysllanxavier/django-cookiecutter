import pytest
from faker import Faker
from model_bakery import baker
from usuario.models import Usuario


class TestUsuario:
    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.usuario = baker.make('usuario.Usuario')

    def test_criar_usuario(self, init):
        assert Usuario.objects.all().count() == 1