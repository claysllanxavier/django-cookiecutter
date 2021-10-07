import pytest
import pytest_django
from faker import Faker
from validate_docbr import CPF
from model_bakery import baker
from usuario.forms import UsuarioForm
from usuario.models import Profissional
from django.contrib.auth.models import Group


class TestUsuarioForm:
    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")

    def test_usuario_create(self, init):
        form_data = {
            "nome": self.faker.name(),
            "email": self.faker.company_email(),
            "latitude": 0.0,
            "longitude": 0.0,
        }
        form = UsuarioForm(data=form_data)
        assert form.is_valid() is True