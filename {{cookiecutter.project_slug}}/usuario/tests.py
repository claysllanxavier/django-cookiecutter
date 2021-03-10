from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from .models import Profissional, Cliente
import pytest
from model_bakery import baker


class test_auth(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_auth_success(self):
        request = self.client.post(
            '/core/api/usuario/auth', {'username': 'guilherme', 'password': 'asdf1234'})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['user'], 'guilherme')
        self.assertEqual(request.data['password'], 'asdf1234')


@pytest.mark.django_db
def test_profissional_favoritado():
    cliente = baker.make(Cliente)
    cliente2 = baker.make(Cliente)
    profissional = baker.make(Profissional)
    profissional.marcar_favorito(cliente.id)
    profissional.marcar_favorito(cliente2.id)
    profissional.desmarcar_favorito(cliente2.id)
    assert profissional.quantidade_curtidas() == 1
