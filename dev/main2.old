let defaultStartDate;
let defaultEndDate;

$(document).ready(function() {

    if ($('#pdvRankingModal').length === 0) {
        $('body').append(`
            <div class="modal fade" id="pdvRankingModal" tabindex="-1" aria-labelledby="pdvRankingModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="pdvRankingModalLabel">Ranking dos PDVs</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <!-- Conteúdo será preenchido dinamicamente -->
                        </div>
                    </div>
                </div>
            </div>
        `);
    }
    
        
    // Definir o período de ano padrão (de janeiro do ano atual a dezembro do ano atual)
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const defaultStartDate = `${currentYear}-01-01`;
    const defaultEndDate = `${currentYear}-12-31`;

    // Definir os valores padrão nos campos de entrada de data
    $('#start_date_input').val(defaultStartDate);
    $('#end_date_input').val(defaultEndDate);

    // Carregar os dados do período padrão
    fetchAndDisplayData();
    fetchAndDisplayVendasOnline();
    fetchdisplayFinalizadorasPorPeriodo(); // Carregar os dados das finalizadoras online
});


function fetchAndDisplayData() {
    // Obter os valores das datas de início e fim
    const startDate = $('#start_date_input').val();
    const endDate = $('#end_date_input').val();
    
    // Fazer a requisição para a API
    $.getJSON(`/filter?start_date=${startDate}&end_date=${endDate}`)
        .done(function(response) {
            // Exibir os dados no dashboard
            displayVendasMensais(response.vendas_mensais);
            displayTotalVendasPorFilial(response.total_vendas_por_filial, startDate, endDate);
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            console.error('Erro ao buscar dados da API:', textStatus, errorThrown);
        });
}


function fetchdisplayFinalizadorasPorPeriodo() {
    $.getJSON('/finalizadoras')
        .done(function(response) {
            console.log('Dados da API:', response); // Log para verificar a estrutura dos dados
            // Chamar a função para exibir os dados na página
            displayFinalizadorasPorPeriodo(response.finalizadoras, response.pdvs);
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            console.error('Erro ao buscar dados da API:', textStatus, errorThrown);
        });
}


function fetchAndDisplayVendasOnline() {
    $.getJSON('/finalizadorasonline')
        .done(function(response) {
            console.log('Dados da API Online:', response); // Log para verificar a estrutura dos dados
            displayVendasOnline(response.pdvs_online);
            console.log ('Teste:', response.pdvs_online);
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            console.error('Erro ao buscar dados de vendas online:', textStatus, errorThrown);
        });
}

function displayVendasOnline(pdvs_online) {
    const container = $('#finalizadoras-online');
    container.empty(); // Limpar o contêiner antes de adicionar os novos dados

    // Criar a tabela
    const table = $('<table class="table"></table>');
    const thead = $('<thead></thead>').appendTo(table);
    const tbody = $('<tbody></tbody>').appendTo(table);

    // Cabeçalho da tabela
    const headerRow = $('<tr></tr>').appendTo(thead);
    $('<th scope="col">Filial</th>').appendTo(headerRow);
    $('<th scope="col">PDV</th>').appendTo(headerRow);
    $('<th scope="col">Finalizadora</th>').appendTo(headerRow);
    $('<th scope="col">Total</th>').appendTo(headerRow);

    // Adicionar os dados de cada PDV à tabela
    for (const filial in pdvs_online) {
        const pdvsData = pdvs_online[filial];
        for (const pdv in pdvsData) {
            const finalizadorasData = pdvsData[pdv];
            for (const finalizadora in finalizadorasData) {
                const total = finalizadorasData[finalizadora];
                const row = $('<tr></tr>').appendTo(tbody);
                $('<td>' + filial + '</td>').appendTo(row);
                $('<td>' + pdv + '</td>').appendTo(row);
                $('<td>' + finalizadora.trim() + '</td>').appendTo(row); // Remover espaços extras
                $('<td>R$ ' + total.toFixed(2) + '</td>').appendTo(row);
            }
        }
    }

    // Adicionar a tabela ao contêiner
    container.append(table);
}

