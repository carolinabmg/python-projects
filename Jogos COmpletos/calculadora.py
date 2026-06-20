import tkinter as tk

# ================= FUNÇÕES =================

def clicar(valor):
    entrada.insert(tk.END, valor)


def limpar():
    entrada.delete(0, tk.END)


def calcular():
    try:
        resultado = eval(entrada.get())
        entrada.delete(0, tk.END)
        entrada.insert(0, str(resultado))
    except:
        entrada.delete(0, tk.END)
        entrada.insert(0, "Erro")


# ================= JANELA =================

janela = tk.Tk()
janela.title("🧮 Calculadora")
janela.geometry("350x500")
janela.configure(bg="#ffe4f1")
janela.resizable(True, True)

# ================= VISOR =================

entrada = tk.Entry(
    janela,
    font=("Arial", 24),
    justify="right",
    width=15
)

entrada.pack(
    pady=20,
    padx=20,
    ipady=15
)

# ================= BOTÕES =================

frame = tk.Frame(janela, bg="#ffe4f1")
frame.pack()

botoes = [
    ("7", 0, 0),
    ("8", 0, 1),
    ("9", 0, 2),
    ("/", 0, 3),

    ("4", 1, 0),
    ("5", 1, 1),
    ("6", 1, 2),
    ("*", 1, 3),

    ("1", 2, 0),
    ("2", 2, 1),
    ("3", 2, 2),
    ("-", 2, 3),

    ("0", 3, 0),
    (".", 3, 1),
    ("=", 3, 2),
    ("+", 3, 3)
]

for texto, linha, coluna in botoes:

    if texto == "=":
        comando = calcular
    else:
        comando = lambda t=texto: clicar(t)

    botao = tk.Button(
        frame,
        text=texto,
        width=5,
        height=2,
        font=("Arial", 20, "bold"),
        bg="#fff0f6",
        fg="#6a1b9a",
        command=comando
    )

    botao.grid(
        row=linha,
        column=coluna,
        padx=5,
        pady=5
    )

# ================= BOTÃO LIMPAR =================

tk.Button(
    janela,
    text="🗑️ Limpar",
    font=("Arial", 16, "bold"),
    bg="#ffb6c1",
    command=limpar
).pack(
    pady=20
)

# ================= EXECUTAR =================

janela.mainloop()