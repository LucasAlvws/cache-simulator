import math
import random
import matplotlib.pyplot as plt


class ChacheLine:
    def __init__(
        self, tag=None, last_hit_time=0, access_counter=0, dirty=False, clean=True
    ):
        self.tag = tag
        self.last_hit_time = last_hit_time
        self.access_counter = access_counter
        self.dirty = dirty
        self.clean = clean


class CacheSet:
    def __init__(self, associativity):
        self.lines = self.create_lines(associativity)

    def create_lines(self, associativity):
        cache_lines = [ChacheLine() for _ in range(associativity)]
        return cache_lines


class CacheSimulator:
    def __init__(self, **kwargs) -> None:
        self.input_parameters = kwargs
        self.set_numbers = (
            self.input_parameters["lines_number"]
            // self.input_parameters["set_associativity"]
        ) or 1
        self.cache_memory = self.create_cache_memory(
            self.input_parameters["set_associativity"], self.set_numbers
        )

        self.word_size = int(self.input_parameters["line_size_pot"])
        if self.set_numbers == 1:
            self.set_size = 1
        else:
            self.set_size = int(math.log2(self.set_numbers))
        self.label_size = int(32 - self.set_size - self.word_size)

        self.all_read_counter = 0
        self.all_write_counter = 0

        self.main_memory_read = 0
        self.main_memory_write = 0

        self.cache_read_hit = 0
        self.cache_write_hit = 0

        self.time = 0

    def execute(self):
        with open(self.input_parameters["input_file_path"], "r") as input_file:
            input_commands = [linha.strip().split() for linha in input_file.readlines()]

        for command in input_commands:
            tag, index, _ = self.get_indices(command[0])
            command_set = self.cache_memory[index]
            if command[1] == "R":
                self.execute_read(command_set, tag)
            else:
                self.execute_write(command_set, tag)

        if self.input_parameters["replacement_policy"] == 1:
            self.execute_write_back()
        self.time = (
            self.input_parameters["hit_time"]
            * (self.cache_read_hit + self.cache_write_hit)
        ) + (
            self.input_parameters["main_memory_time"]
            * (self.main_memory_read + self.main_memory_write)
        )
        self.generate_output_file()

    def get_indices(self, address):
        address_bin = bin(int(address, 16))[2:].zfill(32)
        tag = int(address_bin[: self.label_size], 2)
        if self.set_size == 1:
            index = 0
        else:
            index = int(address_bin[self.label_size : self.label_size + self.set_size], 2)
        offset = int(address_bin[-self.word_size :], 2)

        return tag, index, offset

    def execute_write_back(self):
        for set in self.cache_memory:
            for line in set.lines:
                if line.dirty:
                    self.main_memory_write += 1

    def create_cache_memory(self, set_associativity, set_numbers):
        cache_memory = [CacheSet(set_associativity) for _ in range(set_numbers)]
        return cache_memory

    def execute_read(self, command_set, tag):
        self.all_read_counter += 1
        self.search_on_cache(command_set, tag)

    def execute_write(self, command_set, tag):
        self.all_write_counter += 1

        self.search_on_cache(command_set, tag, True)

    def search_on_cache(self, command_set, tag, write=False):
        for line in command_set.lines:
            if line.tag == tag:
                if write:
                    self.cache_write_hit += 1
                    if self.input_parameters["writing_policy"] == 0:
                        self.main_memory_write += 1
                    else:
                        line.dirty = True
                else:
                    self.cache_read_hit += 1
                line.last_hit_time = self.time
                line.access_counter += 1
                return True
        if write and self.input_parameters["writing_policy"] == 0:
            self.main_memory_write += 1
        self.bring_set_to_cache(command_set, tag)
        return False

    def bring_set_to_cache(self, command_set, tag):
        self.main_memory_read += 1
        for line in command_set.lines:
            if line.clean:
                line.tag = tag
                line.last_hit_time = self.time
                line.access_counter = 1
                line.clean = False
                return

        if self.input_parameters["replacement_policy"] == 0:
            line_to_change = min(
                command_set.lines, key=lambda line: line.access_counter
            )
        elif self.input_parameters["replacement_policy"] == 1:
            line_to_change = min(command_set.lines, key=lambda line: line.last_hit_time)
        else:
            line_to_change = random.choice(command_set.lines)

        if self.input_parameters["writing_policy"] == 1 and line_to_change.dirty:
            self.main_memory_write += 1

        command_set.lines.remove(line_to_change)

        new_line = ChacheLine(tag, clean=False)
        command_set.lines.append(new_line)

    def generate_output_file(self):
        with open(
            f"{self.input_parameters['output_file_directory']}/{self.input_parameters['output_file_name']}.txt",
            "w",
        ) as output_file:
            output_file.write("##Result##\n")
            output_file.write(f"- Leituras: {self.all_read_counter}\n")
            output_file.write(f"- Escritas: {self.all_write_counter}\n")
            output_file.write(
                f"- Total: {self.all_write_counter + self.all_read_counter}\n"
            )
            output_file.write("\n")
            output_file.write(f"- Acertos de Leitura: {self.cache_read_hit}\n")
            output_file.write(f"- Acertos de Escrita: {self.cache_write_hit}\n")
            output_file.write(
                f"- Acertos Totais: {self.cache_read_hit + self.cache_write_hit}\n"
            )
            output_file.write("\n")
            output_file.write(
                f"- Acessos read à Memória Principal: {self.main_memory_read}\n"
            )
            output_file.write(
                f"- Acessos write à Memória Principal: {self.main_memory_write}\n"
            )
            output_file.write(
                f"- Acessos Totais à Memória Principal: {self.main_memory_read + self.main_memory_write}\n"
            )
            output_file.write("\n")
            taxa_hit = ((self.cache_read_hit + self.cache_write_hit) * 100) / (self.all_write_counter + self.all_read_counter)
            output_file.write(
                f"- Taxa de hit total: {taxa_hit:.4f}%\n"
            )

            output_file.write(f"- Tempo Simulação (ns): {self.time:.4f}\n\n")
            media = self.input_parameters['hit_time'] + (1 - taxa_hit/100)* self.input_parameters['main_memory_time']
            output_file.write(f"- Tempo Médio (ns): {media:.4f}\n\n")
            for name, item in self.input_parameters.items():
                output_file.write(f"+ {name} = {item}\n")

    def generate_graph_file(self, x, y, title, xlabel, ylabel, filename):
        plt.figure()
        plt.plot(x, y, marker="o")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)
        plt.savefig(filename)
        plt.close()
