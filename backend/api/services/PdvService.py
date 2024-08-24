from api.models import AssociadoPdvModel, UsuarioModel, PdvModel
class PdvService:
    pass
class TransacaoPdvService:
    pass

class RegistroDiarioPdvService:
    pass 


class AssociadoPdvService:

    
    @staticmethod
    def list_associado_pdv():
        try:
            data = AssociadoPdvModel.objects.all()
            return True, data
        except Exception as e:
            return False, str(e)

    @staticmethod
    def create_associado_pdv(data):
        try:
            usuario = UsuarioModel.objects.get(id_usuario=data["usuario"])
            pdv = PdvModel.objects.get(id_pdv=data["pdv"])
            associado = AssociadoPdvModel.objects.create(
                usuario=usuario,
                pdv=pdv,
                status_acesso=data.get("status_acesso", True),
            )
            associado.save()
            return True, {"id_associado": associado.id_associado}
        except UsuarioModel.DoesNotExist:
            return False, "Usuário não encontrado"
        except PdvModel.DoesNotExist:
            return False, "PDV não encontrado"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def update_associado_pdv(data):
        try:
            associado = AssociadoPdvModel.objects.get(id_associado=data["id_associado"])
            
            if "status_acesso" in data:
                associado.status_acesso = data["status_acesso"]
            if "usuario" in data:
                associado.usuario = UsuarioModel.objects.get(id_usuario=data["usuario"])
            if "pdv" in data:
                associado.pdv = PdvModel.objects.get(id_pdv=data["pdv"])

            associado.save()
            return True, {"id_associado": associado.id_associado}
        except AssociadoPdvModel.DoesNotExist:
            return False, "AssociadoPDV não encontrado"
        except UsuarioModel.DoesNotExist:
            return False, "Usuário não encontrado"
        except PdvModel.DoesNotExist:
            return False, "PDV não encontrado"
        except Exception as e:
            return False, str(e)


    @staticmethod
    def UsuarioIsAssociadoInPDV(id_usuario, id_pdv):
        try:
            associado = AssociadoPdvModel.objects.get(usuario_id=id_usuario, pdv_id=id_pdv)
            if associado.status_acesso:
                return True, associado
            return False, "Usuário não tem permissão de acesso ao PDV"
        except AssociadoPdvModel.DoesNotExist:
            return False, "Associação não encontrada"
