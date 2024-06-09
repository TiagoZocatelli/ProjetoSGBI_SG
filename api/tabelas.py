from flask import Flask, render_template, request, jsonify
import dbf
import sqlite3

app = Flask(__name__)

# Função para criar e popular o banco de dados SQLite
def create_db():
    # Conexão com o banco de dados
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Criação da tabela de vendas
    c.execute('''CREATE TABLE IF NOT EXISTS sales
                 (date TEXT, total_sales REAL, total_customers INTEGER)''')

    # Caminho do arquivo DBF
    dbf_file_path = 'parfil.dbf'

    # Abre a tabela DBF
    table = dbf.Table(dbf_file_path)

    # Carrega os registros da tabela
    table.open()

    # Insere os registros na tabela SQLite
    for record in table:
        date = record["data"].strftime('%Y-%m-%d')
        total_sales = record["totvrvenda"]
        total_customers = record["nclientes"]
        c.execute("INSERT INTO sales (date, total_sales, total_customers) VALUES (?, ?, ?)",
                  (date, total_sales, total_customers))

    # Commit das alterações e fechamento da conexão
    conn.commit()
    conn.close()

# Rota para criar e popular o banco de dados
@app.route('/create_db')
def create_db_route():
    create_db()
    return 'Banco de dados criado e populado com sucesso.'

# Rota para buscar os dados filtrados com base na data
@app.route('/sales', methods=['GET'])
def get_sales():
    try:
        # Parâmetros de data enviados pela solicitação GET
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Conexão com o banco de dados
        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        # Consulta SQL para buscar os registros filtrados
        c.execute("SELECT * FROM sales WHERE date BETWEEN ? AND ?", (start_date, end_date))
        filtered_sales = c.fetchall()

        # Fecha a conexão com o banco de dados
        conn.close()

        # Retorna os dados filtrados como JSON
        return jsonify(filtered_sales)

    except Exception as e:
        # Retorna uma mensagem de erro caso ocorra alguma exceção
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
