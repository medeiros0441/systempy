from ..models import MotoboyModel, EntregaModel
from api.user import UserInfo

class MotoboyService:
    @staticmethod
    def listar_motoboys_por_empresa(request):
        id_empresa = UserInfo.get_id_empresa(request, True)
        if id_empresa:
            motoboys = MotoboyModel.objects.filter(empresa_id=id_empresa)
            motoboy_list = [
                {
                    "id_motoboy": motoboy.id_motoboy,
                    "nome": motoboy.nome,
                    "numero": motoboy.numero,
                }
                for motoboy in motoboys
            ]
            return True, motoboy_list, None
        return False, None, "ID da empresa não encontrado"

    @staticmethod
    def create_motoboy(dados, request):
        nome = dados.get("nome")
        numero = dados.get("telefone")
        id_empresa = UserInfo.get_id_empresa(request, True)

        if nome and numero and id_empresa:
            motoboy = MotoboyModel.objects.create(
                nome=nome, numero=numero, empresa_id=id_empresa
            )
            return True, {"id_motoboy": str(motoboy.id_motoboy)}, None
        return False, None, "Dados insuficientes para criar o motoboy"

    @staticmethod
    def update_motoboy(id_motoboy, data, request):
        nome = data.get("nome")
        numero = data.get("numero")
        id_empresa = UserInfo.get_id_empresa(request, True)

        if nome & numero & id_empresa:
            motoboy = MotoboyModel.objects.filter(
                id_motoboy=id_motoboy, empresa_id=id_empresa
            ).first()
            if motoboy:
                motoboy.nome = nome
                motoboy.numero = numero
                motoboy.save()
                return True, None, None
        return False, None, "Motoboy não encontrado ou dados insuficientes"

    @staticmethod
    def delete_motoboy(id_motoboy, request):
        id_empresa = UserInfo.get_id_empresa(request, True)
        if id_empresa:
            motoboy = MotoboyModel.objects.filter(
                id_motoboy=id_motoboy, empresa_id=id_empresa
            ).first()
            if motoboy:
                motoboy.delete()
                return True, None, None
        return False, None, "Motoboy não encontrado"

    @staticmethod
    def get_motoboy_by_venda(id_venda):
        if id_venda:
            try:
                entrega = EntregaModel.objects.get(venda_id=id_venda)
                motoboy = MotoboyModel.objects.filter(
                    id_motoboy=entrega.motoboy_id
                ).first()
                if motoboy:
                    obj = {
                        "id_motoboy": motoboy.id_motoboy,
                        "nome": motoboy.nome,
                        "telefone": motoboy.numero,
                    }
                    return True, obj, None
            except (MotoboyModel.DoesNotExist, EntregaModel.DoesNotExist):
                return False, None, "Motoboy ou Entrega não encontrado"
        return False, None, "ID da venda não fornecido"
