# SIMULADOR DE ALGORITMO ROUND-ROBIN

# Descrição e Objetivo

Esse simulador tem como objetivo simular a execução do algoritmo Roud Robin, utilizado no escalonamento de processos. A atividade foi proposta como parte das avaliações da disciplina de Sistemas Operacionais da UFBA pela professora Larissa Barbosa Leôncio Pinheiro.

Nesse projeto utilizamos a Linguagem Python para criar o simulador e uma interface gráfica para o mesmo atraves da biblioteca Tkinter.

## Resultados da simulação de teste

Ao comparar com o simulador (Operating System Scheduling by
LotusOregano)[https://lotusoregano.itch.io/operational-system-escalonator] obtemos os seguintes resultados:

### Ordem de execução:
> Segue a mesma em ambos os simuladores

Tempo resposta:
- Simulador site:
    > p1: 0
    > p2: 2
    > p3: 4
    > média: 2
- Nosso Simulador:
    > p1: 0
    > p2: 1
    > p3: 2
    > média: 1
- Causa da diferença:
    > Simulador do site considera uma sobrecarga de 1 unidade de tempo para cada processo, o que não é implementado em nosso simulador.

