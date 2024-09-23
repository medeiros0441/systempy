from .CustomModelSerializer import CustomModelSerializer
from api.models import UsuarioModel,PersonalizacaoModel
from rest_framework import serializers
from api.services import UsuarioService
class UsuarioSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = UsuarioModel
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

    def validate(self, attrs):
        """Validação específica para o usuário."""
        errors = {}

        # Verifica campos obrigatórios
        if not attrs.get('nome_completo'):
            errors['nome_completo'] = 'Nome completo é obrigatório.'
        if not attrs.get('email'):
            errors['email'] = 'Email é obrigatório.'
        if not attrs.get('senha'):
            errors['senha'] = 'Senha é obrigatória.'

        # Se houver erros, formate-os e levante a exceção
        if errors:
            formatted_errors = self.format_errors(errors)
            raise serializers.ValidationError(formatted_errors)

        # Verifica se o email já existe
        if UsuarioService.verificar_email(attrs['email']):
            raise serializers.ValidationError("O email já está cadastrado em nossa base de dados, escolha outro.")

        return attrs
    
class PersonalizacaoSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = PersonalizacaoModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_personalizacao',
            'usuario',
            'chave',
            'valor',
            'descricao',
            'descricao_interna',
            'codigo',
        ]
