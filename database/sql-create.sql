-- Criação da tabela empresa_cliente
CREATE TABLE smw_empresa(  
    id_empresa int PRIMARY KEY IDENTITY(1, 1),
    nome_empresa TEXT NOT NULL,
    nro_cnpj_empresa TEXT NOT NULL,
    razao_social_empresa TEXT not null,
    descricao_empresa TEXT NOT NULL,
    nome_responsavel TEXT NOT NULL,
    cargo_responsavel TEXT NOT NULL,
    email_responsavel TEXT NOT NULL,
    nro_cpf_responsavel TEXT NOT NULL,
    telefone_responsavel TEXT NOT NULL,
    date_time_insert DATETIME NOT NULL,
    date_time_update DATETIME  NULL
);

-- Criação da tabela app_usuario com a chave estrangeira fk_empresa
CREATE TABLE smw_usuario (
    id_usuario int PRIMARY KEY IDENTITY(1, 1),
    nome_completo VARCHAR(255) NOT NULL,
    nome_usuario VARCHAR(50) NOT NULL,
    senha VARCHAR(50) NOT NULL,
    date_time_insert DATETIME not NULL,
    date_time_update DATETIME NULL,
    nivel_usuario INTEGER NOT NULL,
    status_acesso VARCHAR(20) not NULL,
    email VARCHAR(255) not NULL,
    ultimo_login DATETIME NULL,
    fk_empresa INTEGER NOT NULL FOREIGN KEY (fk_empresa) REFERENCES smw_empresa (id_empresa)
)

CREATE TABLE smw_sessao_usuario (
    id_sessao  int PRIMARY KEY IDENTITY(1, 1),
    ip_sessao VARCHAR(100),
    descricao VARCHAR(100),
    pagina_atual VARCHAR(200),
    time_iniciou DATETIME DEFAULT CURRENT_TIMESTAMP,
    time_finalizou DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN null,
    date_time_insert DATETIME not NULL,
    date_time_update DATETIME NULL,
    fk_usuario INT not null   FOREIGN KEY (fk_usuario) REFERENCES usuario(id_usuario)
);

-- Tabela produto

CREATE TABLE [smw_loja] (
  [id_loja] int PRIMARY KEY IDENTITY(1, 1),
  [nome_loja] varchar(255) NOT NULL,
  [endereco] varchar(255),
  [numero_telefone] varchar(15), 
  [horario_operacao] varchar(50),
  [fk_empresa] int FOREIGN KEY ([fk_empresa]) REFERENCES [smw_empresa] ([id_empresa]),
   [date_time_insert] DATETIME not NULL,
    [date_time_update] DATETIME NULL,
)
CREATE TABLE smw_produto (
  id_produto int PRIMARY KEY IDENTITY,
  nome_produto varchar(255) NOT NULL,
  quantidade_estoque int,
  tipo_produto int,
  date_time_insert DATETIME not NULL,
  date_time_update DATETIME null,
  preco_compra decimal(10, 2),
  preco_venda decimal(10, 2),
  fabricante varchar(100),
  descricao text,
  fk_loja int FOREIGN KEY REFERENCES smw_loja(id_loja)
);

CREATE TABLE smw_endereco (
  id_endereco int PRIMARY KEY IDENTITY(1, 1),
  rua varchar(255) NOT NULL,
  numero varchar(10),
  cidade varchar(100) NOT NULL,
  estado varchar(50) NOT NULL,
  codigo_postal varchar(15) NOT NULL,
  descricao text,
  date_time_insert DATETIME not NULL,
  date_time_update DATETIME NULL
);

 
CREATE TABLE smw_cliente (
    id_cliente int PRIMARY KEY IDENTITY(1, 1),
    nome_cliente varchar(255) NOT NULL,
    telefone varchar(20) not null,
    ultima_compra date not null,
    date_time_insert DATETIME not NULL,
    date_time_update DATETIME NULL,
    tipo_cliente varchar(50) not null,
    fk_endereco int FOREIGN KEY REFERENCES smw_endereco(id_endereco)
);

-- Tabela venda
CREATE TABLE smw_venda (
  id_venda int PRIMARY KEY IDENTITY,
  data_venda date,
  valor_total decimal(10, 2),
  forma_pagamento varchar(50),
  tipo_venda varchar(20),
  date_time_insert DATETIME not NULL,
  date_time_update DATETIME NULL,
  descricao text,
  fk_usuario int FOREIGN KEY REFERENCES smw_usuario(id_usuario),
  fk_loja int FOREIGN KEY REFERENCES smw_loja(id_loja),
  fk_cliente int FOREIGN KEY REFERENCES smw_cliente(id_cliente)
);


