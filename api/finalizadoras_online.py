import sys
import os
import dbf
import mysql.connector
from datetime import datetime

# Verifica se o diretório base foi passado como argumento
if len(sys.argv) < 2:
    print("Uso: python3 teste.py <diretorio_base>")
    sys.exit(1)

# Diretório base onde estão as pastas das filiais, passado como argumento
base_directory = sys.argv[1]

# Configurações de conexão com o banco de dados MySQL
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'SG515t3m45',  # Atualize com a senha correta
    'database': 'dashboard'
}

# Função para processar um arquivo DBF
def process_dbf_file(dbf_file_path, filial):
    # Extração do PDV a partir do nome do arquivo
    file_name = os.path.basename(dbf_file_path)
    pdv = file_name[-6:-4]   

    # Abre a conexão com o banco de dados MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Abre a tabela DBF
    table = dbf.Table(dbf_file_path)

    # Carrega os registros da tabela
    table.open()

    # Itera sobre os registros e insere os dados no banco de dados MySQL
    for record in table:
        horario = record["horario"]
        data = record["data"]
        valor = record["valor"]
        operador = record["operador"]
        cupom = record["cupom"]
        especie = record["especie"]
        origem = record["origem"]
        debi_cred = record["debi_cred"]
        cancelado = record["cancelado"]

        # Comando SQL para inserção dos dados na tabela do banco de dados
        insert_query = """
        INSERT INTO finalizadoras_online (horario, data, valor, operador, cupom, especie, origem, debi_cred, cancelado, filial, pdv)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (horario, data, valor, operador, cupom, especie, origem, debi_cred, cancelado, filial, pdv))

    # Confirma as alterações no banco de dados após o término da iteração
    conn.commit()

    # Fecha a tabela e a conexão após o processamento
    table.close()
    cursor.close()
    conn.close()

# Obtém a data atual
data_atual = datetime.now()

# Extrai o dia e o mês da data atual no formato "DDMM"
dia_mes = data_atual.strftime("%d%m")

# Percorre todas as pastas comuni
for root, dirs, files in os.walk(base_directory):
    for dir_name in dirs:
        if dir_name.startswith("comuni"):
            filial = dir_name.replace('comuni', '')
            filial_dir_path = os.path.join(root, dir_name)

            # Percorre todos os arquivos na pasta da filial e suas subpastas
            for sub_root, sub_dirs, sub_files in os.walk(filial_dir_path):
                for file in sub_files:
                    # Verifica se o arquivo tem o padrão "fiDDMMXX.dbf"
                    if file.startswith("fi" + dia_mes) and file.endswith(".dbf"):
                        dbf_file_path = os.path.join(sub_root, file)
                        process_dbf_file(dbf_file_path, filial)
