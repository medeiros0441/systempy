from CustomModelSerializer import CustomModelSerializer
from models import Usuario,Personalizacao

class UsuarioSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = Usuario
        fields = CustomModelSerializer.Meta.fields + [
            'id_usuario',
            'nome_completo',
            'nome_usuario',
            'senha',
            'nivel_usuario',
            'status_acesso',
            'email',
            'ultimo_login',
            'empresa',
        ]

class PersonalizacaoSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = Personalizacao
        fields = CustomModelSerializer.Meta.fields + [
            'id_personalizacao',
            'usuario',
            'chave',
            'valor',
            'descricao',
            'descricao_interna',
            'codigo',
        ]
