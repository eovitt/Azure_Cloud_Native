import streamlit as st
from azure.storage.blob import BlobServiceClient
import pymssql
import uuid
import json
import os
import pandas as pd

# Configurações do Azure Storage
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=stadevlab001brst;AccountKey=HKrhOIqRV4o7omEMFZIjMNC6qgKJkCbcqMifv/X86dXUsMQt/H7QfD5F1GG3jHA69TCYRYrlyB1L+AStoGvKSw==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "fotos"
ACCOUNT_NAME = "stadevlab001brst"

# Configurações do Azure SQL Server
SQL_SERVER   = "srv001dio11.database.windows.net"
SQL_DATABASE = "sqllab001dbdev"
SQL_USERNAME = "vpgomesdev001"
SQL_PASSWORD = "Pa$$word1159"

# Título da aplicação
st.title("Cadastro de Produto")

# Formulário para cadastro do produto
product_name = st.text_input("Nome do Produto")
description = st.text_area("Descrição do Produto")
price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
uploaded_file = st.file_uploader("Imagem do Produto", type=["png", "jpg", "jpeg"])

# Função para enviar imagem para o Azure Blob Storage
def upload_image(file):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_name = f"{uuid.uuid4()}.jpg"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file.read(), overwrite=True)
        image_url = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
        return image_url
    except Exception as e:
        st.error(f"Erro ao enviar imagem: {e}")
        return None

# Função para garantir que a coluna imagem_url existe
def ensure_column_exists():
    try:
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USERNAME, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'Produtos' AND COLUMN_NAME = 'imagem_url'
            )
            BEGIN
                ALTER TABLE dbo.Produtos ADD imagem_url VARCHAR(1000);
            END
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Erro ao verificar/criar coluna imagem_url: {e}")

# Função para inserir os dados do produto no Azure SQL Server
def insert_product_sql(product_data):
    try:
        ensure_column_exists()  # Garante que a coluna existe antes de inserir

        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USERNAME, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO dbo.Produtos (nome, descricao, preco, imagem_url)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (product_data["nome"], product_data["descricao"], product_data["preco"], product_data["imagem_url"]))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir no Azure SQL: {e}")
        return False

# Função para listar os produtos do Azure SQL Server
def list_products_sql():
    try:
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USERNAME, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor(as_dict=True)
        query = "SELECT id, nome, descricao, preco, imagem_url FROM dbo.Produtos"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao listar produtos: {e}")
        return []

# Função para exibir os produtos em cards
def list_produtos_screen():
    products = list_products_sql()
    if products:
        cards_por_linha = 3
        cols = st.columns(cards_por_linha)
        for i, product in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f"### {product['nome']}")
                st.write(f"**Descrição:** {product['descricao']}")
                st.write(f"**Preço:** R$ {product['preco']:.2f}")
                if product["imagem_url"]:
                    html_img = f'<img src="{product["imagem_url"]}" width="200" height="200" alt="Imagem do produto">'
                    st.markdown(html_img, unsafe_allow_html=True)
                st.markdown("---")
            if (i + 1) % cards_por_linha == 0 and (i + 1) < len(products):
                cols = st.columns(cards_por_linha)
    else:
        st.info("Nenhum produto encontrado.")

# Botão para cadastrar produto
if st.button("Cadastrar Produto"):
    if not product_name or not description or price is None:
        st.warning("Preencha todos os campos obrigatórios!")
    else:
        image_url = ""
        if uploaded_file is not None:
            image_url = upload_image(uploaded_file)

        product_data = {
            "nome": product_name,
            "descricao": description,
            "preco": price,
            "imagem_url": image_url
        }

        if insert_product_sql(product_data):
            st.success("Produto cadastrado com sucesso no Azure SQL!")
            list_produtos_screen()
        else:
            st.error("Houve um problema ao cadastrar o produto no Azure SQL.")

        # Salvar localmente (opcional)
        file_path = "produtos.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    produtos = json.load(f)
                except json.JSONDecodeError:
                    produtos = []
        else:
            produtos = []

        produtos.append(product_data)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(produtos, f, ensure_ascii=False, indent=4)
        
        st.json(product_data)

# Listagem de produtos
st.header("Listagem dos Produtos")
if st.button("Listar Produtos"):
    list_produtos_screen()
