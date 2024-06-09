$(document).ready(function() {
    // Função para carregar os dados dos últimos 12 meses de vendas
    function loadLast12MonthsSales() {
        // Obter as datas de início e término dos últimos 12 meses
        const currentDate = new Date();
        const endMonth = currentDate.getMonth();
        const endYear = currentDate.getFullYear();
        const startMonth = (endMonth - 11 + 12) % 12; // Obter o mês de 12 meses atrás
        const startYear = startMonth > endMonth ? endYear - 1 : endYear; // Ajustar o ano, se necessário
        const startDate = new Date(startYear, startMonth, 1).toISOString().split('T')[0];
        const endDate = new Date(endYear, endMonth + 1, 0).toISOString().split('T')[0];

        // Realizar uma solicitação AJAX para obter os dados das vendas
        $.ajax({
            url: `/filter?start_date=${startDate}&end_date=${endDate}`, // Removido o parâmetro codfil
            method: 'GET',
            success: function(data) {
                // Manipular os dados e exibir na tela conforme necessário
                displaySalesData(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("Erro ao carregar os últimos 12 meses de vendas: ", textStatus, errorThrown);
            }
        });
    }

    function displaySalesData(data) {
        console.log("Dados recebidos:", data); // Verificar se os dados estão corretamente recebidos
    
        let totalSales = 0;
        let totalCustomers = 0;
        let totalCost = 0;
        let totalProducts = 0;
    
        const resultsContainer = $('#results');
        resultsContainer.empty();
    
        data.forEach(result => {
            console.log("Resultados individuais:", result); // Verificar cada resultado individual
    
            totalSales += parseFloat(result.totvrvenda || 0); // Verifica se o valor de venda é válido
            totalCustomers += parseInt(result.nclientes || 0, 10); // Verifica se o número de clientes é válido
            totalCost += parseFloat(result.totvrcusto || 0); // Verifica se o custo total é válido
            totalProducts += parseInt(result.totprodvda || 0, 10); // Verifica se o total de produtos é válido
        });
    
        console.log("Total de vendas:", totalSales);
        console.log("Total de clientes:", totalCustomers);
        console.log("Total de custo:", totalCost);
        console.log("Total de produtos:", totalProducts);

        const salesElement = $('<div>', {
            class: 'result-box sales-box',
            text: `Total de Vendas dos Últimos 12 Meses: R$ ${totalSales.toFixed(2)}`
        });
    
        const customersElement = $('<div>', {
            class: 'result-box customers-box',
            text: `Total de Clientes dos Últimos 12 Meses: ${totalCustomers}`
        });
    
        const costElement = $('<div>', {
            class: 'result-box cost-box',
            text: `Total de Custo dos Últimos 12 Meses: R$ ${totalCost.toFixed(2)}`
        });
    
        const productsElement = $('<div>', {
            class: 'result-box products-box',
            text: `Total de Produtos Vendidos nos Últimos 12 Meses: ${totalProducts}`
        });
    
        resultsContainer.append(salesElement, customersElement, costElement, productsElement);
    }

    // Manipulador de eventos para o clique no link "Comparativo"
    $('#comparativo-link').on('click', function(event) {
        event.preventDefault(); // Impedir o comportamento padrão de clicar em um link

        // Chamar a função para carregar os dados dos últimos 12 meses de vendas
        loadLast12MonthsSales();
    });
});

