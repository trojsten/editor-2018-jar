import logging
logging.basicConfig(level=logging.INFO)


class Runner:
    # Variables.
    # If you add new variables, modify load_vars, save_vars and initrunner
    #  TODO zmente nazvy na nieco aspon trochu vtipne.
    NAME = ''

    def __init__(self, code, codename, variables=None):
        """
        variables should be a dict of a form: <type>: <variable names with given name>
        {
            "INT_VECTORS": ["koza", "capko"],
            "STR_VECTORS": ["vr", "rv"],
            "FLOAT_VECTORS": ["omg", "lol"],
            "INTS": ["bobek", "bobok"],
            "STRS": ["gold", "silver"],
            "FLOATS": ["wilager"]
        }        """
        self.code = code
        self.codename = codename
        if variables is not None:
            self.INT_VECTORS = variables.get('INT_VECTORS', [])
            self.STR_VECTORS = variables.get('STR_VECTORS', [])
            self.FLOAT_VECTORS = variables.get('FLOAT_VECTORS', [])
            self.INTS = variables.get('INTS', [])
            self.STRS = variables.get('STRS', [])
            self.FLOATS = variables.get('FLOATS', [])
        else:
            # defaultne harry potter mena premennych
            self.INT_VECTORS = ["kotlik", "hrniec"]
            self.STR_VECTORS = ["kniha", "miska"]
            self.FLOAT_VECTORS = ["magia", "maziar"]
            self.INTS = ["jedna", "dumbier", "mandragora", "netopier"]
            self.STRS = ["zaba", "recept", "zaklinadlo", "jednorozec"]
            self.FLOATS = ["pomer", "tricelestrnast", "mana"]


        safe_zero = lambda x: None if len(x)==0 else x[0]
        
        self.SOME_INT_VECTOR = safe_zero(self.INT_VECTORS)
        self.SOME_STR_VECTOR = safe_zero(self.STR_VECTORS)
        self.SOME_FLOAT_VECTOR = safe_zero(self.FLOAT_VECTORS)
        self.SOME_INT = safe_zero(self.INTS)
        self.SOME_STR = safe_zero(self.STRS)
        self.SOME_FLOAT = safe_zero(self.FLOATS)
        

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
            str: exit message (compilation error message)
        """
        pass

    def execute(self, in_memory, out_memory):
        """Override me. Execute the generated code.
        Returns:
            int: exit status
            str: exit message (what went wrong)
        """
        pass

    def simple_full_run(self, in_memory, out_memory):
        logging.info('Prepare')
        prepare_status = self.prepare()
        logging.info("Prepare status: %s", prepare_status)
        logging.info('Execute')
        execute_status = self.execute(in_memory, out_memory)
        logging.info("Execute status: %s", execute_status)


if __name__ == '__main__':
    pass
