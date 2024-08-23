# services/configuracao_service.py
from models import ConfiguracaoModel, UsuarioModel
from django.core.exceptions import ObjectDoesNotExist
from  utils import Utils
class ConfiguracaoService:

    @staticmethod
    def get_configuracoes_usuario(id_usuario):
        try:
            configuracoes_usuario = ConfiguracaoModel.objects.filter(usuario_id=id_usuario)
            return {"data": list(configuracoes_usuario.values()), "success": True}, 200
        except ObjectDoesNotExist:
            return {"error": "Usuário ou configurações não encontrados."}, 404

    @staticmethod
    def configuracao_set_session(request, id_usuario):
        try:
            configuracoes_usuario = ConfiguracaoModel.objects.filter(usuario_id=id_usuario)
            if configuracoes_usuario:
                configuracoes_serializadas = {
                    config["codigo"]: config["status_acesso"]
                    for config in configuracoes_usuario.values()
                    if config["status_acesso"]
                }
                request.session["configs_ativos"] = configuracoes_serializadas
                return {"success": True}, 200
            else:
                return {"success": False, "message": "Nenhuma configuração encontrada."}, 404
        except Exception as e:
            print(f"Erro ao definir configurações na sessão: {str(e)}")
            return {"error": str(e)}, 500

    @staticmethod
    def criar_configuracoes_padrao(listModel):
        for model in listModel:
            ConfiguracaoModel.objects.create(
                titulo=model.titulo,
                descricao_interna=model.descricao_interna,
                descricao=model.descricao,
                status_acesso=model.status_acesso,
                codigo=model.codigo,
                usuario=model.usuario,
            )

    @staticmethod
    def list_configuracoes_padrao(usuario=None, status=True):
        classes = Utils.lista_de_configuracao()
        list_configuracao = []
        for classe in classes:
            nome_classe = classe["nome"]
            codigo_interger = classe["codigo"]
            titulo = f"Gerenciamento de {nome_classe}"
            descricao_interna = f"Controle de {nome_classe.lower()}, editar, alterar, criar..."
            descricao = f"Permitir acesso ao Painel de {nome_classe}, isso inclui criar, editar, remover, entre outros."
            status_acesso = status
            id = usuario.id_usuario if hasattr(usuario, "id_usuario") else usuario

            configuracao = ConfiguracaoModel(
                titulo=titulo,
                descricao_interna=descricao_interna,
                descricao=descricao,
                status_acesso=status_acesso,
                codigo=codigo_interger,
                usuario_id=id,
            )
            list_configuracao.append(configuracao)

        return list_configuracao
