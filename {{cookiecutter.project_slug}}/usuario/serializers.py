from drf_jsonmask.serializers import FieldsListSerializerMixin
from rest_framework.serializers import ModelSerializer, CharField

from .models import Cliente, Profissao, Profissional


class ProfissaoSerializer(FieldsListSerializerMixin, ModelSerializer):
    """ Class para gerenciar o serializer do model Profissao """

    class Meta:
        model = Profissao
        fields = '__all__'


class ClienteSerializer(FieldsListSerializerMixin, ModelSerializer):
    """ Class para gerenciar o serializer do model Cliente """

    class Meta:
        model = Cliente
        fields = '__all__'


class ProfissionalSerializer(FieldsListSerializerMixin, ModelSerializer):
    """ Class para gerenciar o serializer do model Profissional """

    class Meta:
        model = Profissional
        fields = '__all__'


class ProfissionalGetSerializer(FieldsListSerializerMixin, ModelSerializer):
    """ Classe responsável por serializar o objeto para json
    
    O fields no class Meta, pode ser alterado para controlar quais campos serão serializados ou não, também
    é possível adicionar o campo que não se deseja serializar no exclude: list
     
    Por padrão o exclude: list traz configurados os campos da classe Base, caso deseje retornar alguns desses campos
    lembre-se de removê-lo da lista.
    
    Esse Serializer herda de FieldsListSerializerMixin além do ModelSerializer, essa herança é necessária para permitir
    que nas consultas seja utilizado o parâmetro fields: string aonde pode ser estipulado quais campos deverão ser 
    retornados, como por exemplo http://path_endpoint/?fields=nome,email,cpf.
    
    Caso o import do pacote FieldsListSerializerMixin não ocorra de forma automática, basta adicionar a linha abaixo 
    nos imports
    
    from drf_jsonmask.serializers import FieldsListSerializerMixin
    
    Se for utilizado na url o parâmetro fields o processo de consulta ao banco de dados e também de serialização terá
    um ganho de desempenho, portanto sempre que possível utilize essa funcionalidade.
    """

    categoria_nome = CharField(source='categoria.get_nome_display', allow_blank=True, allow_null=True)
    categoria_nome_id = CharField(source="categoria.nome", allow_null=True, allow_blank=True)
    quantidade_favoritados = CharField(source='quantidade_curtidas', allow_blank=True)
    profissao_nome = CharField(source='profissao.nome', allow_blank=True, allow_null=True)

    class Meta:
        model = Profissional
        exclude = ['enabled', 'deleted', 'created_on', 'updated_on', ]

