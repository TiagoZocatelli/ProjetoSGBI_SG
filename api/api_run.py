from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configurações de conexão com o banco de dados MySQL
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'SG515t3m45',
    'database': 'dbf_data'
}

# Rota para buscar os códigos de filiais existentes
@app.route('/getfiliais', methods=['GET'])
def get_filiais():
    try:
        # Conecta-se ao banco de dados MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Consulta SQL para buscar os códigos de filiais distintos
        query = "SELECT DISTINCT codfil FROM sales_data"
        cursor.execute(query)
        results = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Converte os resultados para uma lista de códigos de filiais
        filials = [row[0] for row in results]

        # Retorna os códigos de filiais como JSON
        return jsonify(filials)

    except mysql.connector.Error as e:
        # Retorna uma mensagem de erro caso ocorra alguma exceção ao conectar ao banco de dados
        return jsonify({"error": str(e)}), 500

@app.route('/filter', methods=['GET'])
def filter_data():
    try:
        # Parâmetros de data enviados pela solicitação GET
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        codfils = request.args.getlist('codfil')  # Obter múltiplos códigos de filiais

        # Conecta-se ao banco de dados MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Constrói a string de placeholders para os códigos de filiais
        format_strings = ','.join(['%s'] * len(codfils))
        
# Consulta SQL para filtrar os dados com base nas datas e códigos de filiais
        query = ("""
            SELECT data, codfil, 
                SUM(totvrvenda) AS total_sales, 
                SUM(nclientes) AS total_customers,
                SUM(totvrcusto) AS total_cost, 
                SUM(totprodvda) AS total_products 
            FROM sales_data 
            WHERE data BETWEEN %s AND %s AND codfil IN ({})
            GROUP BY data, codfil
        """.format(','.join(['%s'] * len(codfils))))

        print("SQL Query:", query)  # Imprime a consulta SQL para debug
        cursor.execute(query, [start_date, end_date] + codfils)
        results = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Retorna os resultados da consulta como JSON
        return jsonify(results)

    except mysql.connector.Error as e:
        # Retorna uma mensagem de erro caso ocorra alguma exceção ao conectar ao banco de dados
        return jsonify({"error": str(e)}), 500


# Rota para servir a página HTML
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
