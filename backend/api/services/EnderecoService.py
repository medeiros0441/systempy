# EnderecoService.py
from models import Cliente, Endereco
from serializers import ClienteSerializer, EnderecoSerializer

class EnderecoService:
    @staticmethod
    def create_endereco(endereco_data):
        try:
            endereco_serializer = EnderecoSerializer(data=endereco_data)
            if endereco_serializer.is_valid():
                endereco = endereco_serializer.save()
                return endereco, True, "Endereço criado com sucesso."
            return None, False, endereco_serializer.errors
        except Exception as e:
            return None, False, str(e)

    @staticmethod
    def update_endereco(endereco_id, endereco_data):
        try:
            endereco = Endereco.objects.get(pk=endereco_id)
            endereco_serializer = EnderecoSerializer(endereco, data=endereco_data, partial=True)
            if endereco_serializer.is_valid():
                endereco = endereco_serializer.save()
                return endereco, True, "Endereço atualizado com sucesso."
            return None, False, endereco_serializer.errors
        except Endereco.DoesNotExist:
            return None, False, "Endereço não encontrado."
        except Exception as e:
            return None, False, str(e)