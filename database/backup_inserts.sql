--
-- PostgreSQL database dump
--

-- Dumped from database version 15.5
-- Dumped by pg_dump version 16.2 (Ubuntu 16.2-1.pgdg22.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: app_empresa; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_empresa (id, id_empresa, nome_empresa, nro_cnpj, razao_social, descricao, nome_responsavel, cargo, email, nro_cpf, telefone, insert, update) FROM stdin;
83cf0be8-9254-4107-8c0b-2666f89c87d7	1	Samuel	02.727.617/0001-39	Medeiros 	\N	Samuel	Desenvolvedor	medeiros0441@gmail.com	493.287.378-69	+55 (11) 9714-86656	2024-03-12 19:50:20.122873+00	\N
759f4615-e144-48f4-9aa8-b325f55f6b67	2	 Samuel medeiro Test	00.000.000/0001-91	medeiros0442@gmail.com	\N	Samuel medeiros 	Desenvolvedor	medeiros0442@gmail.com	493.287.378-69	+55 (11) 9764-09455	2024-04-14 15:43:24.701358+00	\N
106a0460-b7e9-4563-9687-691054209621	3	 Samuel medeiro Test	04.252.011/0001-10	medeiros01441@gmail.com	\N	Samuel medeiros 	Desenvolvedor	medeiros044122@gmail.com	123.456.789-09	+55 (11) 9764-09455	2024-04-14 15:50:02.443005+00	\N
a34437a6-e860-4a34-8a8b-4977c9c3e166	4	 Samuel medeiro Test	21.098.765/0001-99	ASA	\N						2024-04-14 16:04:41.681823+00	\N
a128d375-ce11-4d1a-86da-3df26b3b1661	5	 Samuel medeiro Test	23.456.789/0001-22	SAmuel medeiros TEste	\N	Samuel medeiros 	Desenvolvedor	medeiros0441122@gmail.com	123.456.789-09	+55 (11) 9764-09455	2024-04-14 16:15:56.771899+00	\N
927625e0-c49c-416f-b6fa-7244ef345803	6	 Samuel medeiro Test	98.765.432/0001-21	 astesty	\N	Samuel medeiros 	Desenvolvedor	awreq2@gmail.com	323.367.328-07	+55 (11) 9764-09455	2024-04-14 16:24:03.753662+00	\N
16ac1e35-c493-4442-b286-72e3466f7ae9	7	 Samuel medeiro Test	98.765.432/0001-21	 astesty	\N	Samuel medeiros 	Desenvolvedor	awreq2@gmail.com	323.367.328-07	+55 (11) 9764-09455	2024-04-14 16:26:45.611685+00	\N
\.


--
-- Data for Name: app_endereco; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_endereco (id_endereco, id, rua, numero, bairro, cidade, estado, codigo_postal, descricao, insert, update) FROM stdin;
1	a770ac1f-b678-4688-9508-63dac2f06130	Rua Gil	21	Jardim Matarazzo	São Paulo	SP	03813-230		2024-03-17 13:30:43.081499+00	\N
2	6b67bae9-ab90-4afc-8248-e6ca992b1d61	Rua Gil	21	Jardim Matarazzo	São Paulo	SP	03813-230		2024-03-17 13:40:31.59206+00	\N
3	94e00f42-ddf2-45f0-a4cf-7a5137f76bc6	Rua Gil	21	Jardim Matarazzo	São Paulo	SP	03813-230	{}	2024-04-08 16:45:33.470678+00	\N
4	942a5260-137f-4e05-97d6-6fd23b540688	Rua Gil	21	Jardim Matarazzo	São Paulo	SP	03813-230	{}	2024-04-08 20:00:19.581673+00	\N
5	2b04ae9f-58ca-43f6-bbb5-14203874b07b	Rua Gil	21	Jardim Matarazzo	São Paulo	SP	03813-230	{}	2024-04-08 20:00:55.66022+00	\N
6	7674607e-c387-434c-833d-7d69babf0877	Rua Gil	21	Jardim Matarazzo	São Paulo	SP	03813-230	{}	2024-04-08 20:04:21.783872+00	\N
7	785761db-cc88-4361-a038-595e9fb36057	Rua Gil	21	Jardim Matarazzo	São Paulo	SP	03813-230	{}	2024-04-08 20:05:37.80749+00	\N
8	a4656309-120d-4775-92a4-82f6856f6798	Rua Gil	21	Jardim Matarazzo	São Paulo	SP	03813-230	{}	2024-04-08 20:06:26.222048+00	\N
9	4518a04e-09b9-4d0b-8ef0-9a1fd85e3da8	Avenida Tucuruvi	248	Tucuruvi	São Paulo	SP	02304-000	{}	2024-04-09 16:04:06.642515+00	\N
10	774a8368-85ad-441e-8c10-648f9565cec8	Rua Santa Eliza	21			Sp	45645-354	{}	2024-04-09 17:55:18.350744+00	\N
11	fb08f090-cb80-4727-be3f-a39059232d0c							test	2024-04-09 18:57:22.336126+00	\N
12	ee66ab1f-d038-4eb0-a646-81e85f365b28								2024-04-10 15:54:27.310401+00	\N
\.


--
-- Data for Name: app_loja; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_loja (id_loja, nome_loja, numero_telefone, horario_operacao_inicio, horario_operacao_fim, segunda, terca, quarta, quinta, sexta, sabado, domingo, insert, update, empresa_id, endereco_id) FROM stdin;
1	Loja BarraMansa	+55 (11) 9714-86656	09:00:00	18:00:00	t	t	t	t	t	t	t	2024-03-17 13:30:43.079385+00	2024-03-17 13:30:43.079422+00	1	1
2	loja 1	+55 (11) 1897-48948	00:00:00	00:00:00	t	f	f	f	f	f	f	2024-03-17 13:40:31.590117+00	2024-03-17 13:40:31.590153+00	1	2
\.


--
-- Data for Name: app_usuario; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_usuario (id, id_usuario, nome_completo, nome_usuario, senha, insert, update, nivel_usuario, status_acesso, email, ultimo_login, empresa_id) FROM stdin;
4f4df81c-160b-4765-91ff-1145ba9813ea	1	Samuel	Samuel8038	pbkdf2_sha256$720000$OcjUb37QgW1D1PxGUkkFSe$xODG7uo2RCXyUTiBlR8n4mUFtCoPxMSht/zZIMN3uSw=	2024-03-12 19:50:23.383559+00	2024-03-27 19:46:11.093877+00	1	t	medeiros0441@gmail.com	2024-04-14 19:53:23.709355+00	1
73825e71-5c68-4784-8ff9-3885c5d5f501	18	Samuel M	samuelm	pbkdf2_sha256$720000$P0hhacDfPN2dIp2caGlq6H$Rl9a+KuCKdTmH+Qktbx2dz7hfe5QshJEsWzimisvm/Q=	2024-03-16 17:26:39.864099+00	2024-03-18 19:55:42.545005+00	2	t	sasa@gmail.com	\N	1
f9439d76-8bc6-4a92-883f-000914ec8aaf	22	sam	sam	pbkdf2_sha256$720000$IwqFlw9MLO2C2GP2uqI7I5$MN2MlTifwvV4vZbWpXZ+IIcY5ft/eruD4oGZH5wTvmc=	2024-03-18 15:53:53.925119+00	2024-03-18 19:56:23.621527+00	3	t	medeiros044121@gmail.com	\N	1
f5f7f322-0af4-4827-955e-3dca04a65064	23	Samuel medeiros 	Samuel medeiros 8724	pbkdf2_sha256$720000$ClgtghpbP52R3lGrP72Yg4$gAufdyxfv4uYIYG3hpJffpp2sROJFYXn0zRpbClH5HQ=	2024-04-14 15:43:28.004905+00	\N	1	t	medeiros0442@gmail.com	\N	2
a7f9540e-70e0-489f-ae0b-cf1af7689ccf	24	Samuel medeiros 	Samuel medeiros 9613	pbkdf2_sha256$720000$TqvPvye9tnpWsy7kUkHMIV$DZJPItq6r2yszEJUjPTVZiC33qf4NsdTfQvqJDbUNA0=	2024-04-14 15:50:03.501251+00	\N	1	t	medeiros044122@gmail.com	\N	3
12596d7f-f53a-4fe4-b3b1-75eca92ab8f9	25	Samuel medeiros 	Samuel medeiros 1940	pbkdf2_sha256$720000$3Gk2a5yYL103EPbq9oOoiu$KJZe4p75yJpyJwXmjCPkbG3GPglvSzxny/vutda+nkQ=	2024-04-14 16:17:04.177787+00	\N	1	t	medeiros0441122@gmail.com	\N	5
645b0605-fe39-4a0d-991a-0d484817a0d8	26	Samuel medeiros 	Samuel medeiros 7616	pbkdf2_sha256$720000$h92RdpbidinKbm5h2tNpqt$jKrwATEuY899yqX2YwfzZCusmX1aaTP7fWOr2PaW4Hg=	2024-04-14 16:24:04.594878+00	\N	1	t	awreq2@gmail.com	\N	6
a98b5cc0-57c2-49cc-a071-c2e1bb2b21a3	27	Samuel medeiros 	Samuel medeiros 6065	pbkdf2_sha256$720000$vstNDXW1r7hkVAdmiuSjrh$32NBPpifbbIKBME5AFQ4+SsVjqEBC1VBSe03sr1rah8=	2024-04-14 16:26:50.074951+00	\N	1	t	awreq2@gmail.com	\N	7
\.


--
-- Data for Name: app_associado; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_associado (id_associado, insert, update, status_acesso, loja_id, usuario_id) FROM stdin;
d04c0a2e-7445-472c-a470-f90c9d6c93de	2024-03-18 15:19:37.109219+00	2024-03-18 15:19:37.109517+00	t	1	18
8fbccad2-a1e9-490d-bae4-6e69746f0d7f	2024-03-18 15:19:44.870375+00	2024-03-18 15:19:44.870411+00	t	2	18
c3836142-e899-453b-ae20-9e309b77d3fc	2024-03-18 15:54:22.639309+00	2024-03-18 15:54:22.639366+00	t	1	22
aa9b3e70-1402-4dec-be53-c354d99dc5f1	2024-03-18 15:54:33.32822+00	2024-03-18 15:54:33.330361+00	t	2	22
d0945daa-93ba-4534-8350-3c27043e84ec	2024-03-25 19:32:53.256763+00	2024-03-27 19:26:35.388626+00	t	1	1
78f0ce5d-8a9f-499e-9741-2355e8c6b50e	2024-03-25 19:32:53.430819+00	2024-03-27 19:26:37.315898+00	t	2	1
\.


--
-- Data for Name: app_caixa; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_caixa (id_caixa, insert, update, saldo_inicial, saldo_final, loja_id) FROM stdin;
\.


--
-- Data for Name: app_cliente; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_cliente (id, nome_cliente, telefone_cliente, ultima_compra, insert, update, tipo_cliente, descricao_cliente, empresa_id, endereco_id) FROM stdin;
1	loja 1	+55 (11) 1897-48948	\N	2024-04-08 16:46:09.1075+00	\N	regular		1	3
2	samuel	+55 (11) 1897-48948	\N	2024-04-08 20:00:19.842077+00	\N	ocasional	Trest	1	4
3	samuel	+55 (11) 1897-48948	\N	2024-04-08 20:00:55.814883+00	\N	ocasional	Trest	1	5
4	Samuel	+55 (11) 1897-48948	\N	2024-04-08 20:04:21.937213+00	\N	corporativo		1	6
5	Samuel	+55 (11) 1897-48948	\N	2024-04-08 20:05:37.965258+00	\N	corporativo		1	7
6	loja 1	+55 (11) 1897-48948	\N	2024-04-08 20:06:26.375413+00	\N	corporativo		1	8
7	Cleiton	+55 (11) 9714-86656	\N	2024-04-09 16:04:06.913236+00	\N	ocasional	Test	1	9
8	Wesley	+55 (11) 9317-83187	\N	2024-04-09 17:55:18.54755+00	\N	corporativo	DescricaoCliente	1	10
9	samuel	+55 (11) 9312-39831	\N	2024-04-09 18:57:22.489991+00	\N	corporativo	ates	1	11
10	Julio	+55 (18) 4886-48648	\N	2024-04-10 15:54:27.605143+00	\N	ocasional		1	12
\.


--
-- Data for Name: app_configuracao; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_configuracao (id_configuracao, codigo, titulo, descricao, descricao_interna, insert, update, status_acesso, usuario_id) FROM stdin;
bd4f17ab-e5eb-4b07-85d6-b47b668f1dfd	1	Gerenciamento de Usuario	Permitir acesso ao Painel de Usuario, isso inclui criar, editar, remover, entre outros.	Controle de usuario, editar, alterar, criar...	2024-03-14 18:43:08.499249+00	2024-03-14 18:43:08.499283+00	t	1
aabc3175-6585-4d88-9413-b37792586e96	2	Gerenciamento de Empresa	Permitir acesso ao Painel de Empresa, isso inclui criar, editar, remover, entre outros.	Controle de empresa, editar, alterar, criar...	2024-03-14 18:43:08.682183+00	2024-03-14 18:43:08.68222+00	t	1
f562ebdf-5ea7-471f-bad9-7def4b4a72d1	3	Gerenciamento de Endereco	Permitir acesso ao Painel de Endereco, isso inclui criar, editar, remover, entre outros.	Controle de endereco, editar, alterar, criar...	2024-03-14 18:43:08.845387+00	2024-03-14 18:43:08.845426+00	t	1
1a9e21b7-504c-44f9-ba1f-b1746db321c5	4	Gerenciamento de Galao	Permitir acesso ao Painel de Galao, isso inclui criar, editar, remover, entre outros.	Controle de galao, editar, alterar, criar...	2024-03-14 18:43:09.009118+00	2024-03-14 18:43:09.009155+00	t	1
6164d5b7-8ac8-4868-a4ab-99972895ef41	5	Gerenciamento de Loja	Permitir acesso ao Painel de Loja, isso inclui criar, editar, remover, entre outros.	Controle de loja, editar, alterar, criar...	2024-03-14 18:43:09.172163+00	2024-03-14 18:43:09.172199+00	t	1
c2bc117a-1b89-4a38-8213-87e1ca199603	6	Gerenciamento de Produto	Permitir acesso ao Painel de Produto, isso inclui criar, editar, remover, entre outros.	Controle de produto, editar, alterar, criar...	2024-03-14 18:43:09.337409+00	2024-03-14 18:43:09.337487+00	t	1
a8114cc0-1910-442b-8432-b8181c731ee2	7	Gerenciamento de Venda	Permitir acesso ao Painel de Venda, isso inclui criar, editar, remover, entre outros.	Controle de venda, editar, alterar, criar...	2024-03-14 18:43:09.501357+00	2024-03-14 18:43:09.501395+00	t	1
8700d836-e3d1-432d-8a08-658945c477df	8	Gerenciamento de Cliente	Permitir acesso ao Painel de Cliente, isso inclui criar, editar, remover, entre outros.	Controle de cliente, editar, alterar, criar...	2024-03-14 18:43:09.669838+00	2024-03-14 18:43:09.669876+00	t	1
e1c1f03e-9398-408e-b34c-324daa17fb2e	2	Gerenciamento de Empresa	Permitir acesso ao Painel de Empresa, isso inclui criar, editar, remover, entre outros.	Controle de empresa, editar, alterar, criar...	2024-03-16 20:35:33.442475+00	2024-03-16 20:35:33.442512+00	f	18
ee59dd14-390a-4e6b-955e-282aa7da3105	3	Gerenciamento de Endereco	Permitir acesso ao Painel de Endereco, isso inclui criar, editar, remover, entre outros.	Controle de endereco, editar, alterar, criar...	2024-03-16 20:35:33.750236+00	2024-03-16 20:35:33.750274+00	f	18
1de5f0f8-1447-4461-a69c-cc1dcb2b55b9	4	Gerenciamento de Galao	Permitir acesso ao Painel de Galao, isso inclui criar, editar, remover, entre outros.	Controle de galao, editar, alterar, criar...	2024-03-16 20:35:34.080644+00	2024-03-16 20:35:34.080682+00	f	18
33ed2cb2-efa9-4d21-90e9-42000c4cf93b	5	Gerenciamento de Loja	Permitir acesso ao Painel de Loja, isso inclui criar, editar, remover, entre outros.	Controle de loja, editar, alterar, criar...	2024-03-16 20:35:34.394824+00	2024-03-16 20:35:34.394862+00	f	18
a347bdb8-a7bc-42dc-b400-d7272bf94fa4	6	Gerenciamento de Produto	Permitir acesso ao Painel de Produto, isso inclui criar, editar, remover, entre outros.	Controle de produto, editar, alterar, criar...	2024-03-16 20:35:34.73039+00	2024-03-16 20:35:34.730425+00	f	18
8ce0dcad-b64f-427f-aa80-13889724e5ad	6	Gerenciamento de Produto	Permitir acesso ao Painel de Produto, isso inclui criar, editar, remover, entre outros.	Controle de produto, editar, alterar, criar...	2024-03-18 15:54:39.220035+00	2024-03-18 16:07:11.100537+00	t	22
d776b929-e00a-42fe-b7d8-b6cd7b4055c5	1	Gerenciamento de Usuario	Permitir acesso ao Painel de Usuario, isso inclui criar, editar, remover, entre outros.	Controle de usuario, editar, alterar, criar...	2024-03-16 20:35:33.118133+00	2024-03-16 20:35:33.118171+00	t	18
78abe547-5127-472c-bd6d-bfb3b067bba2	7	Gerenciamento de Venda	Permitir acesso ao Painel de Venda, isso inclui criar, editar, remover, entre outros.	Controle de venda, editar, alterar, criar...	2024-03-16 20:35:35.061317+00	2024-03-16 20:35:35.061354+00	t	18
ed8b1cf0-1aee-4953-aa29-20567fd2d24f	8	Gerenciamento de Cliente	Permitir acesso ao Painel de Cliente, isso inclui criar, editar, remover, entre outros.	Controle de cliente, editar, alterar, criar...	2024-03-16 20:35:35.384245+00	2024-03-16 20:35:35.384281+00	t	18
5ac4fa65-02e2-4a77-8d23-8462d426f5b8	7	Gerenciamento de Venda	Permitir acesso ao Painel de Venda, isso inclui criar, editar, remover, entre outros.	Controle de venda, editar, alterar, criar...	2024-03-18 15:54:39.529947+00	2024-03-18 16:07:11.43367+00	t	22
ac6ffb26-2094-4812-8ccf-3b94016c11df	8	Gerenciamento de Cliente	Permitir acesso ao Painel de Cliente, isso inclui criar, editar, remover, entre outros.	Controle de cliente, editar, alterar, criar...	2024-03-18 15:54:39.84607+00	2024-03-18 16:07:11.761556+00	t	22
5426fede-54e3-44d3-b56e-03d6448a8f20	1	Gerenciamento de Usuario	Permitir acesso ao Painel de Usuario, isso inclui criar, editar, remover, entre outros.	Controle de usuario, editar, alterar, criar...	2024-03-18 15:54:37.660096+00	2024-03-18 15:54:37.660135+00	f	22
801b7602-4037-4e84-8907-839da1dab082	2	Gerenciamento de Empresa	Permitir acesso ao Painel de Empresa, isso inclui criar, editar, remover, entre outros.	Controle de empresa, editar, alterar, criar...	2024-03-18 15:54:37.972728+00	2024-03-18 15:54:37.972766+00	f	22
9ff569cd-d3c6-4f95-a599-aea20be2a52a	3	Gerenciamento de Endereco	Permitir acesso ao Painel de Endereco, isso inclui criar, editar, remover, entre outros.	Controle de endereco, editar, alterar, criar...	2024-03-18 15:54:38.284044+00	2024-03-18 15:54:38.284081+00	f	22
243fc4c6-56e2-4cbb-b11c-1391bcc5f504	4	Gerenciamento de Galao	Permitir acesso ao Painel de Galao, isso inclui criar, editar, remover, entre outros.	Controle de galao, editar, alterar, criar...	2024-03-18 15:54:38.594036+00	2024-03-18 15:54:38.594074+00	f	22
80230db8-be43-4d63-a479-8394e54e184b	5	Gerenciamento de Loja	Permitir acesso ao Painel de Loja, isso inclui criar, editar, remover, entre outros.	Controle de loja, editar, alterar, criar...	2024-03-18 15:54:38.910033+00	2024-03-18 15:54:38.910072+00	f	22
2576f9fd-bf2e-4b16-9dc9-7aa0bad23470	9	\N	\N	\N	2024-04-06 14:08:52.542368+00	\N	t	1
604208f4-048b-4ffa-8273-a52ad52c92b7	1	Gerenciamento de Usuario	Permitir acesso ao Painel de Usuario, isso inclui criar, editar, remover, entre outros.	Controle de usuario, editar, alterar, criar...	2024-04-14 16:27:07.307559+00	2024-04-14 16:27:07.307591+00	t	27
e4c9699a-939c-4bf7-9e65-76e368486f28	2	Gerenciamento de Empresa	Permitir acesso ao Painel de Empresa, isso inclui criar, editar, remover, entre outros.	Controle de empresa, editar, alterar, criar...	2024-04-14 16:27:14.061407+00	2024-04-14 16:27:14.061435+00	t	27
0dd9e5b2-c32d-4528-8b29-90fb2dee382f	3	Gerenciamento de Endereco	Permitir acesso ao Painel de Endereco, isso inclui criar, editar, remover, entre outros.	Controle de endereco, editar, alterar, criar...	2024-04-14 16:27:14.378528+00	2024-04-14 16:27:14.378544+00	t	27
a1b4dfa0-6985-46dc-a3da-fd0b012a5880	4	Gerenciamento de Galao	Permitir acesso ao Painel de Galao, isso inclui criar, editar, remover, entre outros.	Controle de galao, editar, alterar, criar...	2024-04-14 16:27:14.801526+00	2024-04-14 16:27:14.801552+00	t	27
96c7f65b-2b0d-4247-998d-9de57a1dd6b6	5	Gerenciamento de Loja	Permitir acesso ao Painel de Loja, isso inclui criar, editar, remover, entre outros.	Controle de loja, editar, alterar, criar...	2024-04-14 16:27:16.81891+00	2024-04-14 16:27:16.818937+00	t	27
ade1a9a7-ee02-4c26-8ca5-8b04c101e0be	6	Gerenciamento de Produto	Permitir acesso ao Painel de Produto, isso inclui criar, editar, remover, entre outros.	Controle de produto, editar, alterar, criar...	2024-04-14 16:27:17.173908+00	2024-04-14 16:27:17.173934+00	t	27
c60ed14a-49d8-485c-a561-f641849ab415	7	Gerenciamento de Venda	Permitir acesso ao Painel de Venda, isso inclui criar, editar, remover, entre outros.	Controle de venda, editar, alterar, criar...	2024-04-14 16:27:17.49469+00	2024-04-14 16:27:17.494732+00	t	27
8740e24a-fff4-4224-9bf8-2373afa5f59d	8	Gerenciamento de Cliente	Permitir acesso ao Painel de Cliente, isso inclui criar, editar, remover, entre outros.	Controle de cliente, editar, alterar, criar...	2024-04-14 16:27:17.773347+00	2024-04-14 16:27:17.773374+00	t	27
769efc5f-1c7e-4dab-af38-df8e79088016	9	Gerenciamento de Motoboy	Permitir acesso ao Painel de Motoboy, isso inclui criar, editar, remover, entre outros.	Controle de motoboy, editar, alterar, criar...	2024-04-14 16:27:18.187026+00	2024-04-14 16:27:18.187052+00	t	27
f50678cc-9222-4b3a-a9c6-d223bc9dafed	10	Gerenciamento de Caixa	Permitir acesso ao Painel de Caixa, isso inclui criar, editar, remover, entre outros.	Controle de caixa, editar, alterar, criar...	2024-04-14 16:27:18.484311+00	2024-04-14 16:27:18.484337+00	t	27
ed80024a-ba1b-4be0-9839-58a9b7794912	11	Gerenciamento de Transacao	Permitir acesso ao Painel de Transacao, isso inclui criar, editar, remover, entre outros.	Controle de transacao, editar, alterar, criar...	2024-04-14 16:27:18.863284+00	2024-04-14 16:27:18.863316+00	t	27
c652ffcc-b2d2-4731-8484-e0eb560d8ed0	12	Gerenciamento de Faturamento	Permitir acesso ao Painel de Faturamento, isso inclui criar, editar, remover, entre outros.	Controle de faturamento, editar, alterar, criar...	2024-04-14 16:27:19.6988+00	2024-04-14 16:27:19.698826+00	t	27
\.


--
-- Data for Name: app_motoboy; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_motoboy (id_motoboy, nome, numero, insert, update, empresa_id) FROM stdin;
8f6dd070-80c0-4e6c-b6ed-251e000bdc53	loja 1	+5511189748948	2024-04-02 19:31:31.883523+00	2024-04-02 19:31:31.884894+00	1
0b7ba516-dc3f-438d-a375-16b6308e8d83	Samuel	+5511189748948	2024-04-02 19:51:02.040168+00	2024-04-02 19:51:02.057848+00	1
563132a2-22cb-4bdc-a52e-19d7c82cbbd4	loja 1	+5511189748948	2024-04-02 19:55:45.298669+00	2024-04-02 19:55:45.299267+00	1
fa327bd8-bd88-4d98-ab38-53894b1f8062	loja 1	+5511189748948	2024-04-02 19:57:57.783334+00	2024-04-02 19:57:57.78393+00	1
7d36c7b0-6dbf-42dd-b243-f1743c83e049	loja 1	+5511189748948	2024-04-02 20:00:26.230082+00	2024-04-02 20:00:26.230959+00	1
1bc0e816-0fbf-463a-8551-821d2fde0661	Shamuel	11971486656	2024-04-02 20:32:15.650261+00	2024-04-02 20:32:15.651005+00	1
ad042f89-e301-42c3-b59e-41f1ec84ad54	loja 1	+5511189748948	2024-04-04 15:44:45.050953+00	2024-04-04 15:44:45.122317+00	1
\.


--
-- Data for Name: app_entrega; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_entrega (id_entrega, valor_entrega, venda_id, motoboy_id, descricao, insert, time_finalizacao, time_pedido, update) FROM stdin;
\.


--
-- Data for Name: app_galao; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_galao (data_validade, data_fabricacao, descricao, id_galao, insert, update, loja_id, quantidade, titulo) FROM stdin;
\.


--
-- Data for Name: app_gestaogalao; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_gestaogalao (id_gestao_galao, insert, update, cliente_id, galao_entrando_id, galao_saiu_id, venda_id, descricao) FROM stdin;
\.


--
-- Data for Name: app_historico; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_historico (id_historico, descricao, insert, update, usuario) FROM stdin;
\.


--
-- Data for Name: app_log; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_log (id_log, tipo, origem, descricao, insert, update, ip_usuario, usuario_id) FROM stdin;
\.


--
-- Data for Name: app_produto; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_produto (id_produto, nome, quantidade_atual_estoque, quantidade_minima_estoque, insert, update, preco_compra, preco_venda, fabricante, descricao, loja_id, codigo, data_validade, is_retornavel) FROM stdin;
a989d0ab-9fe9-4a17-99d9-33ad6229d923	Bioleve 20L	155	1515	2024-03-19 17:26:58.900085+00	2024-03-19 17:26:58.900118+00	15.00	30.00	3584	\N	2	\N	\N	t
2238ceb8-702d-4e04-aceb-d192abc74238	Lindoia 20L	550	1	2024-03-18 19:59:23.0081+00	2024-03-18 19:59:23.008135+00	6.50	13.00	Lindoia	\N	1	\N	\N	t
75591457-68fa-41ed-b307-190417cc06d3	Fardo 5,10ML	30	5	2024-03-27 18:37:10.28611+00	2024-03-27 18:37:10.286141+00	7.00	17.00	Lindoia	\N	2	\N	\N	f
ed087cf4-ef6a-43a6-b24e-fde06bac8fff	Lindoia 10L	170	13	2024-03-19 16:10:00.919767+00	2024-03-19 16:10:00.919788+00	6.50	14.00	Lindoia	\N	1	\N	\N	t
\.


--
-- Data for Name: app_sessao; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_sessao (id_sessao, ip_sessao, descricao, pagina_atual, time_iniciou, status, insert, update, cidade, regiao, pais, codigo_postal, organizacao, usuario_id, id) FROM stdin;
1	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36	/api/cliente/by_empresa/	2024-03-12 18:56:32.026393+00	t	2024-03-12 18:56:32.026436+00	\N	\N	\N	\N	\N	\N	1	9a6c13ef-de65-4ab7-ad1d-4c7d876a4047
2	169.254.129.1	HealthCheck/1.0	/	2024-03-22 14:17:57.461168+00	t	2024-03-22 14:17:57.461182+00	\N	\N	\N	\N	\N	\N	\N	0b2a58ab-5c09-4f75-a565-bb8ffb4282e9
\.


--
-- Data for Name: app_transacao; Type: TABLE DATA; Schema: public; Owner: wmsdatabase
--

COPY public.app_transacao (id, valor, descricao, caixa_id, venda_id, insert, update) FROM stdin;
\.


--
-- Name: app_cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wmsdatabase
--

SELECT pg_catalog.setval('public.app_cliente_id_seq', 10, true);


--
-- Name: app_empresa_id_empresa_seq; Type: SEQUENCE SET; Schema: public; Owner: wmsdatabase
--

SELECT pg_catalog.setval('public.app_empresa_id_empresa_seq', 7, true);


--
-- Name: app_endereco_id_endereco_seq; Type: SEQUENCE SET; Schema: public; Owner: wmsdatabase
--

SELECT pg_catalog.setval('public.app_endereco_id_endereco_seq', 12, true);


--
-- Name: app_galao_id_galao_seq; Type: SEQUENCE SET; Schema: public; Owner: wmsdatabase
--

SELECT pg_catalog.setval('public.app_galao_id_galao_seq', 1, false);


--
-- Name: app_gestaogalao_id_gestao_galao_seq; Type: SEQUENCE SET; Schema: public; Owner: wmsdatabase
--

SELECT pg_catalog.setval('public.app_gestaogalao_id_gestao_galao_seq', 1, false);


--
-- Name: app_loja_id_loja_seq; Type: SEQUENCE SET; Schema: public; Owner: wmsdatabase
--

SELECT pg_catalog.setval('public.app_loja_id_loja_seq', 2, true);


--
-- Name: app_sessao_id_sessao_seq; Type: SEQUENCE SET; Schema: public; Owner: wmsdatabase
--

SELECT pg_catalog.setval('public.app_sessao_id_sessao_seq', 2, true);


--
-- Name: app_transacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wmsdatabase
--

SELECT pg_catalog.setval('public.app_transacao_id_seq', 1, false);


--
-- Name: app_usuario_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: wmsdatabase
--

SELECT pg_catalog.setval('public.app_usuario_id_usuario_seq', 27, true);


--
-- PostgreSQL database dump complete
--

