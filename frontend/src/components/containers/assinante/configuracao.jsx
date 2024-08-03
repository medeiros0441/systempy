import React from 'react';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router-dom'; // Se você estiver usando o React Router
import Title from 'src/componentes/TitleNavegador'
import { useHistory } from 'react-router-dom';
import request from 'src/utils/api';

const Configuracoes = () => {
    const [personalizacaoData, setPersonalizacaoData] = useState([]);
    const [empresaData, setEmpresaData] = useState({});
    const [lojas, setLojas] = useState([]);
    const [pdvs, setPdvs] = useState([]);
    const [selectedLoja, setSelectedLoja] = useState("0");
    const [selectedPdv, setSelectedPdv] = useState("0");
    const [tabContentVisible, setTabContentVisible] = useState(null);
    const history = useHistory();

    useEffect(() => {
        // Carrega dados quando o componente é montado
        loadDataPersonalizacao();
        loadDataEmpresa();
    }, []);

    // Função para carregar dados da empresa
    const loadDataEmpresa = async () => {
        try {
            const response = await request('/api_get_empresa');
            if (response.data.success) {
                setEmpresaData(response.data.data);
            } else {
                alert('Ocorreu um erro interno.');
            }
        } catch (error) {
            alert(`Erro ao buscar algumas informações: ${error.message}`);
        }
    };

    // Função para carregar dados de personalização
    const loadDataPersonalizacao = async () => {
        try {
            const urls = [
                "/pdv/lista",
                "/api_lojas",
                "/associado_pdv",
                "/personalizacao/list"
            ];
            const responses = await Promise.all(urls.map(url => resquest(url)));
            const [pdvsRes, lojasRes, associadosRes, personalizacaoRes] = responses;

            setPdvs(pdvsRes.data);
            setLojas(lojasRes.data);
            setPersonalizacaoData(personalizacaoRes.data);

            // Atualiza dropdowns e outros elementos
            const { idLoja, idPdv } = getIdsFromPersonalizacao(personalizacaoRes.data);
            setSelectedLoja(idLoja);
            atualizarDropdownLojas(lojasRes.data, idLoja);
            atualizarDropdownPDV(pdvsRes.data.filter(pdv => pdv.loja === parseInt(idLoja)), idPdv);
        } catch (error) {
            alert(`Erro ao buscar algumas informações: ${error.message}`);
        }
    };

    // Atualiza dropdown de PDV
    const atualizarDropdownPDV = (listPdv, id = false) => {
        // Aqui, você precisa ajustar a lógica para atualizar o estado ou diretamente o componente
    };

    // Atualiza dropdown de lojas
    const atualizarDropdownLojas = (listLojas, id = false) => {
        // Aqui, você precisa ajustar a lógica para atualizar o estado ou diretamente o componente
    };

    // Verifica alterações e habilita o botão de salvar
    const verificarAlteracoes = () => {
        const lojaAtual = findByCodigo(personalizacaoData, "1");
        const pdvAtual = findByCodigo(personalizacaoData, "2");

        // Habilita o botão se houver alterações
        document.getElementById('btn_salvar_personalizacao').disabled = (
            selectedLoja === lojaAtual?.valor &&
            selectedPdv === pdvAtual?.valor &&
            selectedLoja !== "0" &&
            selectedPdv !== "0"
        );
    };

    // Envia a personalização para a API
    const salvarPersonalizacao = async () => {
        if (selectedLoja === "0" || selectedPdv === "0") {
            alert("Selecione as opções.");
            return;
        }

        const lojaAtual = findByCodigo(personalizacaoData, "1");
        const pdvAtual = findByCodigo(personalizacaoData, "2");

        if (selectedLoja === lojaAtual?.valor && selectedPdv === pdvAtual?.valor) {
            alert("Selecione as opções.");
            return;
        }

        const dataLoja = createDataObject("Loja Padrão", 1, selectedLoja, `ID da loja: ${selectedLoja}`);
        const dataPdv = createDataObject("PDV Padrão", 2, selectedPdv, `ID do PDV: ${selectedPdv}`);

        await chamarApiPersonalizacao(lojaAtual, dataLoja);
        await chamarApiPersonalizacao(pdvAtual, dataPdv);

        verificarAlteracoes();
    };

    // Função para chamar a API de personalização
    const chamarApiPersonalizacao = async (atual, data) => {
        const url = atual ? `/personalizacao/update/${atual.id_personalizacao}` : "/personalizacao/create";
        const method = atual ? "PUT" : "POST";

        try {
            const response = await reponse(url, method, data);
            if (response.data.success) {
                loadDataPersonalizacao();
                alert("Atualizado com sucesso");
            } else {
                alert("Ocorreu um erro interno.");
            }
        } catch (error) {
            alert(`Erro ao atualizar personalização: ${error.message}`);
        }
    };

    // Obtém IDs da personalização
    const getIdsFromPersonalizacao = (personalizacao) => {
        const idLoja = personalizacao.find(item => Number(item.codigo) === 1)?.valor || "0";
        const idPdv = personalizacao.find(item => Number(item.codigo) === 2)?.valor || "0";
        return { idLoja, idPdv };
    };

    // Encontra item pelo código
    const findByCodigo = (data, codigo) => data.find(item => item.codigo === codigo);

    // Cria objeto de dados para a API
    const createDataObject = (chave, codigo, valor, descricaoInterna) => ({
        chave,
        codigo,
        valor,
        descricao: `Configuração padrão para o ${chave.toLowerCase()} selecionado`,
        descricao_interna: descricaoInterna
    });

    // Manipula mudança no dropdown de loja
    const handleLojaChange = (event) => {
        const selectedLojaId = parseInt(event.target.value);
        setSelectedLoja(event.target.value);
        const filteredPdvs = pdvs.filter(pdv => pdv.loja === selectedLojaId);
        atualizarDropdownPDV(filteredPdvs);
        verificarAlteracoes();
    };

    // Manipula mudança no dropdown de PDV
    const handlePdvChange = (event) => {
        setSelectedPdv(event.target.value);
        verificarAlteracoes();
    };

    // Volta ao menu principal
    const handleBackToMenu = () => {
        setTabContentVisible(null);
    };
    const Desconect = async () => {
        retorn = await response("desconect/", "POST");
        if (retorn.success) {
            Redirect("/home")
        }
    }

    return (
        <>
            <Title text="Configurações" />

            <div className="container mx-auto mt-5">
                {/* Menu List */}
                <div className="card mx-auto aling-item-center bg-dark text-light shadow" style={{ maxWidth: '28rem' }}>
                    <div className="card-header border-bottom border-white">
                        <h1 className="text-light font-montserrat fw-bord my-auto" style={{ fontSize: '1.4rem' }}>Configurações</h1>
                    </div>
                    <div className="list-group">
                        <a className="list-group-item list-group-item-actio border-bottom align-items-center justify-content-between d-flex border-0 bg-dark text-white"
                            href="#personalizacao-content"
                            onClick={() => setTabContentVisible('personalizacao-content')}
                            role="tab">
                            <i className="bi bi-person-gear me-2" style={{ fontSize: '1.4rem' }}></i>
                            <span className="me-auto col">Personalização</span>
                            <i className="bi bi-chevron-right ms-auto" style={{ fontSize: '1.4rem' }}></i>
                        </a>
                        <a className="list-group-item list-group-item-actio border-0 align-items-center justify-content-between d-flex border-0 bg-dark text-white"
                            href="#empresa-content"
                            onClick={() => setTabContentVisible('empresa-content')}
                            role="tab">
                            <i className="bi bi-building-exclamation me-2" style={{ fontSize: '1.4rem' }}></i>
                            <span className="me-auto col">Empresa</span>
                            <i className="bi bi-chevron-right ms-auto" style={{ fontSize: '1.4rem' }}></i>
                        </a>
                    </div>
                    <button className="card-footer border-top border-white text-danger align-items-center d-flex text-decoration-none justify-content-between"
                        onclick={() => Desconect()} type="button">
                        <span className="fw-bold">Desconectar</span>
                        <i className="bi bi-person-x" style={{ fontSize: '1.4rem' }}></i>
                    </button>
                </div>

                {/* Tab Content */}
                <div className={`container ${tabContentVisible ? '' : 'd-none'} tab-content card mx-auto aling-item-center bg-dark text-light shadow py-2`} style={{ maxWidth: '38rem' }}>
                    <div className="d-flex justify-content-between align-items-center border-bottom border-white mb-3">
                        <span className="text-light font-montserrat fw-bord my-auto" style={{ fontSize: '1.4rem' }}>{tabContentVisible}</span>
                        <button className="btn btn-outline-light" onClick={handleBackToMenu}>
                            <i className="bi bi-chevron-left"></i> Voltar ao Menu
                        </button>
                    </div>
                    <div id="personalizacao-content" className={`tab-pane ${tabContentVisible === 'personalizacao-content' ? 'show active' : ''}`}>
                        {/* Conteúdo da personalização */}
                        <div className="row">
                            <div className="col-md-6">
                                <label htmlFor="select_loja">Loja</label>
                                <select id="select_loja" className="form-select select_lojas" value={selectedLoja} onChange={handleLojaChange}>
                                    <option value="0">Selecione</option>
                                    {lojas.map(loja => (
                                        <option key={loja.id_loja} value={loja.id_loja}>{loja.nome}</option>
                                    ))}
                                </select>
                            </div>
                            <div className="col-md-6">
                                <label htmlFor="select_pdv">PDV</label>
                                <select id="select_pdv" className="form-select select_pdv" value={selectedPdv} onChange={handlePdvChange}>
                                    <option value="0">Selecione</option>
                                    {/* Options de PDV serão atualizadas dinamicamente */}
                                </select>
                            </div>
                        </div>
                        <button id="btn_salvar_personalizacao" className="btn btn-primary mt-3" onClick={salvarPersonalizacao}>Salvar</button>
                    </div>
                    <div id="empresa-content" className={`tab-pane ${tabContentVisible === 'empresa-content' ? 'show active' : ''}`}>
                        {/* Conteúdo da empresa */}
                        <p>Nome da Empresa: {empresaData.nome_empresa}</p>
                        <p>CNPJ: {empresaData.nro_cnpj}</p>
                        <p>Razão Social: {empresaData.razao_social}</p>
                        <p>Descrição: {empresaData.descricao}</p>
                        <p>Nome do Responsável: {empresaData.nome_responsavel}</p>
                        <p>Cargo: {empresaData.cargo}</p>
                        <p>Email: {empresaData.email}</p>
                        <p>CPF: {empresaData.nro_cpf}</p>
                        <p>Telefone: {empresaData.telefone}</p>
                        <p>Inserido: {empresaData.insert}</p>
                        <p>Atualizado: {empresaData.update}</p>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Configuracoes;