import tkinter as tk
from tkinter import filedialog, messagebox


class SimulatorMenu:
    """
    Menu do simulador onde toda a interface é criada e onde os atributos são
    recebidos.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Simulador de Cache")
        self.input_file_path = ""
        self.output_file_name = ""
        self.output_file_directory = ""
        self.set_inputs()
        self.set_buttons()

    def set_file_input(self):
        self.input_file_label = tk.Label(
            self.root, text="Selecione o arquivo de entrada:"
        )
        self.input_file_label.grid(row=7, sticky=tk.W)
        tk.Button(
            self.root, text="Selecionar Arquivo", command=self.select_input_file
        ).grid(row=7, column=1)

        self.output_directory_label = tk.Label(
            self.root, text="Selecione o diretório do arquivo de saída:"
        )
        self.output_directory_label.grid(row=9, sticky=tk.W)
        tk.Button(
            self.root, text="Selecionar Diretório", command=self.select_output_directory
        ).grid(row=9, column=1)

    def select_input_file(self):
        self.input_file_path = filedialog.askopenfilename(title="Selecione um arquivo")
        if self.input_file_path:
            self.input_file_label.config(
                text=f"Arquivo selecionado: {self.input_file_path}"
            )
            self.root.update_idletasks()

    def select_output_directory(self):
        self.output_file_directory = filedialog.askdirectory(
            title="Selecione um diretório"
        )
        if self.output_file_directory:
            self.output_directory_label.config(
                text=f"Diretório selecionado: {self.output_file_directory}"
            )
            self.root.update_idletasks()

    def set_inputs(self):
        self.writing_policy = self.set_label(
            text="Política de escrita (0 - write-through e 1 - write-back):", row=0
        )
        self.line_size = self.set_label(
            text="Tamanho da linha (potência de 2, em bytes):", row=1
        )
        self.lines_number = self.set_label(
            text="Número de linhas (potência de 2):", row=2
        )
        self.set_associativity = self.set_label(
            text="Associatividade por conjunto (potência de 2):", row=3
        )
        self.hit_time = self.set_label(text="Hit time (nanosegundos):", row=4)
        self.replacement_policy = self.set_label(
            text="Política de Substituição (0 - LFU, 1 - LRU, 2 - Aleatória):", row=5
        )
        self.main_memory_time = self.set_label(
            text="Tempo de leitura/escrita da memória principal (em ns):", row=6
        )
        self.output_file_name = self.set_label(
            text="Nome do arquivo de saída (exemplo.txt):", row=8
        )
        self.set_file_input()

    def set_buttons(self):
        tk.Button(self.root, text="Quit", command=self.root.quit).grid(
            row=10, column=0, sticky=tk.W, pady=4
        )
        tk.Button(
            self.root,
            text="Show",
            command=self.run_simulation,
        ).grid(row=10, column=1, sticky=tk.E, pady=4)

    def run_simulation(self):
        if att_dict := self.get_all_attributes():
            # TODO: implementar agora o simulador no cache.py
            pass
        else:
            messagebox.showerror(
                title="Erro nos atributos de entrada!",
                message="Verifique os atributos de entrada e rode novamente o programa.",
            )

    def get_all_attributes(self):
        try:
            att_dict = {
                "writing_policy": int(self.writing_policy.get()),
                "line_size": int(self.line_size.get()),
                "lines_number": int(self.lines_number.get()),
                "set_associativity": int(self.set_associativity.get()),
                "replacement_policy": int(self.replacement_policy.get()),
                "hit_time": int(self.hit_time.get()),
                "main_memory_time": int(self.main_memory_time.get()),
                "output_file_name": self.output_file_name.get(),
                "input_file_path": self.input_file_path,
                "output_file_directory": self.output_file_directory,
            }
        except ValueError:
            att_dict = None
        return att_dict

    def set_label(self, text, row):
        tk.Label(self.root, text=text).grid(row=row, column=0, sticky=tk.W)
        att = tk.Entry(self.root)
        att.grid(row=row, column=1, sticky=tk.E)
        return att
