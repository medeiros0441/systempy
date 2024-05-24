from django.contrib import admin
from .models import (
    Usuario,
    Empresa,
    Endereco,
    Galao,
    GestaoGalao,
    Loja,
    Associado,
    Produto,
    Sessao,
    Venda,
    ItemCompra,
    Motoboy,
    Caixa,
    Transacao,
    Entrega,
    Historico,
    Log,
    Configuracao,
    Cliente,
)


class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "nome_completo",
        "nome_usuario",
        "email",
        "nivel_usuario",
        "status_acesso",
    )
    list_filter = ("nivel_usuario", "status_acesso")
    search_fields = ("nome_completo", "nome_usuario", "email")


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nome_empresa", "email", "nro_cnpj")
    search_fields = ("nome_empresa", "email")
    list_filter = ("nome_empresa",)


class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "telefone",
        "ultima_compra",
        "insert",
        "update",
        "tipo_cliente",
        "descricao",
        "endereco",
        "empresa",
    )
    list_filter = ("ultima_compra", "tipo_cliente", "empresa")
    search_fields = ["nome", "telefone", "descricao"]
    readonly_fields = ("insert", "update")


class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "codigo",
        "titulo",
        "descricao",
        "descricao_interna",
        "insert",
        "update",
        "status_acesso",
    )
    list_filter = ("usuario", "status_acesso")
    search_fields = ["codigo", "titulo", "descricao", "descricao_interna"]
    readonly_fields = ("insert", "update")


class EnderecoAdmin(admin.ModelAdmin):
    list_display = (
        "rua",
        "numero",
        "bairro",
        "cidade",
        "estado",
        "codigo_postal",
        "descricao",
        "insert",
        "update",
    )
    list_filter = ("cidade", "estado")
    search_fields = ["rua", "bairro", "cidade", "estado", "codigo_postal", "descricao"]
    readonly_fields = ("insert", "update")


class GalaoAdmin(admin.ModelAdmin):
    list_display = (
        "data_validade",
        "data_fabricacao",
        "descricao",
        "quantidade",
        "titulo",
        "insert",
        "update",
        "loja",
    )
    list_filter = ("data_validade", "data_fabricacao", "quantidade", "loja")
    search_fields = ["descricao", "titulo"]
    readonly_fields = ("insert", "update")


class GestaoGalaoAdmin(admin.ModelAdmin):
    list_display = (
        "galao_saiu",
        "galao_entrando",
        "venda",
        "insert",
        "update",
        "descricao",
    )
    list_filter = ("galao_saiu", "galao_entrando", "venda")
    search_fields = ["descricao"]
    readonly_fields = ("insert", "update")


class HistoricoAdmin(admin.ModelAdmin):
    list_display = ("descricao", "insert", "update", "usuario")
    list_filter = ("usuario",)
    search_fields = ["descricao"]
    readonly_fields = ("insert", "update")


class LogAdmin(admin.ModelAdmin):
    list_display = (
        "tipo",
        "origem",
        "descricao",
        "insert",
        "update",
        "usuario",
        "ip_usuario",
    )
    list_filter = ("tipo", "origem", "usuario")
    search_fields = ["tipo", "origem", "descricao", "ip_usuario"]
    readonly_fields = ("insert", "update")


class LojaAdmin(admin.ModelAdmin):
    list_display = (
        "nome_loja",
        "numero_telefone",
        "horario_operacao_inicio",
        "horario_operacao_fim",
        "segunda",
        "terca",
        "quarta",
        "quinta",
        "sexta",
        "sabado",
        "domingo",
        "insert",
        "update",
        "empresa",
        "endereco",
    )
    list_filter = (
        "empresa",
        "segunda",
        "terca",
        "quarta",
        "quinta",
        "sexta",
        "sabado",
        "domingo",
    )
    search_fields = ["nome_loja", "numero_telefone"]
    readonly_fields = ("insert", "update")


class AssociadoAdmin(admin.ModelAdmin):
    list_display = ("insert", "update", "status_acesso", "usuario", "loja")
    list_filter = ("status_acesso", "usuario", "loja")
    readonly_fields = ("insert", "update")


