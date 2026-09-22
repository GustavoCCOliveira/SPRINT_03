# ChargeGrid Intelligence — Sprint 3

## Protótipo Funcional e Integração

Projeto desenvolvido para a **Global Solution — FIAP**, com foco em gerenciamento inteligente de energia para recarga de veículos elétricos, integração de fontes renováveis e automação do consumo energético.

A Sprint 3 evolui o protótipo desenvolvido anteriormente, adicionando a integração entre **energia solar, rede elétrica, gerenciamento de demanda e veículos elétricos**, permitindo simular uma estação inteligente de recarga.

---

## Equipe

| Integrante           | RM |
| -------------------- | -- |
* RM: 561975 Rafael laprega gontijo magalhaes 
* RM: 572952 Gustavo Torres de Oliveira 
* RM: 568690 Lucas Furquim Lima 
- RM: 570246 Diogo Chiaradia Santos

> Substitua os nomes e RMs pelos integrantes da equipe.

---

## Objetivo do Projeto

O **ChargeGrid Intelligence** tem como objetivo desenvolver uma solução capaz de gerenciar a energia destinada à recarga de veículos elétricos de maneira automatizada.

O sistema considera:

* Consumo energético da instalação;
* Energia gerada por fonte renovável;
* Energia disponível da rede elétrica;
* Quantidade de veículos conectados;
* Estado da bateria dos veículos;
* Potência disponível para recarga;
* Demanda energética;
* Tarifa dinâmica;
* Situações de baixa disponibilidade de energia.

A partir dessas informações, o sistema realiza automaticamente a distribuição da potência disponível entre os veículos.

---

# Evolução da Sprint 2 para a Sprint 3

Na Sprint 2, o projeto apresentava uma simulação baseada principalmente no consumo da instalação e na distribuição de energia entre os veículos.

Na Sprint 3, o projeto foi ampliado para apresentar uma integração maior entre os componentes.

### Sprint 2

```text
Consumo da instalação
          ↓
Energia disponível
          ↓
ChargeGrid Intelligence
          ↓
Distribuição de potência
          ↓
Veículos elétricos
```

### Sprint 3

```text
                  ┌──────────────────┐
                  │   ENERGIA SOLAR  │
                  └────────┬─────────┘
                           │
                           ▼
                    Energia renovável
                           │
                           ▼
┌────────────────┐  ┌──────────────────────┐
│ REDE ELÉTRICA  │─►│ CHARGEGRID           │
│                │  │ INTELLIGENCE         │
└────────────────┘  └──────────┬───────────┘
                               │
                     Gerenciamento de
                          demanda
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
           BYD Dolphin     GWM Ora 03     Volvo EX30
                 │             │             │
                 └─────────────┼─────────────┘
                               ▼
                       Balanceamento de
                            potência
                               │
                               ▼
                        Recarga das baterias
```

---

# Funcionamento do Sistema

O sistema é composto por três elementos principais:

### 1. Fonte de energia renovável

A classe `EnergiaSolar` simula a geração de energia proveniente de painéis solares.

A quantidade de energia gerada varia durante a execução do programa, representando diferentes condições de geração.

```python
painel_solar = EnergiaSolar(
    capacidade_maxima=30.0
)
```

A geração é simulada utilizando valores variáveis:

```python
random.uniform(10.0, self.capacidade_maxima)
```

Dessa forma, cada ciclo pode apresentar uma quantidade diferente de energia renovável disponível.

---

### 2. Rede elétrica

A rede possui um limite máximo de potência definido no sistema:

```python
central_chargegrid = ChargeGridIntelligence(
    limite_max_rede=80.0
)
```

O sistema simula o consumo da instalação:

```python
consumo_predio = random.uniform(30.0, 65.0)
```

A energia disponível da rede é calculada a partir da diferença entre o limite da rede e o consumo da instalação.

```text
Energia disponível da rede =
Limite máximo da rede - Consumo da instalação
```

---

### 3. ChargeGrid Intelligence

O módulo principal é responsável pelo gerenciamento da energia disponível.

Ele recebe informações sobre:

* Consumo da instalação;
* Energia solar;
* Energia disponível da rede;
* Veículos conectados.

Depois disso, calcula a quantidade de potência que pode ser direcionada aos veículos.

