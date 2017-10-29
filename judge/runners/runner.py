import logging

logging.basicConfig(level=logging.INFO)


class Runner:
    # Variables.
    # If you add new variables, modify load_vars, save_vars and initrunner
    #  TODO zmente nazvy na nieco aspon trochu vtipne.
    SOME_INT_VECTOR = "vector_intov"
    SOME_STR_VECTOR = "vector_stringov"
    SOME_FLOAT_VECTOR = "vector_floatov"
    SOME_INT = "intt"
    SOME_STR = "stringg"
    SOME_FLOAT = "floatik"

    INT_VECTORS = [SOME_INT_VECTOR]
    STR_VECTORS = [SOME_STR_VECTOR]
    FLOAT_VECTORS = [SOME_FLOAT_VECTOR]
    INTS = [SOME_INT]
    STRS = [SOME_STR, "string2"]
    FLOATS = [SOME_FLOAT]
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

        for vector in self.FLOAT_VECTORS:
            code += self.load_float_vector(vector)

        for floatt in self.FLOATS:
            code += self.load_float(floatt)

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

        for vector in self.FLOAT_VECTORS:
            code += self.save_float_vector(vector)

        for floats in self.FLOATS:
            code += self.save_float(floats)

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

    def load_float_vector(self, vector):
        """Override me. Code that loads vectors of floats.
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

    def load_float(self, floatt):
        """Override me. Code that loads floats.                Returns:
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

    def save_float_vector(self, vector):
        """Override me. Code that saves vectors of floats.
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

    def save_float(self, floatt):
        """Override me. Code that saves floats.
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
            print("VECTOR_INT:\n" + vector + "\n0", file=memory)

        for intt in self.INTS:
            print("INT:\n" + intt + "\n0", file=memory)

        for vector in self.STR_VECTORS:
            print("VECTOR_STR:\n" + vector + "\n0", file=memory)

        for strr in self.STRS:
            print("STR:\n" + strr + "\n", file=memory)

        for vector in self.FLOAT_VECTORS:
            print("VECTOR_FLOAT:\n" + vector + "\n0", file=memory)

        for floatt in self.FLOATS:
            print("FLOAT:\n" + floatt + "\n0", file=memory)
        memory.close()

    def load_memory(self, memory):
        memory = open(memory, 'r')
        variables = {}
        for vector in self.INT_VECTORS:
            _ = memory.readline().strip()
            vector_name = memory.readline().strip()
            vector_size = int(memory.readline().strip())
            assert vector == vector_name
            variables[vector_name] = [int(memory.readline().strip()) for _ in range(vector_size)]

        for intt in self.INTS:
            _ = memory.readline().strip()
            intt_name = memory.readline().strip()
            intt_value = memory.readline().strip()
            assert intt == intt_name
            variables[intt_name] = int(intt_value)

        for vector in self.STR_VECTORS:
            _ = memory.readline().strip()
            vector_name = memory.readline().strip()
            vector_size = int(memory.readline().strip())
            assert vector == vector_name
            variables[vector_name] = [memory.readline().strip() for _ in range(vector_size)]

        for strr in self.STRS:
            _ = memory.readline().strip()
            strr_name = memory.readline().strip()
            strr_value = memory.readline().strip()
            assert strr == strr_name
            variables[strr_name] = strr_value

        for vector in self.FLOAT_VECTORS:
            _ = memory.readline().strip()
            vector_name = memory.readline().strip()
            vector_size = int(memory.readline().strip())
            assert vector == vector_name
            variables[vector_name] = [float(memory.readline().strip()) for _ in range(vector_size)]

        for floatt in self.FLOATS:
            _ = memory.readline().strip()
            floatt_name = memory.readline().strip()
            floatt_value = float(memory.readline().strip())
            assert floatt == floatt_name
            variables[floatt_name] = int(floatt_value)

        memory.close()
        return variables


if __name__ == '__main__':
    init = InitRunner()
    init.create_init_memory('tmp/memory_init.txt')
    print(init.load_memory('tmp/memory_init.txt'))
