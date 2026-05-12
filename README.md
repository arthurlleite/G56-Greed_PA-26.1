# Rotina de Uma Mae Solo — Organizador de Tarefas para Minimizar Atrasos

Projeto da disciplina **Projeto de Algoritmos** — implementação do algoritmo guloso **Earliest Due Date (EDD)** para minimizar o atraso máximo em um conjunto de tarefas diárias.

---

## Descrição do problema

Uma mãe solo precisa cuidar dos filhos, trabalhar e manter a casa. Ela acorda às **06:00** e tem uma série de tarefas com prazos rígidos: levar as crianças na escola às **07:30**, chegar ao trabalho às **08:00**, buscá-las às **18:00** e muito mais.

Qual é a melhor ordem de execução para que o maior atraso do dia seja o menor possível?

---

## O algoritmo guloso: Earliest Due Date (EDD)

O algoritmo **EDD** resolve o problema com uma escolha gulosa simples:

> **Sempre execute primeiro a tarefa com o menor prazo de entrega.**

A cada passo, em vez de analisar todas as combinações possíveis, o algoritmo escolhe localmente a tarefa mais urgente. Essa escolha local é globalmente ótima para minimizar o atraso máximo — resultado provado por troca de argumentos (exchange argument).

### Por que ordenar pelo menor prazo é uma escolha gulosa?

Imagine duas tarefas consecutivas `i` e `j` com `prazo_i < prazo_j`. Se executarmos `j` antes de `i`, a tarefa `i` ficará mais atrasada do que o necessário. Trocar as duas de ordem nunca piora o atraso máximo. Aplicando esse argumento a todas as trocas possíveis, chega-se à ordem EDD como globalmente ótima.

---

## Estrutura do projeto

```
greedy-atraso-maximo/
├── main.py          # Algoritmo EDD: leitura, ordenação e cálculo
├── visualizar.py    # Gráfico de Gantt interativo (matplotlib)
├── tarefas.csv      # 20 tarefas da rotina de uma mãe solo
├── test_main.py     # Testes automatizados com pytest
├── requirements.txt # Dependências (matplotlib + pytest)
└── .gitignore
```

---

## Como rodar o projeto

**Pré-requisitos:** Python 3.8 ou superior.

```bash
# 1. Clone ou baixe o repositório
git clone <url-do-repositorio>
cd greedy-atraso-maximo

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/macOS

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o programa no terminal
python main.py

# 5. Gere o gráfico de Gantt visual
python visualizar.py
```

---

## Como rodar os testes

```bash
pytest test_main.py -v
```

---

## Sobre o arquivo `tarefas.csv`

As colunas `duracao` e `prazo` são representadas em **minutos desde 06:00** (horário em que a mãe acorda). O programa converte automaticamente para o formato **HH:MM** na exibição.

| Horário real | Minutos desde 06:00 |
|---|---|
| 06:00 | 0 |
| 07:30 | 90 |
| 08:00 | 120 |
| 12:00 | 360 |
| 17:30 | 690 |
| 18:00 | 720 |

---

## Exemplo de entrada (`tarefas.csv`)

| id | nome | duracao | prazo |
|----|------|---------|-------|
| 1 | Acordar e levantar | 5 | 10 |
| 2 | Acordar as criancas | 10 | 20 |
| 3 | Dar banho nas criancas | 20 | 50 |
| 4 | Preparar cafe da manha | 20 | 60 |
| 5 | Arrumar mochila das criancas | 10 | 70 |
| 6 | Se arrumar para o trabalho | 20 | 80 |
| 7 | Levar criancas na escola | 25 | 90 |
| 8 | Ir para o trabalho | 20 | 120 |
| ... | ... | ... | ... |
| 20 | Ajudar nas licoes de casa e colocar para dormir | 50 | 900 |

---

## Exemplo de saída

**Terminal (`python main.py`):**

