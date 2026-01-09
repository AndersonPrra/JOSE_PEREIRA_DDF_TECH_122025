# Case Técnico — Plataforma de Dados para Otimização de Ações Promocionais no Varejo

A apresentação do case pode ser verificada em: https://youtu.be/KvMPuuDLl2Q

## 1. Contexto do Problema

Uma grande empresa de e-commerce busca construir uma **Plataforma de Dados** capaz de centralizar informações de diferentes áreas do negócio, permitindo análises descritivas e prescritivas com maior agilidade, menor custo e impacto direto na tomada de decisão.

Neste contexto, o desafio proposto consiste em utilizar dados históricos de vendas para **avaliar a efetividade de ações promocionais** e **orientar decisões estratégicas** sobre onde, quando e como aplicar promoções de forma mais eficiente.

---

## 2. Pergunta Central do Projeto

> **Como a empresa pode otimizar suas ações promocionais para maximizar vendas semanais, considerando tipo de loja, departamento, sazonalidade e indicadores econômicos?**

Essa pergunta norteia todas as decisões técnicas e analíticas adotadas ao longo do projeto.

---

## 3. Base de Dados Utilizada

Foi utilizada a base pública **Walmart Sales Dataset**, disponível no Kaggle, contendo mais de **400 mil registros** de vendas semanais.
 https://www.kaggle.com/datasets/uelitonviana/walmart

### Principais informações disponíveis:

* Vendas semanais por loja e departamento
* Tipo e tamanho da loja
* Indicadores econômicos (CPI, desemprego, preço de combustível)
* Informações de feriados
* Intensidade de ações promocionais (Markdowns)

A base permite análises em diferentes níveis de granularidade, sendo adequada para estudos de impacto promocional.

---

## 4. Estruturação de Dados (Arquitetura)

O projeto foi organizado seguindo uma arquitetura em camadas, visando **clareza, reprodutibilidade e escalabilidade**:

### 🔹 Camada Raw

* Dados brutos conforme disponibilizados pela fonte
* Sem alterações estruturais

### 🔹 Camada Processed

* Tratamentos leves e enriquecimento de dados
* Criação de variáveis derivadas, como:

  * total de markdown por registro
  * flags de promoção
  * agregações temporais
* Nenhuma exclusão ou modificação destrutiva dos dados originais

### 🔹 Camada Analytics

Camada orientada a **decisão de negócio**, contendo datasets analíticos prontos para consumo:

1. **promo_efficiency_by_type.parquet**

   * Avalia eficiência promocional por tipo de loja

2. **promo_efficiency_by_dept.parquet**

   * Avalia eficiência promocional por departamento

3. **store_dept_priority.parquet**

   * Ranking prescritivo de prioridade (Loja × Departamento)

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/c56bfded-a1b1-450f-81ef-6cd5c8360be7" />

---

## 5. Análises Exploratórias e Estatísticas

As análises exploratórias permitiram identificar padrões importantes, como:

* Forte concentração das vendas em poucos departamentos
* Diferenças claras de desempenho entre tipos de loja
* Impacto positivo, porém heterogêneo, das promoções
* Distribuições assimétricas com **caudas longas** para vendas e markdowns

Testes estatísticos (Shapiro-Wilk) confirmaram a **não normalidade** das principais métricas, orientando decisões metodológicas posteriores.

---

## 6. Métricas Prescritivas

Com base nas análises, foram definidas métricas prescritivas voltadas à priorização de ações:

### 🔹 Lift Promocional

Diferença relativa entre vendas médias com e sem promoção.

### 🔹 Eficiência Promocional

Relação entre ganho em vendas e intensidade média de desconto.

### 🔹 Score de Prioridade

Métrica composta que combina:

* vendas médias normalizadas
* intensidade promocional normalizada

Essa métrica permite responder **onde a promoção gera maior retorno marginal**, apoiando decisões estratégicas.

---

## 7. Visualização e Consumo dos Dados

### 📈 Dashboard (Looker Studio)

Foi desenvolvido um dashboard conectado à camada **processed**, permitindo:

* visão executiva de vendas
* comparações temporais
* análises por loja, tipo e departamento

pode ser verificado em: https://lookerstudio.google.com/reporting/ef025d31-4140-4bf9-a77a-6b541b04afb7

abaixo segue print do dashboard

<img width="1080" height="1357" alt="Image" src="https://github.com/user-attachments/assets/65bcd908-f381-4d3c-b067-baa935221688" />

### 🧠 Data App (Streamlit)

Um **Data App interativo** foi desenvolvido para consumo da camada **analytics**, permitindo:

* ranking prescritivo de prioridade
* análise de eficiência promocional
* filtros dinâmicos por loja, tipo e departamento
* apoio direto à tomada de decisão

pode ser verificado em: https://data-app-otimiza-o-de-acoes-promocionais-4aarhpvnq6xmrhpxhs2fy.streamlit.app/

Caso deseje rodar localmente, baixe o código do data app, use o terminal para navegar até a pasta específica, através do comando cd, e em seguida rode o comando "python -m streamlit run app.py"

abaixo seggue prints do data app

<img width="1917" height="767" alt="Image" src="https://github.com/user-attachments/assets/b8731f09-5ff2-459c-9a26-692ed3befa27" />

<img width="1916" height="717" alt="Image" src="https://github.com/user-attachments/assets/9936f814-a077-4735-beef-4075269c59dc" />

<img width="1917" height="596" alt="Image" src="https://github.com/user-attachments/assets/0c5ba647-5e8c-48ac-a589-ba4e79331301" />

<img width="1915" height="610" alt="Image" src="https://github.com/user-attachments/assets/d77e9def-a5a6-4886-8b2a-dcddda158099" />

---

## 8. Principais Insights

* Promoções não geram impacto homogêneo: dependem fortemente do tipo de loja e departamento
* Alguns departamentos apresentam alto volume de vendas mesmo com baixa intensidade promocional
* A priorização orientada por dados permite reduzir custos promocionais sem perda de receita
* Métricas compostas são essenciais para decisões prescritivas

---

## 9. Conclusão

O projeto demonstra como uma **plataforma de dados bem estruturada** pode transformar dados históricos em **insights acionáveis**, apoiando decisões estratégicas de negócio.

A abordagem adotada — da estruturação dos dados ao Data App — reflete um cenário real de implementação em empresas orientadas a dados, alinhado às práticas esperadas para projetos conduzidos com a plataforma Dadosfera.

---

## 10. Próximos Passos (Evoluções Possíveis)

* Modelos preditivos de vendas com e sem promoção
* Simulações de cenários promocionais
* Integração com dados em tempo real
* Deploy do Data App em ambiente cloud
