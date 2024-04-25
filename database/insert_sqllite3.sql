-- Active: 1714055861968@@127.0.0.1@3306#app_empresa

'insert' INTO app_empresa (id, id_empresa, nome_empresa, nro_cnpj, razao_social, descricao, nome_responsavel, cargo, email, nro_cpf, telefone, 'insert', update_date) VALUES
('83cf0be8-9254-4107-8c0b-2666f89c87d7', 1, 'Samuel', '02.727.617/0001-39', 'Medeiros', NULL, 'Samuel', 'Desenvolvedor', 'medeiros0441@gmail.com', '493.287.378-69', '+55 (11) 9714-86656', '2024-03-12 19:50:20.122873', NULL),
('759f4615-e144-48f4-9aa8-b325f55f6b67', 2, 'Samuel medeiro Test', '00.000.000/0001-91', NULL, 'Samuel medeiros', 'Desenvolvedor', 'medeiros0442@gmail.com', '493.287.378-69', '+55 (11) 9764-09455', '2024-04-14 15:43:24.701358', NULL),
('106a0460-b7e9-4563-9687-691054209621', 3, 'Samuel medeiro Test', '04.252.011/0001-10', NULL, 'Samuel medeiros', 'Desenvolvedor', 'medeiros044122@gmail.com', '123.456.789-09', '+55 (11) 9764-09455', '2024-04-14 15:50:02.443005', NULL),
('a34437a6-e860-4a34-8a8b-4977c9c3e166', 4, 'Samuel medeiro Test', '21.098.765/0001-99', 'ASA', NULL, NULL, NULL, NULL, NULL, NULL, '2024-04-14 16:04:41.681823', NULL),
('a128d375-ce11-4d1a-86da-3df26b3b1661', 5, 'Samuel medeiro Test', '23.456.789/0001-22', 'SAmuel medeiros TEste', NULL, 'Samuel medeiros', 'Desenvolvedor', 'medeiros0441122@gmail.com', '123.456.789-09', '+55 (11) 9764-09455', '2024-04-14 16:15:56.771899', NULL),
('927625e0-c49c-416f-b6fa-7244ef345803', 6, 'Samuel medeiro Test', '98.765.432/0001-21', 'astesty', NULL, 'Samuel medeiros', 'Desenvolvedor', 'awreq2@gmail.com', '323.367.328-07', '+55 (11) 9764-09455', '2024-04-14 16:24:03.753662', NULL),
('16ac1e35-c493-4442-b286-72e3466f7ae9', 7, 'Samuel medeiro Test', '98.765.432/0001-21', 'astesty', NULL, 'Samuel medeiros', 'Desenvolvedor', 'awreq2@gmail.com', '323.367.328-07', '+55 (11) 9764-09455', '2024-04-14 16:26:45.611685', NULL);
'insert' INTO app_endereco (id_endereco, id, rua, numero, bairro, cidade, estado, codigo_postal, descricao, 'insert', update_date) VALUES
(1, 'a770ac1f-b678-4688-9508-63dac2f06130', 'Rua Gil', '21', 'Jardim Matarazzo', 'São Paulo', 'SP', '03813-230', NULL, '2024-03-17 13:30:43.081499', NULL),
(2, '6b67bae9-ab90-4afc-8248-e6ca992b1d61', 'Rua Gil', '21', 'Jardim Matarazzo', 'São Paulo', 'SP', '03813-230', NULL, '2024-03-17 13:40:31.59206', NULL),
(3, '94e00f42-ddf2-45f0-a4cf-7a5137f76bc6', 'Rua Gil', '21', 'Jardim Matarazzo', 'São Paulo', 'SP', '03813-230', NULL, '2024-04-08 16:45:33.470678', NULL),
(4, '942a5260-137f-4e05-97d6-6fd23b540688', 'Rua Gil', '21', 'Jardim Matarazzo', 'São Paulo', 'SP', '03813-230', NULL, '2024-04-08 20:00:19.581673', NULL),
(5, '2b04ae9f-58ca-43f6-bbb5-14203874b07b', 'Rua Gil', '21', 'Jardim Matarazzo', 'São Paulo', 'SP', '03813-230', NULL, '2024-04-08 20:00:55.66022', NULL),
(6, '7674607e-c387-434c-833d-7d69babf0877', 'Rua Gil', '21', 'Jardim Matarazzo', 'São Paulo', 'SP', '03813-230', NULL, '2024-04-08 20:04:21.783872', NULL),
(7, '785761db-cc88-4361-a038-595e9fb36057', 'Rua Gil', '21', 'Jardim Matarazzo', 'São Paulo', 'SP', '03813-230', NULL, '2024-04-08 20:05:37.80749', NULL),
(8, 'a4656309-120d-4775-92a4-82f6856f6798', 'Rua Gil', '21', 'Jardim Matarazzo', 'São Paulo', 'SP', '03813-230', NULL, '2024-04-08 20:06:26.222048', NULL),
(9, '4518a04e-09b9-4d0b-8ef0-9a1fd85e3da8', 'Avenida Tucuruvi', '248', 'Tucuruvi', 'São Paulo', 'SP', '02304-000', NULL, '2024-04-09 16:04:06.642515', NULL),
(10, '774a8368-85ad-441e-8c10-648f9565cec8', 'Rua Santa Eliza', '21', NULL, 'Sp', NULL, '45645-354', NULL, '2024-04-09 17:55:18.350744', NULL),
(11, 'fb08f090-cb80-4727-be3f-a39059232d0c', NULL, NULL, NULL, NULL, NULL, NULL, 'test', '2024-04-09 18:57:22.336126', NULL),
(12, 'ee66ab1f-d038-4eb0-a646-81e85f365b28', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2024-04-10 15:54:27.310401', NULL);
'insert' INTO app_loja (id_loja, nome_loja, numero_telefone, horario_operacao_inicio, horario_operacao_fim, segunda, terca, quarta, quinta, sexta, sabado, domingo, 'insert', update_date, empresa_id, endereco_id) VALUES
(1, 'Loja BarraMansa', '+55 (11) 9714-86656', '09:00:00', '18:00:00', 't', 't', 't', 't', 't', 't', 't', '2024-03-17 13:30:43.079385', '2024-03-17 13:30:43.079422', 1, 1),
(2, 'loja 1', '+55 (11) 1897-48948', '00:00:00', '00:00:00', 't', 'f', 'f', 'f', 'f', 'f', 'f', '2024-03-17 13:40:31.590117', '2024-03-17 13:40:31.590153', 1, 2);
'insert' INTO app_associado (id_associado, 'insert', update_date, status_acesso, loja_id, usuario_id) VALUES
('d04c0a2e-7445-472c-a470-f90c9d6c93de', '2024-03-18 15:19:37.109219', '2024-03-18 15:19:37.109517', 't', 1, 18),
('8fbccad2-a1e9-490d-bae4-6e69746f0d7f', '2024-03-18 15:19:44.870375', '2024-03-18 15:19:44.870411', 't', 2, 18),
('c3836142-e899-453b-ae20-9e309b77d3fc', '2024-03-18 15:54:22.639309', '2024-03-18 15:54:22.639366', 't', 1, 22),
('aa9b3e70-1402-4dec-be53-c354d99dc5f1', '2024-03-18 15:54:33.32822', '2024-03-18 15:54:33.330361', 't', 2, 22),
('d0945daa-93ba-4534-8350-3c27043e84ec', '2024-03-25 19:32:53.256763', '2024-03-27 19:26:35.388626', 't', 1, 1),
('78f0ce5d-8a9f-499e-9741-2355e8c6b50e', '2024-03-25 19:32:53.430819', '2024-03-27 19:26:37.315898', 't', 2, 1);
