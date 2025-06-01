import tkinter as tk
from tkinter import messagebox
from collections import deque
from threading import Thread
from time import sleep

class Processo:
    def __init__(self, nome, chegada, duracao):
        self.nome = nome
        self.chegada = chegada
        self.tempo_restante = duracao
        self.inicio_execucao = None
        self.termino_execucao = None
        self.label = None
    #metodo para verificar se processos devem voltar a fila
    def verifica_tempo(self, time:int, fila) -> bool:
        return self.chegada == time and self not in fila and self.tempo_restante > 0

def round_robin_ui(processos, quantum, root, canvas):
    tempo = 0
    fila_prontos = deque()
    ordem_execucao = []

    while True:
        # Verifica se há novos processos para adicionar à fila
        for processo in processos:
            if processo.verifica_tempo(tempo, fila_prontos):
                fila_prontos.append(processo)

        if fila_prontos:
            processo = fila_prontos.popleft()
            ordem_execucao.append(processo.nome)

            # Marca início da execução, se ainda não tiver sido registrado
            if processo.inicio_execucao is None:
                processo.inicio_execucao = tempo

            for p in processos:
                if p.tempo_restante == 0:
                    p.label.config(bg="red")
                    continue
                p.label.config(bg="gray" if p != processo else "green")
            root.update()

            # Executa o processo até 2 unidades ou até acabar
            for _ in range(quantum):
                if processo.tempo_restante > 0:
                    sleep(1)
                    tempo += 1
                    processo.tempo_restante -= 1

                    # Verifica chegada de novos processos a cada unidade de tempo
                    for p in processos:
                        if p.verifica_tempo(tempo, fila_prontos):
                            fila_prontos.append(p)

                if processo.tempo_restante == 0:
                    processo.termino_execucao = tempo
                    processo.label.config(bg="red")
                    break
            else:
                # Se não finalizou, volta para o fim da fila
                fila_prontos.append(processo)
        else:
            # Se fila está vazia mas ainda há processos a serem executados
            if any(p.tempo_restante > 0 for p in processos):
                sleep(1)
                tempo += 1
                continue
            break

        root.update()
        sleep(0.5)

    # Exibição dos resultados
    resultado = "\nOrdem de Execução:\n" + " → ".join(ordem_execucao)
    tempos_resposta = []
    for p in processos:
        resposta = p.inicio_execucao - p.chegada
        tempos_resposta.append(resposta)
        resultado += f"\n{p.nome}: Tempo de Resposta = {resposta}"

    media = sum(tempos_resposta) / len(tempos_resposta)
    resultado += f"\n\nTempo Médio de Resposta: {media:.2f}"

    messagebox.showinfo("Resultados", resultado)

def iniciar_simulacao(entradas, quantum_entry, root, canvas):
    for widget in canvas.winfo_children():
        widget.destroy()

    try:
        quantum = int(quantum_entry.get())
        if quantum <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Quantum inválido. Use número inteiro positivo.")
        return

    processos = []
    for i, (entrada_chegada, entrada_duracao) in enumerate(entradas):
        try:
            chegada = int(entrada_chegada.get())
            duracao = int(entrada_duracao.get())
            if chegada < 0 or duracao <= 0:
                raise ValueError
            nome = f"P{i+1}"
            processo = Processo(nome, chegada, duracao)
            lbl = tk.Label(canvas, text=nome, bg="gray", fg="white", width=15, height=2)
            lbl.pack(pady=5)
            processo.label = lbl
            processos.append(processo)
        except ValueError:
            messagebox.showerror("Erro", f"Dados inválidos no processo P{i+1}.")
            return

    Thread(target=round_robin_ui, args=(processos, quantum, root, canvas)).start()

def criar_campos_processos(num_processos_entry, entradas_frame):
    for widget in entradas_frame.winfo_children():
        widget.destroy()

    try:
        n = int(num_processos_entry.get())
        if n <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Número de processos inválido.")
        return

    entradas = []
    for i in range(n):
        tk.Label(entradas_frame, text=f"Chegada P{i+1}:").grid(row=i, column=0, padx=5, pady=2)
        entrada_chegada = tk.Entry(entradas_frame, width=5)
        entrada_chegada.grid(row=i, column=1)

        tk.Label(entradas_frame, text="Duração:").grid(row=i, column=2)
        entrada_duracao = tk.Entry(entradas_frame, width=5)
        entrada_duracao.grid(row=i, column=3)

        entradas.append((entrada_chegada, entrada_duracao))

    return entradas


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulador Round Robin com Chegada de Processos")
    root.geometry("550x600")

    tk.Label(root, text="Quantum:").pack()
    quantum_entry = tk.Entry(root)
    quantum_entry.pack()

    tk.Label(root, text="Quantidade de processos:").pack()
    num_processos_entry = tk.Entry(root)
    num_processos_entry.pack()

    entradas_frame = tk.Frame(root)
    entradas_frame.pack(pady=10)

    entradas = []

    def gerar_campos():
        global entradas
        entradas = criar_campos_processos(num_processos_entry, entradas_frame) or []

    tk.Button(root, text="Gerar Campos de Processos", command=gerar_campos).pack(pady=5)

    canvas = tk.Frame(root)
    canvas.pack(pady=20)

    tk.Button(root, text="Iniciar Simulação", command=lambda: iniciar_simulacao(entradas, quantum_entry, root, canvas)).pack(pady=10)

    root.mainloop()