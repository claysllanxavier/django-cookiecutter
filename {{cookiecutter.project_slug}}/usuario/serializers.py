from drf_jsonmask.serializers import FieldsListSerializerMixin
from rest_framework.serializers import ModelSerializer

from .models import Usuario


class UsuarioSerializer(ModelSerializer):
    """ Class do serializer do model Usuario para os métodos POST, PUT, PATCH, DELETE """
    class Meta:
        model = Usuario
        exclude = ['deleted', 'enabled']


class UsuarioGETSerializer(FieldsListSerializerMixin, ModelSerializer):
    """ Class do serializer do model Usuario para o método GET """
    class Meta:
        model = Usuario
        exclude = ['deleted', 'enabled']