```
  Rotina do dia — horarios a partir das 06:00 | duracao e atraso em minutos

#     ID   Tarefa                                           Dur.    Prazo   Inicio  Termino   Atraso
----------------------------------------------------------------------------------------------------
1     1    Acordar e levantar                               5       06:10   06:00   06:05     -
2     2    Acordar as criancas                              10      06:20   06:05   06:15     -
3     3    Dar banho nas criancas                           20      06:50   06:15   06:35     -
4     4    Preparar cafe da manha                           20      07:00   06:35   06:55     -
5     5    Arrumar mochila das criancas                     10      07:10   06:55   07:05     -
6     6    Se arrumar para o trabalho                       20      07:20   07:05   07:25     5min
7     7    Levar criancas na escola                         25      07:30   07:25   07:50     20min
8     8    Ir para o trabalho                               20      08:00   07:50   08:10     10min
...
20    20   Ajudar nas licoes de casa e colocar para dormir  50      21:00   16:20   17:10     -

Atraso maximo encontrado: 20 minuto(s)
```

**O que o resultado mostra:**

Na correria da manhã, mesmo com o EDD organizando da melhor forma possível, a mãe chega **20 minutos atrasada na escola** e **10 minutos atrasada no trabalho**. A partir das 08:10, com a rotina estabilizada, todas as tarefas são cumpridas no prazo.

**Gráfico de Gantt (`python visualizar.py`):**

![Cronograma de Gantt](cronograma.png)

### Como ler o gráfico

Cada linha representa uma tarefa, ordenada pelo menor prazo (EDD). O eixo horizontal é o horário real do dia (HH:MM).

| Elemento | Significado |
|---|---|
| Barra **verde** | A tarefa foi executada dentro do prazo |
| Barra **vermelha** | A parte da execução que ultrapassou o prazo |
| Seta **laranja** | O prazo (deadline) daquela tarefa |
| **+Xmin** à direita | Quantidade de atraso em minutos |

**Lendo o cronograma da manhã (o trecho mais crítico):**

As 5 primeiras tarefas (acordar, banho, café, mochila) terminam no prazo — as barras são totalmente verdes. O problema começa na tarefa **6 (Se arrumar)**: ela devia terminar às 07:20, mas termina às 07:25 — **5 minutos de atraso**. Esse pequeno atraso se propaga em cascata:

- **Tarefa 7 — Levar crianças na escola:** começa atrasada (07:25 em vez de 07:00) e termina às 07:50. A escola esperava às **07:30** → **20 minutos de atraso** (o maior do dia).
- **Tarefa 8 — Ir para o trabalho:** começa às 07:50 e termina às 08:10. O horário era **08:00** → **10 minutos de atraso**.

A partir das **08:10**, o algoritmo EDD garante que todas as 12 tarefas restantes sejam concluídas dentro do prazo — as barras voltam a ser completamente verdes até o fim do dia.

**Conclusão visual:** o gráfico deixa claro que o EDD minimiza o caos, mas não elimina completamente os atrasos quando o volume de tarefas supera o tempo disponível na janela da manhã. O atraso máximo encontrado é de **20 minutos**.

O arquivo `cronograma.png` é salvo automaticamente na raiz do projeto ao rodar `python visualizar.py`.

---

## Complexidade do algoritmo

| Etapa | Complexidade |
|---|---|
| Leitura do CSV | O(n) |
| Ordenação (EDD) | O(n log n) |
| Cálculo do cronograma | O(n) |
| **Total** | **O(n log n)** |

O gargalo é a ordenação. Para `n` tarefas, o algoritmo é eficiente mesmo para entradas grandes.

---

## Vídeo de apresentação

> Substitua `ID_DO_VIDEO` pelo ID do vídeo publicado no YouTube.

[![Assista ao vídeo](https://img.youtube.com/vi/ID_DO_VIDEO/0.jpg)](https://www.youtube.com/watch?v=ID_DO_VIDEO)

> **Nota:** O GitHub não renderiza `<iframe>` diretamente em Markdown. A forma mais segura e compatível é usar uma imagem clicável que redireciona para o YouTube, como mostrado acima.

---

## Autores

Projeto desenvolvido para a disciplina **Projeto de Algoritmos**.