function displayFinalizadorasPorPeriodo(finalizadoras, pdvs) {
    const container = $('#finalizadorasPorPeriodo');
    container.empty(); // Limpar o contêiner antes de adicionar os novos dados

    // Calcular a soma total das finalizadoras
    let totalGeral = 0;
    for (const total of Object.values(finalizadoras)) {
        totalGeral += total;
    }

    // Criar a tabela
    const table = $('<table class="table"></table>');
    const thead = $('<thead></thead>').appendTo(table);
    const tbody = $('<tbody></tbody>').appendTo(table);

    // Cabeçalho da tabela
    const headerRow = $('<tr></tr>').appendTo(thead);
    $('<th scope="col">Finalizadora</th>').appendTo(headerRow);
    $('<th scope="col">Total</th>').appendTo(headerRow);

    // Adicionar os dados de cada finalizadora à tabela
    $.each(finalizadoras, function(finalizadora, total) {
        const row = $('<tr></tr>').appendTo(tbody);
        $('<td>' + finalizadora.trim() + '</td>').appendTo(row); // Remover espaços extras
        $('<td>R$ ' + total.toFixed(2) + '</td>').appendTo(row);
    });

    // Adicionar a linha com a soma total das finalizadoras
    const totalRow = $('<tr></tr>').appendTo(tbody);
    $('<td><strong>Total Geral</strong></td>').appendTo(totalRow);
    $('<td><strong>R$ ' + totalGeral.toFixed(2) + '</strong></td>').appendTo(totalRow);

    // Adicionar a tabela ao contêiner
    container.append(table);

    // Adicionar um botão "Ver Detalhes" abaixo da tabela
    const detailsButton = $('<button class="btn btn-primary btn-sm mt-3">Ver Detalhes</button>').appendTo(container);
    detailsButton.click(function() {
        console.log('Botão Ver Detalhes clicado.'); // Adicionar depuração
        console.log('pdvs:', pdvs); // Adicionar depuração
        // Exibir o ranking dos PDVs
        displayPdvRankingPeriodo(pdvs);
    });
}


function displayPdvRankingPeriodo(pdvs) {
    console.log('Exibindo o ranking dos PDVs.');

    const modal = $('#pdvRankingModal');
    if (!modal.length) {
        console.error('Modal não encontrado.');
        return;
    }

    modal.modal('show');
    const container = modal.find('.modal-body').empty();

    // Adicione um contêiner para cada filial
    $.each(pdvs, function(filial, pdvsData) {
        // Adicionar um contêiner separado para o título da filial
        $('<div class="filial-header" style="background-color: #f0f0f0; padding: 10px; margin-top: 20px; font-weight: bold;">Filial ' + filial + '</div>').appendTo(container);

        const tableContainer = $('<div class="table-container"></div>').appendTo(container);
        const table = $('<table class="table table-bordered table-striped mb-4"></table>').appendTo(tableContainer);
        const thead = $('<thead></thead>').appendTo(table);
        const tbody = $('<tbody></tbody>').appendTo(table);

        // Obter todas as finalizadoras para esta filial
        const finalizadoras = {};
        $.each(pdvsData, function(pdv, finalizadorasData) {
            $.each(finalizadorasData, function(finalizadora) {
                finalizadoras[finalizadora] = true;
            });
        });

        // Criação do cabeçalho
        const headerRow = $('<tr><th>PDV</th></tr>').appendTo(thead);
        for (const finalizadora in finalizadoras) {
            headerRow.append('<th>' + finalizadora + '</th>');
        }

        // Variável para somar os totais
        let totalFilial = 0;

        // Preenchimento dos dados para cada PDV
        $.each(pdvsData, function(pdv, finalizadorasData) {
            const row = $('<tr><td>' + pdv + '</td></tr>').appendTo(tbody);
            for (const finalizadora in finalizadoras) {
                const valor = finalizadorasData[finalizadora] || 0;
                row.append('<td>' + (typeof valor === 'number' ? 'R$ ' + valor.toFixed(2) : valor) + '</td>');
                if (typeof valor === 'number') {
                    totalFilial += valor;
                }
            }
        });

        // Adiciona o total abaixo da tabela
        $('<div class="total-filial" style="font-weight: bold; margin-top: 10px;">Total Filial ' + filial + ': R$ ' + totalFilial.toFixed(2) + '</div>').appendTo(container);
    });
}

let vendasMensaisChart; // Variável global para armazenar o objeto Chart
let clientesMensaisChart; // Variável global para armazenar o objeto Chart