---

# Veículos Elétricos

O protótipo utiliza três veículos simulados:

| Veículo     | Bateria inicial | Capacidade |
| ----------- | --------------: | ---------: |
| BYD Dolphin |          15 kWh |     45 kWh |
| GWM Ora 03  |          38 kWh |     48 kWh |
| Volvo EX30  |          42 kWh |     51 kWh |

Cada veículo é representado pela classe `CarroEletrico`.

A classe controla:

* Modelo;
* Bateria atual;
* Capacidade máxima;
* Potência de recarga;
* Energia recebida;
* Porcentagem da bateria.

---

# Gerenciamento Automático da Energia

Após calcular a energia disponível, o sistema divide a potência entre os veículos conectados.

A potência máxima por veículo é limitada a:

```text
11 kW
```

O objetivo é evitar que um único veículo utilize toda a energia disponível.

### Exemplo

Se três veículos estiverem conectados:

```text
Energia disponível
        ↓
ChargeGrid Intelligence
        ↓
Divisão da potência
   ↙       ↓       ↘
Carro 1  Carro 2  Carro 3
```

Essa distribuição permite utilizar a infraestrutura disponível de maneira equilibrada.

---

# Controle de Situações Críticas

O sistema possui mecanismos para situações em que a quantidade de energia disponível não é suficiente.

## Baixa disponibilidade

Quando a energia disponível fica abaixo de determinado nível, o sistema reduz a potência de carregamento.

```text
Baixa disponibilidade
        ↓
Redução da potência
        ↓
Recarga controlada
```

## Demanda crítica

Quando a disponibilidade energética é muito baixa:

```text
Demanda crítica
        ↓
Potência de recarga = 0 kW
        ↓
Carregamento suspenso
```

Essa funcionalidade representa um mecanismo de proteção da infraestrutura energética.

---

# Tarifa Dinâmica

O sistema também possui um mecanismo de tarifa baseado na demanda energética.

As faixas utilizadas são:

| Demanda               |      Tarifa |
| --------------------- | ----------: |
| Até 50% da capacidade | R$ 0,65/kWh |
| Acima de 50%          | R$ 1,20/kWh |
| Acima de 85%          | R$ 2,50/kWh |

A tarifa é determinada automaticamente durante cada ciclo de monitoramento.

> O mecanismo utilizado nesta versão é baseado em regras condicionais e não em um modelo de Machine Learning.

---

# Coleta de Dados

Durante a execução, o sistema registra informações de cada ciclo de monitoramento.

São armazenados:

* Horário;
* Consumo da instalação;
* Energia solar gerada;
* Energia disponível da rede;
* Energia total disponível;
* Tarifa;
* Potência distribuída por veículo.

Essas informações são armazenadas no histórico do sistema.

```python
self.historico.append(registro)
```

Ao final da simulação, o sistema apresenta um relatório consolidado.

---

# Relatório Final

Ao terminar os ciclos de simulação, o sistema apresenta:

* Quantidade de ciclos realizados;
* Energia solar total simulada;
* Consumo médio da instalação;
* Potência média por veículo;
* Estado final da bateria;
* Energia recebida por cada veículo.

Exemplo:

```text
======================================================================
              RELATÓRIO FINAL DA SESSÃO
======================================================================

Ciclos de monitoramento: 5

Energia solar total simulada: XX.XX kW
Consumo médio da instalação: XX.XX kW
Potência média por veículo: XX.XX kW

STATUS FINAL DOS VEÍCULOS

BYD Dolphin       | Bateria: XX.X% | Energia recebida: XX.XX kWh
GWM Ora 03        | Bateria: XX.X% | Energia recebida: XX.XX kWh
Volvo EX30        | Bateria: XX.X% | Energia recebida: XX.XX kWh
```

---

# Arquitetura do Sistema

