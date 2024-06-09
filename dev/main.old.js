function fetchAndDisplayVendasOnline() {
    $.getJSON('/finalizadorasonline')
        .done(function(response) {
            console.log('Dados da API Online:', response); // Log para verificar a estrutura dos dados
            displayVendasOnline(response.pdvs_online);
            console.log('Teste:', response.pdvs_online);
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            console.error('Erro ao buscar dados de vendas online:', textStatus, errorThrown);
        });
}

function displayVendasOnline(pdvs_online) {
    const container = $('#finalizadoras-online');
    container.empty(); // Limpar o contêiner antes de adicionar os novos dados

    // Adicionar os dados de cada PDV à tabela
    for (const filial in pdvs_online) {
        // Criar um título para cada filial
        const filialTitle = $('<h3></h3>').text('Filial: ' + filial);
        container.append(filialTitle);

        // Criar a tabela para a filial
        const table = $('<table class="table table-striped"></table>');
        const thead = $('<thead></thead>').appendTo(table);
        const tbody = $('<tbody></tbody>').appendTo(table);

        // Cabeçalho da tabela
        const headerRow = $('<tr></tr>').appendTo(thead);
        $('<th scope="col">PDV</th>').appendTo(headerRow);

        // Determinar todas as finalizadoras presentes para criar colunas dinamicamente
        const pdvsData = pdvs_online[filial];
        for (const pdv in pdvsData) {
            const finalizadorasData = pdvsData[pdv];
            for (let finalizadora in finalizadorasData) {
                finalizadora = finalizadora.trim(); // Remover espaços extras
                // Adicionar nomes das finalizadoras ao cabeçalho
                $('<th scope="col">' + finalizadora + '</th>').appendTo(headerRow);
            }
            // Sair do loop após verificar apenas um PDV
            break;
        }

        $('<th scope="col">Valor Total</th>').appendTo(headerRow);

        console.log('Dados brutos para Filial ' + filial + ':', pdvsData);

        // Adicionar os dados dos PDVs à tabela
        for (const pdv in pdvsData) {
            const finalizadorasData = pdvsData[pdv];
            const row = $('<tr></tr>').appendTo(tbody);
            $('<td>' + pdv + '</td>').appendTo(row);
            let valorTotal = 0;

            // Adicionar valores das finalizadoras à linha
            for (let finalizadora in finalizadorasData) {
                const valor = finalizadorasData[finalizadora];
                console.log(`Filial: ${filial}, PDV: ${pdv}, Finalizadora: ${finalizadora}, Valor: ${valor}`);
                valorTotal += valor;
                $('<td>R$ ' + valor.toFixed(2) + '</td>').appendTo(row);
            }

            // Adicionar valor total à linha
            $('<td>R$ ' + valorTotal.toFixed(2) + '</td>').appendTo(row);
        }

        // Adicionar a tabela ao contêiner
        container.append(table);
    }
}

// Chamar a função para buscar e exibir os dados quando o documento estiver pronto
$(document).ready(function() {
    fetchAndDisplayVendasOnline();
});