function displayVendasMensais(vendasMensais) {
    const ctxVendas = document.getElementById('vendasMensaisChart').getContext('2d');
    const ctxClientes = document.getElementById('clientesMensaisChart').getContext('2d');
    const labels = [];
    const datasetsVendas = [];
    const datasetsClientes = [];

    // Processar os dados para os gráficos
    for (const codfil in vendasMensais) {
        const data = vendasMensais[codfil];
        const mesLabels = data.map(item => item.mes);
        const vendasData = data.map(item => item.totvrvenda);
        const clientesData = data.map(item => item.nclientes);

        labels.push(...mesLabels);
        datasetsVendas.push({
            label: `Vendas - Filial ${codfil}`,
            data: vendasData,
            borderColor: getRandomColor(),
            fill: false
        });
        datasetsClientes.push({
            label: `Clientes - Filial ${codfil}`,
            data: clientesData,
            borderColor: getRandomColor(),
            fill: false
        });
    }

    // Remover duplicados nas labels
    const uniqueLabels = [...new Set(labels)];

    // Destruir os gráficos existentes, se houverem
    if (vendasMensaisChart) {
        vendasMensaisChart.destroy();
    }
    if (clientesMensaisChart) {
        clientesMensaisChart.destroy();
    }

    // Criar os novos gráficos
    vendasMensaisChart = new Chart(ctxVendas, {
        type: 'line',
        data: {
            labels: uniqueLabels,
            datasets: datasetsVendas
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Mês'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Valor de Vendas'
                    }
                }
            }
        }
    });

    clientesMensaisChart = new Chart(ctxClientes, {
        type: 'line',
        data: {
            labels: uniqueLabels,
            datasets: datasetsClientes
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Mês'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Número de Clientes'
                    }
                }
            }
        }
    });
}

function displayTotalVendasPorFilial(totalVendasPorFilial, startDate, endDate) {
    const container = $('#totalVendasPorFilial');
    container.empty(); // Limpar o contêiner antes de adicionar os novos dados

    // Criar a tabela
    const table = $('<table class="table"></table>');
    const thead = $('<thead></thead>').appendTo(table);
    const tbody = $('<tbody></tbody>').appendTo(table);

    // Cabeçalho da tabela
    const headerRow = $('<tr></tr>').appendTo(thead);
    $('<th scope="col">Filial</th>').appendTo(headerRow);
    $('<th scope="col">Total de Vendas</th>').appendTo(headerRow);
    $('<th scope="col">Número de Clientes</th>').appendTo(headerRow);
    $('<th scope="col">Total de Custo</th>').appendTo(headerRow);
    $('<th scope="col">Total de Produtos Vendidos</th>').appendTo(headerRow);
    $('<th scope="col">Lucro Sobre Custo</th>').appendTo(headerRow);

    let totalVendas = 0;
    let totalCusto = 0;
    let totalClientes = 0;
    let totalProdutos = 0;
    let totalLucroSobreCusto = 0;

    // Adicionar uma linha para o período selecionado
    const periodRow = $('<tr></tr>').appendTo(tbody);
    $('<td colspan="6">Período: ' + startDate + ' a ' + endDate + '</td>').appendTo(periodRow);

    // Adicionar os dados de cada filial à tabela e calcular os totais
    $.each(totalVendasPorFilial, function(codfil, values) {
        const row = $('<tr></tr>').appendTo(tbody);
        $('<td>Filial ' + codfil + '</td>').appendTo(row);
        $('<td>R$ ' + values.totvrvenda + '</td>').appendTo(row);
        $('<td>' + values.nclientes + '</td>').appendTo(row);
        $('<td>R$ ' + values.totvrcusto + '</td>').appendTo(row);
        $('<td>' + values.totprodvda + '</td>').appendTo(row);

        const lucroSobreCusto = values.totvrvenda - values.totvrcusto;
        $('<td>R$ ' + lucroSobreCusto.toFixed(2) + '</td>').appendTo(row);

        // Somar os valores de vendas, custo, clientes e produtos dessa filial aos totais
        totalVendas += parseFloat(values.totvrvenda);
        totalCusto += parseFloat(values.totvrcusto);
        totalClientes += parseInt(values.nclientes);
        totalProdutos += parseFloat(values.totprodvda);
        totalLucroSobreCusto += lucroSobreCusto;
    });

    // Adicionar uma linha para o total de todas as filiais
    const totalRow = $('<tr></tr>').appendTo(tbody);
    $('<td>Total Global</td>').appendTo(totalRow);
    $('<td>R$ ' + totalVendas.toFixed(2) + '</td>').appendTo(totalRow);
    $('<td>' + totalClientes + '</td>').appendTo(totalRow);
    $('<td>R$ ' + totalCusto.toFixed(2) + '</td>').appendTo(totalRow);
    $('<td>' + totalProdutos + '</td>').appendTo(totalRow);
    $('<td>R$ ' + totalLucroSobreCusto.toFixed(2) + '</td>').appendTo(totalRow);

    // Adicionar a tabela ao contêiner
    container.append(table);
}

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}