CREATE TABLE [smw_venda_produto] (
  [id_venda_produto] int PRIMARY KEY IDENTITY(1, 1),
  [fk_venda] int,
  [fk_produto] int,
  [quantidade] int,
    date_time_insert DATETIME not NULL,
    date_time_update DATETIME NULL,
  FOREIGN KEY ([fk_venda]) REFERENCES [smw_venda] ([id_venda]),
  FOREIGN KEY ([fk_produto]) REFERENCES [smw_produto] ([id_produto])
)
 


CREATE TABLE [smw_Galao] (
  [id_galao] int PRIMARY KEY IDENTITY(1, 1),
   [date_time_insert] DATETIME not NULL,
    [date_time_update] DATETIME NULL,
  [data_validade] varchar(50),
  [data_fabricacao] varchar(50),
  [descricao] text
) 
CREATE TABLE [smw_GestaoGalao] (
  [id_gestao_galao] int PRIMARY KEY IDENTITY(1, 1),
  [fk_galao_saiu] int FOREIGN KEY REFERENCES [smw_Galao] ([id_galao]),
  [fk_galao_entrando] int FOREIGN KEY ([fk_galao_entrando]) REFERENCES [smw_Galao] ([id_galao]),
  [fk_cliente] int FOREIGN KEY ([fk_cliente]) REFERENCES [smw_cliente] ([id_cliente]),
  [fk_venda] int  FOREIGN KEY ([fk_venda]) REFERENCES [smw_venda] ([id_venda]),
  [date_time_insert] DATETIME not NULL,
    [date_time_update] DATETIME NULL,
)
 
-- Tabela tb_plano_gestao
CREATE TABLE [smw_plano_gestao] (
  id_plano_gestao int PRIMARY KEY IDENTITY,
  nome_plano_gestao varchar(100) NOT NULL,
  descricao_plano_gestao varchar(500),
  preco_plano_gestao decimal(10, 2) NOT NULL,
  duracao_meses_plano_gestao int NOT NULL,
  status_plano_gestao bit NOT NULL DEFAULT 1,
   [date_time_insert] DATETIME not NULL,
    [date_time_update] DATETIME NULL,
);

-- Tabela tb_inscricao_gestao
CREATE TABLE smw_inscricao_gestao (
  id_inscricao_gestao int PRIMARY KEY IDENTITY,
  nome_inscricao varchar(50) NOT NULL,
  descricao_inscricao varchar(255) NOT NULL,
  preco_inscricao float NOT NULL,
  periodo_faturamento_inscricao int NOT NULL,
  status_inscricao bit NOT NULL,
   date_time_insert DATETIME not NULL,
    date_time_update DATETIME NULL,
  fk_plano_gestao int NOT NULL FOREIGN KEY REFERENCES smw_plano_gestao(id_plano_gestao),
  fk_empresa int NOT NULL FOREIGN KEY REFERENCES smw_empresa(id_empresa)
);

-- Tabela tb_historico_cliente
CREATE TABLE smw_historico_cliente (
  id_historico_cliente int PRIMARY KEY IDENTITY,
  id_empresa int NOT NULL FOREIGN KEY REFERENCES smw_empresa(id_empresa),
  data_evento datetime2 NOT NULL,
  descricao_evento varchar(500) NOT NULL,
  date_time_insert DATETIME not NULL,
    date_time_update DATETIME NULL,
);
CREATE TABLE smw_configuracao_plataforma (
  id_configuracao_plataforma int PRIMARY KEY IDENTITY,
  nome_configuracao_plataforma varchar(100) NOT NULL,
  valor_configuracao_plataforma varchar(500) NOT NULL,
  status_configuracao_plataforma bit NOT NULL,
  descricao_configuracao_plataforma varchar(500) NOT NULL,
  date_time_insert DATETIME not NULL,
    date_time_update DATETIME NULL,
  fk_empresa int NOT NULL FOREIGN KEY REFERENCES smw_empresa(id_empresa)
);
-- Tabela tb_sessao
CREATE TABLE smw_sessao (
  id_sessao int PRIMARY KEY,
  hora_inicio_sessao datetime2 NOT NULL,
  hora_fim_sessao datetime2,
  navegador_sessao varchar(255) NOT NULL,
  status_sessao bit NOT NULL,
  date_time_insert DATETIME not NULL,
    date_time_update DATETIME NULL,
);

-- Tabela tb_registro
CREATE TABLE smw_registro (
  id_registro int PRIMARY KEY,
  texto nvarchar(max) NOT NULL,
  codigo_localidade_texto nvarchar(max) NOT NULL,
  sistema_texto nvarchar(max) NOT NULL,
  nivel varchar(max) NOT NULL,
  id_sessao int NOT NULL,
  date_time_insert DATETIME not NULL,
  date_time_update DATETIME NULL,
  fk_sessao int FOREIGN KEY REFERENCES smw_sessao(id_sessao)
);
