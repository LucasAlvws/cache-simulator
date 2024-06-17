class ChacheLine:
    def __init__(self):
        self.address = None
        self.last_hit_time = 0
        self.access_counter = 0


class CacheSet:
    def __init__(self, associativity):
        self.lines = self.create_lines(associativity)

    def create_lines(self, associativity):
        cache_lines = [ChacheLine() for _ in range(associativity)]
        return cache_lines

class CacheSimulator:
    def __init__(self, **kwargs) -> None:
        self.input_parameters = kwargs
        self.set_numbers = self.input_parameters['lines_number'] // self.input_parameters['set_associativity']
        self.cache_memory = self.create_cache_memory(
            self.input_parameters['set_associativity'], self.set_numbers
        )
        self.all_read_counter = 0
        self.read_hit = 0
        self.write_hit = 0
        self.all_write_counter = 0
        self.main_memory_hit = 0

    tempo_atual = 0

    def execute(self):
        with open(self.input_parameters['input_file_path'], "r") as input_file:
            input_commands = [linha.strip().split() for linha in input_file.readlines()]
        from IPython import embed

        embed(header="")
        for command in input_commands:
            if command['1'] == 'R':
                self.execute_read()
            else:
                self.execute_write()

    def create_cache_memory(self, set_associativity, set_numbers):
        cache_memory = [CacheSet(set_associativity) for _ in range(set_numbers)]
        return cache_memory

    def execute_read(self):
        self.all_read_counter += 1

    def execute_write(self):
        self.all_write_counter += 1

    def search_on_cache(self):
        pass

    def search_on_cache(self):
        pass

    def generate_output_file(self):
        with open(f"{self.input_parameters['output_file_directory']}/{self.input_parameters['output_file_name']}.txt", "w") as output_file:
            for name, item in self.input_parameters.items():
                output_file.write(f"{name} = {item}\n")
