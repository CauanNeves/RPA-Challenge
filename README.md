# 🩺 Scrapy + Selenium: Consulta de Medicamentos no Portal Nacional de Contratações Públicas

Este projeto é uma ferramenta automatizada desenvolvida em **Python**, utilizando **Scrapy** e **Selenium**, para realizar consultas no **Portal Nacional de Contratações Públicas (PNCP)**. Ele busca informações relacionadas a medicamentos com base em palavras-chave correspondentes ao princípio ativo de cada medicamento.

## 🚀 Funcionalidades

- **Consulta Automatizada:** Realiza buscas no PNCP com base em palavras-chave definidas.
- **Extração de Dados:** Coleta informações relevantes das consultas.
- **Armazenamento em JSON:** Salva os resultados em um arquivo `.json`.
- **Conversão para Excel:** Um segundo script transforma o arquivo `.json` em um arquivo `.xlsx`, organizando os dados por palavra-chave.

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Scrapy**
- **Selenium**
- **Pandas**

## 📂 Estrutura do Projeto

```
.
├── eCorp/              # Diretório principal do projeto
│   ├── spiders/        # Módulos principais do Scrapy
│   │   ├── __init__.py
│   │   ├── consultabot.py
│   │   ├── __init__.py
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── pipelines.py
│   │   ├── settings.py
│   │
│   ├── dados_brutos.json  # Resultado bruto extraído
│   ├── dados.xls          # Resultado final em Excel
│   ├── process_data.py    # Script para processamento dos dados
│   ├── scrapy.cfg         # Arquivo de configuração do Scrapy
│
├── venv/              # Ambiente virtual Python
├── requirements.txt   # Dependências do projeto
├── RPA Challenge.pdf  # Documentação adicional
```

## ⚙️ Como Executar

### 1. Clone o Repositório
```bash
git clone https://github.com/CauanNeves/RPA-Challenge.git
cd RPA-Challenge
```

### 2. Ative o Ambiente Virtual
```bash
source venv/bin/activate  # No Linux/Mac
venv\Scripts\activate    # No Windows
```

### 3. Execute o Crawler
```bash
cd eCorp
scrapy crawl consultabot -o dados_brutos.json
```

Isso irá gerar um arquivo `dados_brutos.json`.

### 4. Processe os Dados
```bash
python process_data.py
```

O arquivo `dados.xls` será gerado na pasta raiz.

## ✅ Contribuições

Sinta-se à vontade para contribuir com melhorias, abrir **issues** ou enviar **pull requests**.

---

✨ *Desenvolvido por Cauan Neves utilizando Scrapy, Selenium e dedicação!* 🚀
