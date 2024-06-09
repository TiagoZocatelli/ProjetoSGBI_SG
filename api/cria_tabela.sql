CREATE database dashboard;

CREATE TABLE vendas_mes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE,
    totvrvenda DECIMAL(10, 2),
    nclientes INT,
    codfil VARCHAR(10),
    totvrcusto DECIMAL(10, 2),
    totprodvda DECIMAL(10, 2)
);


CREATE TABLE finalizadoras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    horario TIME,
    data DATE,
    valor DECIMAL(10, 2),
    operador INT,
    cupom INT,
    especie VARCHAR(50),
    origem VARCHAR(50),
    debi_cred CHAR(1),
    cancelado CHAR(1),
    filial INT,  -- Adiciona o campo filial
    pdv INT      -- Adiciona o campo pdv
);


CREATE TABLE finalizadoras_online (
    id INT AUTO_INCREMENT PRIMARY KEY,
    horario TIME,
    data DATE,
    valor DECIMAL(10, 2),
    operador INT,
    cupom INT,
    especie VARCHAR(50),
    origem VARCHAR(50),
    debi_cred CHAR(1),
    cancelado CHAR(1),
    filial INT,  -- Adiciona o campo filial
    pdv INT      -- Adiciona o campo pdv
);



SELECT 
    especie,
    pdv,
    filial,
    SUM(valor) as total
FROM finalizadoras
WHERE debi_cred = 'C' AND cancelado = '' AND pdv = "1" AND filial = "4"
GROUP BY especie, pdv, filial;