```text
                    ┌───────────────────┐
                    │    ENERGIA SOLAR  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ ENERGIA DISPONÍVEL│
                    └─────────┬─────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────────┐
│  REDE ELÉTRICA  │───►│ CHARGEGRID          │
└─────────────────┘    │ INTELLIGENCE        │
                       └──────────┬──────────┘
                                  │
                         ┌────────▼────────┐
                         │ GERENCIAMENTO    │
                         │ DE DEMANDA       │
                         └────────┬─────────┘
                                  │
                   ┌──────────────┼──────────────┐
                   │              │              │
                   ▼              ▼              ▼
              ┌────────┐    ┌────────┐    ┌────────┐
              │ CARRO 1│    │ CARRO 2│    │ CARRO 3│
              └────────┘    └────────┘    └────────┘
                   │              │              │
                   └──────────────┼──────────────┘
                                  ▼
                         ┌────────────────┐
                         │ BATERIAS DOS   │
                         │ VEÍCULOS       │
                         └────────────────┘
```

---

# Tecnologias Utilizadas

## Python

A linguagem Python foi utilizada para desenvolver toda a lógica do protótipo.

Principais recursos utilizados:

* Classes;
* Objetos;
* Métodos;
* Listas;
* Estruturas condicionais;
* Laços de repetição;
* Funções;
* Manipulação de dados;
* Geração de valores simulados.

## Bibliotecas

### `random`

Utilizada para simular condições variáveis do sistema, como:

* Consumo energético;
* Geração solar.

### `time`

Utilizada para criar intervalos entre os ciclos de monitoramento.

### `datetime`

Utilizada para registrar o horário de cada ciclo.

---

# Conexão com a Disciplina

O projeto utiliza conceitos relacionados à computação e à lógica aplicada a sistemas inteligentes.

### Programação Orientada a Objetos

O sistema é estruturado utilizando classes:

```text
CarroEletrico
EnergiaSolar
ChargeGridIntelligence
```

Cada classe representa uma parte do sistema.

### Lógica Condicional

O sistema utiliza condições para tomar decisões automaticamente.

Exemplo:

```python
if energia_total_disponivel < 6:
    potencia_por_carro = 0
```

Isso representa uma regra de controle do sistema.

### Automação

Após receber os dados, o sistema realiza automaticamente:

1. Leitura dos dados;
2. Cálculo da energia disponível;
3. Definição da tarifa;
4. Distribuição da potência;
5. Atualização das baterias;
6. Registro dos resultados.

---

# Sustentabilidade

O projeto busca contribuir para uma utilização mais eficiente da energia durante a recarga de veículos elétricos.

A integração da energia solar permite simular a utilização de uma fonte renovável para complementar a energia proveniente da rede.

O gerenciamento automático também evita que todos os veículos utilizem potência máxima de forma indiscriminada.

O sistema pode:

* Aproveitar energia renovável disponível;
* Controlar a potência de recarga;
* Reduzir o carregamento em situações críticas;
* Distribuir a energia entre os veículos;
* Monitorar o consumo energético.

---

# Como Executar

## Requisitos

É necessário possuir:

* Python 3.x;
* Terminal ou IDE compatível com Python.

O projeto não necessita de bibliotecas externas.

---

## Execução

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd NOME_DO_PROJETO
```

Execute:

```bash
python main.py
```

O programa iniciará a simulação e realizará cinco ciclos de monitoramento.

---

# Demonstração

O vídeo da Sprint 3 apresenta:

1. Inicialização do sistema;
2. Conexão dos veículos;
3. Geração simulada de energia solar;
4. Consumo da instalação;
5. Cálculo da energia disponível;
6. Definição da tarifa;
7. Distribuição automática da potência;
8. Atualização das baterias;
9. Monitoramento dos veículos;
10. Relatório final da sessão.

### Vídeo

**YouTube — Não listado:**
`INSIRA_AQUI_O_LINK_DO_VIDEO`

---

# Repositório

**GitHub:**
`INSIRA_AQUI_O_LINK_DO_REPOSITORIO`

---

# Conclusão

A Sprint 3 transforma o projeto ChargeGrid Intelligence em um protótipo funcional integrado, demonstrando a interação entre energia renovável, rede elétrica, gerenciamento automatizado e veículos elétricos.

Por meio da simulação, é possível observar como diferentes condições de geração e consumo influenciam a disponibilidade de energia e como o sistema responde automaticamente, distribuindo ou suspendendo a potência de recarga conforme as condições encontradas.

O protótipo permite demonstrar, de forma prática, conceitos de **programação, automação, gerenciamento energético, sustentabilidade e integração de sistemas**.
