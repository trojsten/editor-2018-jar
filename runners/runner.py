import logging

logging.basicConfig(level=logging.INFO)


class Runner:
    # Variables.
    # If you add new variables, modify load_vars, save_vars and initrunner
    INT_VECTORS = ["vi1", "vi2"]
    STR_VECTORS = ["vs1", "vs2"]
    INTS = ["i1", "i2"]
    STRS = ["s"]
    NAME = ''

    def __init__(self):
        pass

    def load_vars(self):
        code = ''
        for vector in self.INT_VECTORS:
            code += self.load_int_vector(vector)

        for intt in self.INTS:
            code += self.load_int(intt)

        for vector in self.STR_VECTORS:
            code += self.load_str_vector(vector)

        for strr in self.STRS:
            code += self.load_str(strr)

        return code

    def save_vars(self):
        code = ''
        for vector in self.INT_VECTORS:
            code += self.save_int_vector(vector)

        for intt in self.INTS:
            code += self.save_int(intt)

        for vector in self.STR_VECTORS:
            code += self.save_str_vector(vector)

        for strr in self.STRS:
            code += self.save_str(strr)

        return code

    def begin_ceremony(self):
        """Override me to generate code at the beginning of file (headers)."""
        pass

    def end_ceremony(self):
        """Override me to generate code at the end of file (closing files)."""
        pass

    def load_int_vector(self, vector):
        """Override me. Code that loads vectors of ints."""
        pass

    def load_str_vector(self, vector):
        """Override me. Code that loads vectors of strings."""
        pass

    def load_int(self, intt):
        """Override me. Code that loads ints."""
        pass

    def load_str(self, strr):
        """Override me. Code that loads string."""
        pass

    def save_int_vector(self, vector):
        """Override me. Code that saves vectors of ints."""
        pass

    def save_str_vector(self, vector):
        """Override me. Code that saves vectors of trings."""
        pass

    def save_int(self, intt):
        """Override me. Code that saves ints."""
        pass

    def save_str(self, strr):
        """Override me. Code that saves strings."""
        pass

    def generate(self, code):
        """Generates the whole code."""
        code = (
          self.begin_ceremony() + '\n' +
          self.load_vars() + '\n' +
          code + '\n' +
          self.save_vars() + '\n' +
          self.end_ceremony()
        )
        return code

    def prepare(self, codename):
        """Override me. Prepare code so it can be run (compile)."""
        pass

    def execute(self, codename, in_memory, out_memory):
        """Override me. Execute the generated code. """
        pass

    def simle_full_run(self, code,  codename, in_memory, out_memory):
        logging.info('Open')
        logging.info(codename)
        code_file = open(codename, 'w')
        logging.info('Generate')
        code_file.write(self.generate(code))
        code_file.close()
        logging.info('Prepare')
        self.prepare(codename)
        logging.info('execute')
        self.execute(codename, in_memory, out_memory)


class InitRunner(Runner):
    def create_init_memory(self, memory):
        memory = open(memory, 'w')
        for vector in self.INT_VECTORS:
            print(vector + " 0", file=memory)

        for intt in self.INTS:
            print(intt + " 0", file=memory)

        for vector in self.STR_VECTORS:
            print(vector + " 0", file=memory)

        for strr in self.STRS:
            print(strr + "\nss", file=memory)
        memory.close()

    def load_memory(self, memory):
        memory = open(memory, 'r')
        variables = {}
        for vector in self.INT_VECTORS:
            line = memory.readline().split()
            vector_name = line[0]
            assert vector == vector_name
            variables[vector_name] = list(map(int, line[2:]))

        for intt in self.INTS:
            line = memory.readline().split()
            intt_name = line[0]
            assert intt == intt_name
            variables[intt_name] = int(line[1])

        for vector in self.STR_VECTORS:
            line = memory.readline().split()
            vector_name, vector_size = line[0], line[1]
            assert vector == vector_name
            variables[vector_name] = []
            for x in range(int(vector_size)):
                variables[vector_name].append(memory.readline())

        for strr in self.STRS:
            strr_name = memory.readline().strip()
            assert strr == strr_name, strr_name + " " + strr
            variables[strr_name] = memory.readline().strip()
        memory.close()
        return variables


if __name__ == '__main__':
    init = InitRunner()
    init.create_init_memory('tmp/memory_init.txt')
    print(init.load_memory('tmp/memory_init.txt'))
