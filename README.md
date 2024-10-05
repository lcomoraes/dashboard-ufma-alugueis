# Dashboard

Dashboard interativo realizado em python utilizando a biblioteca **Streamlit** para análise de dados de aluguel de imóveis. A fonte de dados está localizada no projeto (houses_to_rent_v2.csv) e também está disponível no kaggle: https://www.kaggle.com/datasets/rubenssjr/brasilian- houses-to-rent.

Este projeto faz parte do estudo relacionado a disciplina de Visualização de Dados do Curso de Especialização em Análise de Dados e Inteligência Artificial - 2024.1. 

### Configuração localhost

1. Com o Python instalado basta seguir as seguintes etapas:
```bash
# atualizando o Pip
python.exe -m pip install --upgrade pip
# criando venv
python -m venv venv
# ativando venv
.\venv\Scripts\activate
# instalando dependências
pip install -r requirements.txt
```

2. Caso ocorra erro de execução de script (não pode ser carregado porque a execução de scripts foi desabilitada neste sistema). Executar no PowerShell como Administrador, o seguinte comando:
```bash
set-executionpolicy unrestricted
```
Para verificar como esta a restrição use o seguinte:
```bash
get-executionpolicy
```

### Configuração via clone do Projeto

1. Clone o repositório em sua máquina local:
   ```bash
   git clone https://github.com/lcomoraes/dashboard-ufma-alugueis.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd <diretorio-do-projeto/dashboard-ufma-alugueis>
   ```
3. Instale as dependências listadas no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

##  Executando o Dashboard

Para executar o dashboard, utilize o seguinte comando:
```bash
streamlit run dashboard.py
```

O dashboard será aberto no navegador.


##  Funcionalidades

- Filtros para selecionar cidades, faixa de área e valor de aluguel, permitindo personalizar a análise.
- Gráficos interativos que exibem:
  - **Quantidade de casas por cidade** (gráfico de barras)
  - **Preço médio de aluguel por quantidade de quartos e cidade** (gráfico de barras agrupadas)
  - **Média de área por cidade** (gráfico de barras)
  - **Média de aluguel por cidade** (gráfico de linha)
  - **Distribuição dos valores embutidos no aluguel por cidade** (gráfico de violino)

##  Ferramentas e Bibliotecas Utilizadas

- **Python**: Linguagem principal do projeto.
- **Streamlit**: Para criar a interface web interativa.
- **Pandas**: Para manipulação e análise de dados.
- **Plotly**: Para a criação de gráficos interativos.