class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "quantidade_atual_estoque",
        "quantidade_minima_estoque",
        "codigo",
        "is_retornavel",
        "status",
        "data_validade",
        "insert",
        "update",
        "preco_compra",
        "preco_venda",
        "fabricante",
        "descricao",
        "loja",
    )
    list_filter = ("is_retornavel", "status", "loja")
    search_fields = ["nome", "codigo", "fabricante"]
    readonly_fields = ("insert", "update")


class SessaoAdmin(admin.ModelAdmin):
    list_display = (
        "ip_sessao",
        "descricao",
        "pagina_atual",
        "time_iniciou",
        "status",
        "insert",
        "update",
        "cidade",
        "regiao",
        "pais",
        "codigo_postal",
        "organizacao",
        "usuario",
    )
    list_filter = ("status", "cidade", "pais", "usuario")
    search_fields = ["ip_sessao", "descricao", "pagina_atual"]
    readonly_fields = ("insert", "update")


class VendaAdmin(admin.ModelAdmin):
    list_display = (
        "data_venda",
        "forma_pagamento",
        "estado_transacao",
        "metodo_entrega",
        "desconto",
        "valor_total",
        "valor_entrega",
        "valor_pago",
        "troco",
        "insert",
        "update",
        "descricao",
        "usuario",
        "loja",
        "cliente",
        "nota_fiscal",
    )
    list_filter = (
        "forma_pagamento",
        "estado_transacao",
        "metodo_entrega",
        "usuario",
        "loja",
        "cliente",
    )
    search_fields = [
        "forma_pagamento",
        "estado_transacao",
        "metodo_entrega",
        "descricao",
    ]
    readonly_fields = ("insert", "update")


class ItemCompraAdmin(admin.ModelAdmin):
    list_display = (
        "venda",
        "produto",
        "quantidade",
        "valor_unidade",
        "insert",
        "update",
    )
    list_filter = ("venda", "produto")
    search_fields = ["venda__id", "produto__nome"]
    readonly_fields = ("insert", "update")


class MotoboyAdmin(admin.ModelAdmin):
    list_display = ("nome", "numero", "insert", "update", "empresa")
    list_filter = ("empresa",)
    search_fields = ["nome", "numero"]
    readonly_fields = ("insert", "update")


class EntregaAdmin(admin.ModelAdmin):
    list_display = (
        "venda",
        "valor_entrega",
        "time_pedido",
        "time_finalizacao",
        "insert",
        "update",
        "motoboy",
        "descricao",
    )
    list_filter = ("time_pedido", "time_finalizacao", "motoboy")
    search_fields = ["descricao"]
    readonly_fields = ("insert", "update")


class CaixaAdmin(admin.ModelAdmin):
    list_display = ("loja", "dia", "insert", "update", "saldo_inicial", "saldo_final")
    list_filter = ("loja",)
    search_fields = ["dia"]
    readonly_fields = ("insert", "update")


class TransacaoAdmin(admin.ModelAdmin):
    list_display = ("caixa", "venda", "valor", "descricao", "insert", "update")
    list_filter = ("caixa", "venda")
    search_fields = ["descricao"]
    readonly_fields = ("insert", "update")


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Sessao, SessaoAdmin)
admin.site.register(Venda, VendaAdmin)
admin.site.register(ItemCompra, ItemCompraAdmin)
admin.site.register(Motoboy, MotoboyAdmin)
admin.site.register(Entrega, EntregaAdmin)
admin.site.register(Caixa, CaixaAdmin)
admin.site.register(Transacao, TransacaoAdmin)
admin.site.register(Historico, HistoricoAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Loja, LojaAdmin)
admin.site.register(Associado, AssociadoAdmin)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Galao, GalaoAdmin)
admin.site.register(GestaoGalao, GestaoGalaoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Configuracao, ConfiguracaoAdmin)
# Registrando as classes Admin

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Empresa, EmpresaAdmin)
