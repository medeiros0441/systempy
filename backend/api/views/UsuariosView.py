from api.user import UserInfo
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from api.models import UsuarioModel, ConfiguracaoModel, LojaModel, AssociadoModel
from api.utils import Utils
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from api.permissions import CustomPermission
from rest_framework import viewsets, status
from rest_framework.response import Response
from api.services import UsuarioService,LojaService,EmpresaService
from api.models import UsuarioModel
from api.serializers import UsuarioSerializer
from api.permissions import CustomPermission
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
import uuid


class UsuariosView(viewsets.ViewSet):
    permission_classes = [CustomPermission]

    def get_permissions(self):
        permissions = [permission() for permission in self.permission_classes]
        for permission in permissions:
            if isinstance(permission, CustomPermission):
                permission.codigo_model = "usuario"
                permission.auth_required = True
        return permissions
    
    def create(self, request):
        """
        Cria um novo usuário.
        """
        data = request.data.get('usuario', {})

        # Obtém o ID da empresa associada ao usuário
        id_empresa = UserInfo.get_id_empresa(request)
        # Criptografa a senha
        data['senha'] = make_password(data['senha'])
        # Gera um nome de usuário único
        nome_usuario = data['nome_completo'].replace(" ", "").lower()
        while UsuarioService.exist_nome_usuario(nome_usuario):
            nome_usuario = f"{nome_usuario}{Utils.gerar_numero_aleatorio()}"

        data['nome_usuario'] = nome_usuario

        # Verifica se a empresa existe
        empresa = EmpresaService.get_exist_empresa(id_empresa, return_data=True)
        if not empresa:
            return Response({"message": "Empresa não encontrada."}, status=status.HTTP_400_BAD_REQUEST)
        
        data['empresa'] = empresa.pk

        # Valida e cria o usuário
        serializer = UsuarioSerializer(data=data)
        if serializer.is_valid():
            usuario = UsuarioService.create_usuario(serializer.data)

            # Associa o usuário às lojas conforme o status de acesso
            status_acesso = data.get("status_acesso", {})
            for loja_id, acesso in status_acesso.items():
                LojaService.associate_usuario_loja(loja_id=loja_id, id_usuario=usuario.id, id_status_acesso=acesso)

            return Response(UsuarioSerializer(usuario).data, status=status.HTTP_201_CREATED)

        # Usa a função format_errors para tratar os erros do serializer
        formatted_errors = serializer.format_errors(serializer.errors)
        return Response({"message": formatted_errors}, status=status.HTTP_400_BAD_REQUEST)



        

    def list(self, request):
        """
        Retorna todos os usuários se o usuário for um administrador.
        """
        if not request.user.is_superuser:  # Verifica se o usuário é um administrador
            return Response({'detail': 'Você não tem permissão para acessar esta informação.'}, status=403)

        usuarios = UsuarioService.get_all_usuarios()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='empresa(?:/(?P<id_empresa>[^/.]+))?')
    def get_usuarios_by_empresa(self, request, id_empresa=None):
        if not id_empresa:
            id_empresa = UserInfo.get_id_empresa(request)

        # Aqui você pode querer validar se id_empresa é um UUID válido
        try:
            # Validação de UUID
            uuid.UUID(id_empresa)  # Verifica se é um UUID válido
        except ValueError:
            return Response({'detail': 'O valor fornecido não é um UUID válido.'}, status=400)

        usuarios = UsuarioService.get_usuarios_by_empresa(id_empresa)
        if not usuarios:
            return Response({'detail': 'Nenhum usuário encontrado para esta empresa.'}, status=404)

        serializer = UsuarioSerializer(usuarios, many=True)
        return Response({'data': serializer.data, 'sucesso': True})


    @action(detail=False, methods=['get'], url_path='usuario/(?P<usuario_id>[^/.]+)')
    def get_usuario_by_id(self, request, usuario_id):
        """
        Retorna um único usuário baseado no ID fornecido.
        """
        try:
            usuario = UsuarioService.get_usuario_by_id(usuario_id)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data)
        except UsuarioModel.DoesNotExist:
            return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
 

    def retrieve(self, request, pk=None):
        """
        Retorna um usuário específico.
        """
        usuario = UsuarioService.get_usuario_by_id(pk)
        if usuario:
            return Response(UsuarioSerializer(usuario).data)
        return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        Atualiza um usuário específico.
        """
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = UsuarioService.update_usuario(pk, serializer.validated_data)
            if usuario:
                return Response(UsuarioSerializer(usuario).data)
            return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Deleta um usuário específico.
        """
        success = UsuarioService.delete_usuario(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], url_path='bloquear')
    def bloquear_usuario(self, request):
        id_usuario = request.data.get("id_usuario")
        if not id_usuario:
            return Response({"message": "ID do usuário não fornecido."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = UsuarioService.bloquear_usuario(id_usuario)
            return Response(UsuarioSerializer(usuario).data, status=status.HTTP_200_OK)
        except UsuarioModel.DoesNotExist:
            return Response({"message": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='ativar')
    def ativar_usuario(self, request):
        id_usuario = request.data.get("id_usuario")
        if not id_usuario:
            return Response({"message": "ID do usuário não fornecido."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = UsuarioService.ativar_usuario(id_usuario)
            return Response(UsuarioSerializer(usuario).data, status=status.HTTP_200_OK)
        except UsuarioModel.DoesNotExist:
            return Response({"message": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def autenticar_usuario(email, senha):
        try:
            usuario = UsuarioModel.objects.get(email__iexact=email)
            if check_password(senha, usuario.senha):
                return usuario
        except UsuarioModel.DoesNotExist:
            pass
        return None

 

    @staticmethod
    @require_http_methods(["POST"])
    def configuracao_usuario(request, id_usuario):
        try:
            # Carrega e decodifica os dados JSON do corpo da requisição
            data = json.loads(request.body)

            # Verifica se os dados contêm configurações
            if "configuracoes" in data:
                for key, value in data["configuracoes"].items():
                    if key.startswith("status_acesso_"):
                        configuracao_id = key.replace("status_acesso_", "")
                        # Atualiza o status de acesso para a configuração correspondente
                        configuracao = get_object_or_404(
                            ConfiguracaoModel, id_configuracao=configuracao_id
                        )
                        configuracao.status_acesso = value == "on"
                        configuracao.update = timezone.now()
                        configuracao.save()

                return JsonResponse(
                    {"message": "Configurações salvas com sucesso!"}, status=200
                )
            else:
                return JsonResponse(
                    {
                        "message": "Dados de configuração não encontrados no corpo da requisição."
                    },
                    status=400,
                )

        except ConfiguracaoModel.DoesNotExist:
            return JsonResponse({"message": "Configuração não encontrada."}, status=404)

        except Exception as e:
            # Captura e retorna qualquer outro erro inesperado
            return JsonResponse({"message": str(e)}, status=500)
 
