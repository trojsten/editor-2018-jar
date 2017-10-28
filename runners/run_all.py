from runner_python import PythonRunner
from runner_cpp import CppRunner
from runner import InitRunner, Runner
import logging
import re

logging.basicConfig(level=logging.INFO)

runners = [PythonRunner, CppRunner]

REGISTER = {r.NAME: r for r in runners}


class MasterRunner:
    def __init__(self, code):
        self.code = code
        self.runners = []
        self.location = 'tmp/runer{}'

    def prepare(self):
        """
        Args:
          code (list[pairs[code, language]]): code.
        """
        for i, (line, language) in enumerate(self.code):
            special_match = re.match("IF (.*) IS NOT ZERO GOTO (\d*)", line)
            if special_match is None:
                runner = REGISTER[language](line, self.location.format(i))
                # TODO catch errors
                prepare_status = runner.prepare()
                if prepare_status != 0:
                    return "CERR", line+1, prepare_status
                self.runners.append(runner)
            else:
                groups = special_match.groups()
                self.runners.append((groups[0], int(groups[1])))
        return None

    def run(self, input_file):
        counter = 0
        line = 0
        last_memory = input_file
        init_runner = InitRunner()
        while line < len(self.runners):
            counter += 1
            runner = self.runners[line]
            if not isinstance(runner, tuple):
                logging.info('Line %d, counter %d, runner %s', line, counter, runner.NAME)
                out_memory = self.location.format("_mem_"+str(counter))
                logging.info('From: %s, To: %s', last_memory, out_memory)
                execute_status = self.runners[line].execute(last_memory, out_memory)
                if execute_status != 0:
                    return "EXEC", line+1, execute_status
                last_memory = out_memory
                line += 1
            else:
                logging.info('Jupming on line: %d', line)
                variable = runner[0]
                to_line = runner[1]-1
                memory = init_runner.load_memory(last_memory)
                logging.info('Memory: %s = %d', variable, memory[variable])

                if memory[variable] != 0:
                    line = to_line
                else:
                    line += 1

        logging.info('Reading final memory: %s', last_memory)
        memory = init_runner.load_memory(last_memory)
        return memory


if __name__ == "__main__":
    code = [
      [Runner.SOME_STR_VECTOR + '.append("P1")', 'Python'],
      [Runner.SOME_STR_VECTOR + '.push_back("C1");', 'C++'],
      [Runner.SOME_STR_VECTOR + '.append("P2")', 'Python'],
      [Runner.SOME_STR_VECTOR + '.push_back("C2");', 'C++'],
    ]
    init = InitRunner()
    init.create_init_memory('tmp/memory.txt')
    master = MasterRunner(code)
    master.prepare()
    memory = master.run('tmp/memory.txt')
    print(memory[Runner.SOME_STR_VECTOR])
    assert memory[Runner.SOME_STR_VECTOR] == ["P1", "C1", "P2", "C2"]

    # CODE 2 with flow control
    code2 = [
      [Runner.SOME_INT + '=5', 'Python'],
      [Runner.SOME_STR + '=""', 'Python'],
      [Runner.SOME_STR + '+="a"', 'Python'],
      [Runner.SOME_INT + '-=1', 'Python'],
      ['IF ' + Runner.SOME_INT + ' IS NOT ZERO GOTO 3', 'C++'],
    ]

    init = InitRunner()
    init.create_init_memory('tmp/memory.txt')
    master = MasterRunner(code2)
    master.prepare('tmp/c_python2')
    memory = master.run('tmp/memory.txt')
    print(memory[Runner.SOME_STR])
    print(memory[Runner.SOME_INT])
    assert memory[Runner.SOME_STR] == "aaaaa"
