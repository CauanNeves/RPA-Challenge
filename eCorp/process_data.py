import pandas as pd
import os

# Caminho do arquivo JSON gerado pelo Scrapy
df = pd.read_json('eCorp/dados_teste.json')

# Dividir os dados em grupos de 500 linhas
chunk_size = 500
sheets = ['Dipirona Sódica', 'Atenolol', 'Clonazepam']

# Salvar em um único arquivo Excel com abas específicas
with pd.ExcelWriter('eCorp/dados.xlsx', engine='openpyxl') as writer:
    for i, sheet_name in enumerate(sheets):
        start_row = i * chunk_size
        end_row = start_row + chunk_size
        
        # Pega o intervalo correspondente de 500 linhas
        df_chunk = df.iloc[start_row:end_row]
        
        # Salva o intervalo na aba correspondente
        df_chunk.to_excel(writer, sheet_name=sheet_name[:30], index=False)

# Salva qualquer linha que restar na última aba (Clonazepam)
if len(df) > len(sheets) * chunk_size:
    df_remaining = df.iloc[len(sheets) * chunk_size:]
    with pd.ExcelWriter('../dados/dados_palavras_chave.xlsx', engine='openpyxl', mode='a') as writer:
        df_remaining.to_excel(writer, sheet_name='Clonazepam_Extra', index=False)

print("Planilha com abas gerada com sucesso!")
