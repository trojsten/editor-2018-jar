from runners.init_runner import InitRunner
from runners.run_all import MasterRunner

import sys
import os
import click
import json
import glob
import math

@click.command()
@click.option('--generate/--no-generate', default=False, help='Regenerate the folder')
@click.option('--test/--no-test', default=False, help='Test the solution')
@click.option('--test_sample', help='Test only one sample')
@click.option('--clean/--no-clean', default=True, help='Clean temporary files')
@click.option('--config_path', help='Path to config', required=True)
def main(generate, test, test_sample, clean, config_path):
    exec(open(config_path).read(), globals())
    task_path = os.path.dirname(config_path)
    if generate:
        json.dump(variables, open(task_path+'/variables.json', 'w'))

        init = InitRunner(variables)
        samples_names = "abcdefgh"
        # generate samples
        for i, (sample_input, sample_output) in enumerate(sample_input_output_pairs):
            init.prepare_memory(sample_input, task_path+"/00.{}.sample.in".format(samples_names[i]))
            json.dump(sample_output, open(task_path+"/00.{}.sample.out".format(samples_names[i]), 'w'))

        for i, (sample_input, sample_output) in enumerate(real_input_output_pairs):
            init.prepare_memory(sample_input, task_path+"/{0:02d}.in".format(i+1))
            json.dump(sample_output, open(task_path+"/{0:02d}.out".format(i+1), 'w'))
    else:
        print('Not generating anything, --generate')

    if test or test_sample is not None:
        master = MasterRunner(vzorak, prefix='_tmp_', variables=variables)
        result = master.prepare()
        print(result)
        count_ok = 0
        all_results = []
        for input_path in glob.glob(task_path + '/*.in'):
            if test_sample is not None and test_sample not in input_path:
                continue
            base = os.path.splitext(input_path)[0]
            result = master.run(input_path)
            print(result)
            message, line, diff = 'OK', 0, {}
            if isinstance(result, tuple):
                message = 'EXC'
                line = result[1]
            elif isinstance(result, dict):
                memory = result

                with open('%s.out' % base, 'r') as out_file:
                    output = json.loads(out_file.read())
                    ok = True
                    for premenna, hodnota in output.items():
                        # TODO: floaty su meh
                        if not compare(memory, premenna, hodnota, variables):
                            ok = False
                            diff[premenna] = (hodnota, memory[premenna])
                    if ok:
                        message = 'OK'
                        count_ok += 1
                    else:
                        message = 'WA'
            print(message, line)
            all_results.append((input_path, message, line))
            if len(diff) > 0:
                s = ''
                for premenna, (nasa, tvoja) in diff.items():
                    s += 'nas %s: %s\n' % (premenna, nasa)
                    s += 'tvoj %s: %s\n' % (premenna, tvoja)
                print(s)
        for result in all_results:
            print(result)

    else:
        print('Not testing anything, --test')

    if clean:
        files = [fname for fname in glob.glob(task_path+"/*") if '_tmp' in fname]
        for f in files:
            os.remove(f)
    else:
        print('Not cleaning anything, --clean')

def compare(memory, premenna, hodnota, variables):
    if premenna in variables['FLOATS']:
        return math.isclose(memory[premenna],hodnota, rel_tol=1e-05, abs_tol=0.00001)
    elif premenna in variables['FLOAT_VECTORS']:
        return all(list(map(lambda x:math.isclose(x[0],x[1],rel_tol=1e-05, abs_tol=0.00001), zip(memory[premenna],hodnota))))
    else:
        return hodnota == memory[premenna]



if __name__=="__main__":
    main()