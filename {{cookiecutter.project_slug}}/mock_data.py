"""Código para popular dados de exemplo"""

import os

import django
from faker import Faker
from validate_docbr import CPF

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
django.setup()


from usuario.models import Usuario


class Mock:
    def __init__(self, *args, **kwargs):
        super(Mock, self).__init__(*args, **kwargs)
        self.fake = Faker("pt_br")
        # Faker.seed(10)

    def criar_usuarios(self):
        try:
            for _ in range(10):
                cpf = CPF().generate()
                nome = self.fake.name()
                email = "{}@{}".format(nome.lower(), self.fake.free_email_domain()).replace(" ", "")
                telefone = self.fake.phone_number()
                endereco_comercial = self.fake.address()

                Usuario.objects.create(
                    nome=nome,
                    cpf=cpf,
                    email=email,
                    telefone=telefone,
                    endereco=endereco_comercial,
                )
        except Exception as error:
            print(error)


if __name__ == "__main__":
    Mock().criar_usuarios()
