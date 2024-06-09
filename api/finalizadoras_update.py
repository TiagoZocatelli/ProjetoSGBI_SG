import sys
import os
import dbf
import mysql.connector

# Configurações de conexão com o banco de dados MySQL
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'SG515t3m45',  # Atualize com a senha correta
    'database': 'dashboard'
}

def connect_to_database():
    """Estabelece a conexão com o banco de dados."""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        sys.exit(1)

def read_dbf_files(folder_path):
    """Lê os arquivos DBF de uma pasta e retorna os dados em um array."""
    data_array = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.dbf'):
            file_path = os.path.join(folder_path, file_name)
            table = dbf.Table(file_path)
            table.open()
            for record in table:
                data_array.append(record)
            table.close()
    return data_array

def update_database(cursor, data_array, filial):
    """Atualiza o banco de dados com os dados do array."""
    for record in data_array:
        pdv = record["pdv"]
        cupom = record["cupom"]
        horario = record["horario"]
        data = record["data"]
        valor = record["valor"]
        operador = record["operador"]
        especie = record["especie"]
        origem = record["origem"]
        debi_cred = record["debi_cred"]
        cancelado = record["cancelado"]

        # Verifica se o registro já existe no banco de dados
        select_query = """
        SELECT horario, valor, operador, especie, origem, debi_cred, cancelado
        FROM finalizadoras
        WHERE data = %s AND cupom = %s AND filial = %s
        """
        cursor.execute(select_query, (data, cupom, filial))
        existing_record = cursor.fetchone()

        if existing_record:
            # Compara os valores para verificar se houve alterações
            if (horario, valor, operador, especie, origem, debi_cred, cancelado) != existing_record:
                # Atualiza o registro existente
                update_query = """
                UPDATE finalizadoras
                SET horario = %s, valor = %s, operador = %s, especie = %s, origem = %s, debi_cred = %s, cancelado = %s
                WHERE data = %s AND cupom = %s AND filial = %s
                """
                cursor.execute(update_query, (horario, valor, operador, especie, origem, debi_cred, cancelado, data, cupom, filial))
        else:
            print(f"Registro não encontrado no banco de dados para cupom {cupom} na filial {filial}")

def main(base_directory):
    """Função principal que processa os arquivos DBF."""
    conn = connect_to_database()
    cursor = conn.cursor()

    for root, dirs, files in os.walk(base_directory):
        for dir_name in dirs:
            if dir_name.startswith("comuni"):
                filial = dir_name.replace('comuni', '')
                filial_dir_path = os.path.join(root, dir_name)
                print(f"Processando pasta {dir_name}...")
                data_array = read_dbf_files(filial_dir_path)
                update_database(cursor, data_array, filial)

    # Confirma as alterações no banco de dados
    conn.commit()

    # Fecha a conexão com o banco de dados após o processamento
    cursor.close()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 teste.py <diretorio_base>")
        sys.exit(1)

    base_directory = sys.argv[1]
    main(base_directory)
