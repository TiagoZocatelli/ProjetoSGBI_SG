from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Configurações de conexão com o banco de dados MySQL
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'SG515t3m45',
    'database': 'dashboard'
}

@app.route('/filter', methods=['GET'])
def filter_data():
    try:
        # Parâmetros de data enviados pela solicitação GET
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Conecta-se ao banco de dados MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Consulta SQL para obter os dados de vendas agrupados por mês e ano
        query = """
            SELECT 
                codfil, 
                DATE_FORMAT(data, '%Y-%m') as mes, 
                SUM(nclientes) as nclientes, 
                SUM(totvrvenda) as totvrvenda, 
                SUM(totvrcusto) as totvrcusto, 
                SUM(totprodvda) as totprodvda
            FROM vendas_mes 
            WHERE data BETWEEN %s AND %s
            GROUP BY codfil, mes
            ORDER BY mes
        """
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

        # Consulta SQL para obter o total de vendas no período
        total_query = """
            SELECT 
                codfil,
                SUM(nclientes) as nclientes, 
                SUM(totvrvenda) as totvrvenda, 
                SUM(totvrcusto) as totvrcusto, 
                SUM(totprodvda) as totprodvda
            FROM vendas_mes 
            WHERE data BETWEEN %s AND %s
            GROUP BY codfil
        """
        cursor.execute(total_query, (start_date, end_date))
        total_results = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Processa os resultados para retornar as vendas mensais por filial
        vendas_mensais = {}
        for row in results:
            codfil = row['codfil']
            mes = row['mes']
            if codfil not in vendas_mensais:
                vendas_mensais[codfil] = []
            vendas_mensais[codfil].append({
                'mes': mes,
                'nclientes': row['nclientes'],
                'totvrvenda': row['totvrvenda'],
                'totvrcusto': row['totvrcusto'],
                'totprodvda': row['totprodvda']
            })

        # Processa os resultados para retornar o total de vendas por filial
        total_vendas_por_filial = {}
        for row in total_results:
            codfil = row['codfil']
            total_vendas_por_filial[codfil] = {
                'nclientes': row['nclientes'],
                'totvrvenda': row['totvrvenda'],
                'totvrcusto': row['totvrcusto'],
                'totprodvda': int(row['totprodvda'])
            }

        # Prepara a resposta
        response = {
            "vendas_mensais": vendas_mensais,
            "total_vendas_por_filial": total_vendas_por_filial
        }

        # Retorna os resultados da consulta como JSON
        return jsonify(response)

    except mysql.connector.Error as e:
        # Retorna uma mensagem de erro caso ocorra alguma exceção ao conectar ao banco de dados
        return jsonify({"error": str(e)}), 500

@app.route('/vendasonline', methods=['GET'])
def get_vendas_online():
    try:
        # Conecta-se ao banco de dados MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Consulta SQL para obter os dados da tabela finalizadoras_online
        query = """
            SELECT 
                especie,
                pdv,
                filial,
                SUM(valor) as total
            FROM finalizadoras_online
            WHERE debi_cred = 'C' AND cancelado = ''
            GROUP BY especie, pdv, filial
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Preparar os dados no formato solicitado
        finalizadoras_online = {}
        pdvs_online = {}

        for row in results:
            especie = row['especie']
            pdv = row['pdv']
            filial = row['filial']
            total = float(row['total'])  # Converter para float

            if especie not in finalizadoras_online:
                finalizadoras_online[especie] = 0
            finalizadoras_online[especie] += total

            if pdv not in pdvs_online:
                pdvs_online[pdv] = {}
            if filial not in pdvs_online[pdv]:
                pdvs_online[pdv][filial] = {}
            pdvs_online[pdv][filial][especie] = total

        # Preparar a resposta
        response = {
            "finalizadoras_online": finalizadoras_online,
            "pdvs_online": pdvs_online
        }

        # Retorna os resultados da consulta como JSON
        return jsonify(response)

    except mysql.connector.Error as e:
        # Retorna uma mensagem de erro caso ocorra alguma exceção ao conectar ao banco de dados
        return jsonify({"error": str(e)}), 500
    
@app.route('/finalizadorasonline', methods=['GET'])
def get_finalizadorasonline():
    try:
        # Conecta-se ao banco de dados MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Consulta SQL para obter os dados da tabela finalizadoras_online
        query = """
            SELECT 
                especie,
                pdv,
                filial,
                SUM(valor) as total
            FROM finalizadoras_online
            WHERE debi_cred = 'C' AND cancelado = ''
            GROUP BY especie, pdv, filial
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Preparar os dados no formato solicitado
        pdvs_online = {}

        for row in results:
            especie = row['especie']
            pdv = row['pdv']
            filial = row['filial']
            total = float(row['total'])  # Converter para float

            if filial not in pdvs_online:
                pdvs_online[filial] = {}
            if pdv not in pdvs_online[filial]:
                pdvs_online[filial][pdv] = {}
            if especie not in pdvs_online[filial][pdv]:
                pdvs_online[filial][pdv][especie] = 0
            pdvs_online[filial][pdv][especie] += total

        # Fecha a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Preparar a resposta
        response = {"pdvs_online": pdvs_online}

        # Retorna os resultados da consulta como JSON
        return jsonify(response)

    except mysql.connector.Error as e:
        # Retorna uma mensagem de erro caso ocorra alguma exceção ao conectar ao banco de dados
        return jsonify({"error": str(e)}), 500    

@app.route('/finalizadoras', methods=['GET'])
def get_finalizadoras():
    try:
        # Conecta-se ao banco de dados MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Consulta SQL para obter os dados da tabela finalizadoras
        query = """
            SELECT 
                especie,
                pdv,
                filial,
                SUM(valor) as total
            FROM finalizadoras
            WHERE debi_cred = 'C' AND cancelado = ''
            GROUP BY especie, pdv, filial
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Preparar os dados no formato solicitado
        finalizadoras = {}
        pdvs = {}

        for row in results:
            especie = row['especie']
            pdv = row['pdv']
            filial = row['filial']
            total = float(row['total'])  # Converter para float

            # Finalizadoras
            if especie not in finalizadoras:
                finalizadoras[especie] = 0
            finalizadoras[especie] += total

            # PDVs
            if filial not in pdvs:
                pdvs[filial] = {}
            if pdv not in pdvs[filial]:
                pdvs[filial][pdv] = {}
            if especie not in pdvs[filial][pdv]:
                pdvs[filial][pdv][especie] = 0
            pdvs[filial][pdv][especie] += total

        # Preparar a resposta
        response = {
            "finalizadoras": finalizadoras,
            "pdvs": pdvs
        }

        # Retorna os resultados da consulta como JSON
        return jsonify(response)

    except mysql.connector.Error as e:
        # Retorna uma mensagem de erro caso ocorra alguma exceção ao conectar ao banco de dados
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
