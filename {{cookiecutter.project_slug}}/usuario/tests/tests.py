import pytest
from django.contrib.auth.models import Group
from usuario.models import Usuario
from faker import Faker
from validate_docbr import CPF
from model_bakery import baker


class TestUsuario:
    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.usuario = baker.make('usuario.Profissional')

    def test_criar_usuario(self, init):
        assert Usuario.objects.all().count() == 1
