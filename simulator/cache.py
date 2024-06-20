import random
import matplotlib.pyplot as plt


class ChacheLine:
    def __init__(self):
        self.address = None
        self.last_hit_time = 0
        self.access_counter = 0
        self.dirty = False


class CacheSet:
    def __init__(self, associativity):
        self.lines = self.create_lines(associativity)

    def create_lines(self, associativity):
        cache_lines = [ChacheLine() for _ in range(associativity)]
        return cache_lines


class CacheSimulator:
    def __init__(self, **kwargs) -> None:
        self.input_parameters = kwargs
        self.set_numbers = self.input_parameters["lines_number"] // self.input_parameters["set_associativity"]
        self.cache_memory = self.create_cache_memory(self.input_parameters["set_associativity"], self.set_numbers)
        self.all_read_counter = 0
        self.read_hit = 0
        self.write_hit = 0
        self.cache_miss = 0
        self.all_write_counter = 0
        self.main_memory_hit = 0

        self.time = 0

    def execute(self):
        with open(self.input_parameters["input_file_path"], "r") as input_file:
            input_commands = [linha.strip().split() for linha in input_file.readlines()]

        for command in input_commands:
            command_set_index = (int(command[0], 16) // self.input_parameters["line_size"]) % self.set_numbers
            command_set = self.cache_memory[command_set_index]
            if command[1] == "R":
                self.execute_read(command_set, command[0])
            else:
                self.execute_write(command_set, command[0])
        if self.input_parameters["replacement_policy"] == 1:
            self.execute_write_back()
        self.generate_output_file()

    def execute_write_back(self):
        for set in self.cache_memory:
            for line in set.lines:
                if line.dirty:
                    self.time += self.input_parameters["main_memory_time"]

    def create_cache_memory(self, set_associativity, set_numbers):
        cache_memory = [CacheSet(set_associativity) for _ in range(set_numbers)]
        return cache_memory

    def execute_read(self, command_set, address):
        self.all_read_counter += 1
        if self.search_on_cache(command_set, address):
            self.read_hit += 1

    def execute_write(self, command_set, address):
        self.all_write_counter += 1
        if self.search_on_cache(command_set, address, True):
            self.write_hit += 1

    def search_on_cache(self, command_set, address, write=False):
        for line in command_set.lines:
            if line.address == address:
                line.last_hit_time = self.time
                line.access_counter += 1
                self.time += self.input_parameters["hit_time"]
                return True
        self.time += self.input_parameters["hit_time"] + self.input_parameters["main_memory_time"]
        self.cache_miss += 1
        self.change_line(command_set, address, write)
        return False

    def change_line(self, command_set, address, write):
        if self.input_parameters["replacement_policy"] == 0:
            line_to_change = min(command_set.lines, key=lambda linha: linha.access_counter)
        elif self.input_parameters["replacement_policy"] == 1:
            line_to_change = min(command_set.lines, key=lambda linha: linha.last_hit_time)
        else:
            line_to_change = random.choice(command_set.lines)

        if self.input_parameters["replacement_policy"] == 0:
            self.time += self.input_parameters["main_memory_time"]
        elif self.input_parameters["replacement_policy"] == 1 and line_to_change.dirty:
            self.time += self.input_parameters["main_memory_time"]

        line_to_change.address = address
        line_to_change.last_hit_time = self.time
        line_to_change.access_counter = 1
        line_to_change.dirty = write
        return line_to_change

    def generate_output_file(self):
        with open(
            f"{self.input_parameters['output_file_directory']}/{self.input_parameters['output_file_name']}.txt",
            "w",
        ) as output_file:
            output_file.write("##Result##\n")
            output_file.write(f"- Leituras: {self.all_read_counter}\n")
            output_file.write(f"- Acertos de Leitura: {self.read_hit}\n")
            output_file.write(f"- Escritas: {self.all_write_counter}\n")
            output_file.write(f"- Acertos de Escrita: {self.write_hit}\n")
            output_file.write(f"- Acetos Totais: {self.read_hit + self.write_hit}\n")
            output_file.write(f"- Acessos à Memória Principal: {self.cache_miss}\n")
            output_file.write(f"- Tempo Simulação (ns): {self.time:.4f}\n\n")
            for name, item in self.input_parameters.items():
                output_file.write(f"+ {name} = {item}\n")

    def generate_graph_file(self, x, y, title, xlabel, ylabel, filename):
        plt.figure()
        plt.plot(x, y, marker='o')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)
        plt.savefig(filename)
        plt.close()
