class Alerta:
    _mensagem = None

    @staticmethod
    def set_mensagem(mensagem):
        Alerta._mensagem = mensagem

    @staticmethod
    def get_mensagem():
        mensagem = Alerta._mensagem
        Alerta._mensagem = None  # Limpa a mensagem após ser lida
        return mensagem
