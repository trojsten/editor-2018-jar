import logging

logging.basicConfig(level=logging.INFO)


class Runner:
    # Variables.
    # If you add new variables, modify load_vars, save_vars and initrunner
    SOME_INT_VECTOR = "vstring"
    SOME_STR_VECTOR = "vs1"
    SOME_INT = "stringg"
    SOME_STR = "vector"
    SOME_FLOAT = "intt"

    INT_VECTORS = [SOME_INT_VECTOR, "chcem_float", "bilbo"]
    STR_VECTORS = [SOME_STR_VECTOR, "nemam_for"]
    INTS = [SOME_INT, "nemam_while"]
    STRS = [SOME_STR, "nemam_if"]
    NAME = ''

    def __init__(self, code, codename):
        self.code = code
        self.codename = codename
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
        """Override me to generate code at the beginning of file (headers).
        Returns:
            str: code
        """
        pass

    def end_ceremony(self):
        """Override me to generate code at the end of file (closing files).
        Returns:
            str: code
        """

        pass

    def load_int_vector(self, vector):
        """Override me. Code that loads vectors of ints.
                Returns:
            str: code
        """
        pass

    def load_str_vector(self, vector):
        """Override me. Code that loads vectors of strings.
                Returns:
            str: code
        """
        pass

    def load_int(self, intt):
        """Override me. Code that loads ints.                Returns:
            str: code
        """
        pass

    def load_str(self, strr):
        """Override me. Code that loads string.
        Returns:
            str: code
        """
        pass

    def save_int_vector(self, vector):
        """Override me. Code that saves vectors of ints.
        Returns:
            str: code
        """
        pass

    def save_str_vector(self, vector):
        """Override me. Code that saves vectors of trings.
        Returns:
            str: code
        """
        pass

    def save_int(self, intt):
        """Override me. Code that saves ints.
        Returns:
            str: code
        """
        pass

    def save_str(self, strr):
        """Override me. Code that saves strings.
        Returns:
            str: code
        """
        pass

    def generate(self):
        """Generates the whole code."""
        code = (
          self.begin_ceremony() + '\n' +
          self.load_vars() + '\n' +
          self.code + '\n' +
          self.save_vars() + '\n' +
          self.end_ceremony()
        )
        return code

    def prepare(self):
        """Override me. Save code to file and prepare it so it can be run (compile it).
        Returns:
            int: exit status (non zero in case of compilation error)
        """
        pass

    def execute(self, in_memory, out_memory):
        """Override me. Execute the generated code.
        Returns:
            int: exit status
        """
        pass

    def simple_full_run(self, in_memory, out_memory):
        logging.info('Prepare')
        prepare_status = self.prepare()
        logging.info("Prepare status: %s", prepare_status)
        logging.info('Execute')
        execute_status = self.execute(in_memory, out_memory)
        logging.info("Execute status: %s", execute_status)


class InitRunner(Runner):
    def __init__(self):
        pass

    def create_init_memory(self, memory):
        memory = open(memory, 'w')
        for vector in self.INT_VECTORS:
            print(vector + " 0", file=memory)

        for intt in self.INTS:
            print(intt + " 0", file=memory)

        for vector in self.STR_VECTORS:
            print(vector + " 0", file=memory)

        for strr in self.STRS:
            print(strr + "\n", file=memory)
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
                variables[vector_name].append(memory.readline().strip())

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
