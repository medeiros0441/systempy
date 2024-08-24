from api.utils import Utils
from api.models import LojaModel, EnderecoModel, AssociadoModel, UsuarioModel, EmpresaModel

class LojaService:

    @staticmethod
    def create_loja(data, empresa_instance, usuario_id):
        try:
            # Criar endereço
            endereco = EnderecoModel(
                rua=data["rua"],
                cidade=data["cidade"],
                estado=data["estado"],
                cep=data["cep"],
            )
            endereco.save()

            # Criar loja
            loja = LojaModel(
                nome=data["nome"],
                descricao=data["descricao"],
                endereco=endereco,
                empresa=empresa_instance,
            )
            loja.save()

            # Associar usuários
            usuario_adm = UsuarioModel.objects.get(
                empresa_id=loja.empresa_id, nivel_usuario=1
            )
            associados = [
                AssociadoModel(usuario_id=usuario_id, loja=loja, status_acesso=True)
            ]
            if usuario_adm.id_usuario != usuario_id:
                associados.append(
                    AssociadoModel(usuario=usuario_adm, loja=loja, status_acesso=True)
                )
            AssociadoModel.objects.bulk_create(associados)

            return loja, True, f"LojaModel {loja.nome} criada com sucesso."
        except Exception as e:
            return None, False, f"Erro ao criar loja: {str(e)}"

    @staticmethod
    def update_loja(id_loja, data):
        try:
            loja = LojaModel.objects.get(id_loja=id_loja)
            endereco = loja.endereco

            # Atualizar endereço
            endereco.rua = data.get("rua", endereco.rua)
            endereco.cidade = data.get("cidade", endereco.cidade)
            endereco.estado = data.get("estado", endereco.estado)
            endereco.cep = data.get("cep", endereco.cep)
            endereco.save()

            # Atualizar loja
            loja.nome = data.get("nome", loja.nome)
            loja.descricao = data.get("descricao", loja.descricao)
            loja.endereco = endereco
            loja.save()

            return loja, True, f"LojaModel {loja.nome} atualizada com sucesso."
        except LojaModel.DoesNotExist:
            return None, False, f"Loja com ID {id_loja} não encontrada."
        except Exception as e:
            return None, False, f"Erro ao atualizar loja: {str(e)}"

    @staticmethod
    def delete_loja(id_loja):
        try:
            loja = LojaModel.objects.get(id_loja=id_loja)
            loja.delete()
            return True, "LojaModel excluída com sucesso."
        except LojaModel.DoesNotExist:
            return False, f"Loja com ID {id_loja} não encontrada."
        except Exception as e:
            return False, f"Erro ao excluir loja: {str(e)}"

    @staticmethod
    def list_lojas(id_empresa):
        try:
            lojas = LojaModel.objects.filter(empresa_id=id_empresa)
            lojas_json = []
            for loja in lojas:
                loja_data = {
                    "id_loja": loja.id_loja,
                    "nome": loja.nome,
                    "numero_telefone": loja.numero_telefone,
                    "horario_operacao_inicio": (
                        loja.horario_operacao_inicio.strftime("%H:%M:%S")
                        if loja.horario_operacao_inicio
                        else None
                    ),
                    "horario_operacao_fim": (
                        loja.horario_operacao_fim.strftime("%H:%M:%S")
                        if loja.horario_operacao_fim
                        else None
                    ),
                    "segunda": loja.segunda,
                    "terca": loja.terca,
                    "quarta": loja.quarta,
                    "quinta": loja.quinta,
                    "sexta": loja.sexta,
                    "sabado": loja.sabado,
                    "domingo": loja.domingo,
                    "insert": loja.insert,
                    "update": loja.update,
                    "empresa": loja.empresa.id_empresa,
                    "endereco": loja.endereco.id if loja.endereco else None,
                }
                associados = AssociadoModel.objects.filter(loja=loja)
                loja_data["associados"] = [
                    {
                        "id_associado": associado.id_associado,
                        "insert": associado.insert,
                        "update": associado.update,
                        "status_acesso": associado.status_acesso,
                        "usuario": {
                            "id_usuario": associado.usuario.id_usuario,
                            "nome_completo": associado.usuario.nome_completo,
                        },
                        "loja": associado.loja.id_loja,
                    }
                    for associado in associados
                ]
                lojas_json.append(loja_data)

            return lojas_json, True, "Lojas recuperadas com sucesso."
        except Exception as e:
            return [], False, f"Erro ao listar lojas: {str(e)}"
