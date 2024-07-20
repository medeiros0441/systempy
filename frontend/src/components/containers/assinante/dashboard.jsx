import React, { useEffect } from 'react';
import { request } from 'src/utils/api';
import { setLocalStorageItem } from 'src/utils/storage';
import alerta from 'src/utils/alerta';
import loading from 'src/utils/loading';

const calcularFaturamentoTotal = () => {
  const vendas = JSON.parse(localStorage.getItem('data_vendas'));
  let totalFaturamento = 0;
  const mesAtual = new Date().getMonth() + 1;

  const formatarNumero = (numero) => {
    if (typeof numero === 'number' && !isNaN(numero)) {
      return numero.toFixed(2);
    } else {
      return '0.00';
    }
  };

  const converterStringParaData = (dataString) => {
    const parts = dataString.split('-');
    if (parts.length === 3) {
      return new Date(parts[0], parts[1] - 1, parts[2]);
    }
    return null;
  };

  if (vendas && vendas.length > 0) {
    vendas.forEach((venda) => {
      const dataVenda = converterStringParaData(venda.insert);

      if (dataVenda !== null) {
        const mesVenda = dataVenda.getMonth() + 1;
        const valorVenda = parseFloat(venda.valor_total);

        if (!isNaN(valorVenda) && mesVenda === mesAtual) {
          totalFaturamento += valorVenda;
        }
      } else {
        console.error('Data inválida:', venda.insert);
      }
    });
  }
  return formatarNumero(totalFaturamento);
};

const atualizarFaturamento = () => {
  const totalFaturamento = calcularFaturamentoTotal();
  document.getElementById('total-faturamento').innerText = `R$ ${totalFaturamento}`;
};

const checkStockLevels = () => {
  const products = JSON.parse(localStorage.getItem('data_produtos'));
  if (products && products.length > 0) {
    products.forEach((product) => {
      const currentStock = product.quantidade_atual_estoque;
      const minStock = product.quantidade_minima_estoque;
      if (currentStock <= minStock) {
        const message = `O produto ${product.nome} está próximo da quantidade mínima de estoque. Quantidade atual: ${currentStock}`;
        alerta(message, 4);
      }
    });
  }
};

const getData = () => {
  loading(true, 'dashboard');
  request('vendas/dados')
    .then((response) => {
      if (response.success === true) {
        setLocalStorageItem('data_lojas', response.lojas);
        setLocalStorageItem('data_vendas', response.vendas);
        setLocalStorageItem('data_produtos', response.produtos);
        atualizarFaturamento();
      } else {
        alerta(response.error);
      }
    })
    .catch((error) => {
      console.error('Erro ao chamar a função Python:', error);
    })
    .finally(() => {
      loading(false, 'dashboard');
    });
};

const Dashboard = () => {
  useEffect(() => {
    getData();
    checkStockLevels();
  }, []);

  return (
    <div className="container mx-auto mt-3" id="dashboard">
      <div className="row">
        <div className="col-md-6 mx-auto">
          <div className="card">
            <div className="card-header bg-primary text-white">
              <i className="bi bi-bar-chart-line"></i> Faturamento Total
            </div>
            <div className="card-body">
              <h5 className="card-title" id="total-faturamento">R$ 0,00</h5>
              <p className="card-text">Este é o faturamento total de todas as lojas, deste mês.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
