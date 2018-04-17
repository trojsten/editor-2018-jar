from runners.runner import Runner
from runners.init_runner import InitRunner
import os

the_genesis = '''
fn get_line(input: &mut std::io::BufRead) -> String {
    let mut line = String::new();
    input.read_line(&mut line).expect("failed to read line");
    let len = line.len();
    line[..len - 1].to_string()
}

fn get_value<T>(input: &mut std::io::BufRead) -> T
where
    T: std::str::FromStr,
    <T as std::str::FromStr>::Err: std::fmt::Debug,
{
    get_line(input).parse::<T>().expect("failed to parse value")
}

fn get_it<T>(input: &mut std::io::BufRead) -> T
where
    T: std::str::FromStr,
    <T as std::str::FromStr>::Err: std::fmt::Debug,
{
    get_line(input); // <TYPE>
    get_line(input); // <name>
    get_value(input) // <value>
}

fn get_vec<T>(input: &mut std::io::BufRead) -> Vec<T>
where
    T: std::str::FromStr,
    <T as std::str::FromStr>::Err: std::fmt::Debug,
{
    get_line(input); // <TYPE>
    get_line(input); // <name>
    let len = get_value::<usize>(input); // <len>
    (0..len).map(|_| get_value::<T>(input)).collect() // <values...>
}

fn put_it<T>(output: &mut std::io::Write, typ: &str, name: &str, x: T)
where
    T: std::fmt::Display,
{
    writeln!(output, "{}", typ).unwrap();
    writeln!(output, "{}", name).unwrap();
    writeln!(output, "{}", x).unwrap();
}

fn put_vec<T>(output: &mut std::io::Write, typ: &str, name: &str, xs: Vec<T>)
where
    T: std::fmt::Display,
{
    writeln!(output, "{}", typ).unwrap();
    writeln!(output, "{}", name).unwrap();
    writeln!(output, "{}", xs.len()).unwrap();
    for x in xs {
        writeln!(output, "{}", x).unwrap();
    }
}

fn main() {
    let mut args = std::env::args();
    args.next();
    let input_name = args.next().expect("input file name not provided");
    let output_name = args.next().expect("output file name not provided");
    let mut input_file = std::fs::File::open(input_name).expect("error opening input file");
    let mut output_file = std::fs::File::create(output_name).expect("error creating output file");
    let mut input = std::io::BufReader::new(input_file);
    let mut output = std::io::BufWriter::new(output_file);
'''

the_apocalypse = '''
}
'''


class RustRunner(Runner):
    NAME = "Rust"

    def begin_ceremony(self):
        return the_genesis

    def end_ceremony(self):
        return the_apocalypse

    def load_int(self, name):
        return '''
        let mut {0} = get_it::<i64>(&mut input);
        '''.format(name)

    def load_float(self, name):
        return '''
        let mut {0} = get_it::<f64>(&mut input);
        '''.format(name)

    def load_str(self, name):
        return '''
        let mut {0} = get_it::<String>(&mut input);
        '''.format(name)

    def load_int_vector(self, name):
        return '''
        let mut {0} = get_vec::<i64>(&mut input);
        '''.format(name)

    def load_float_vector(self, name):
        return '''
        let mut {0} = get_vec::<f64>(&mut input);
        '''.format(name)

    def load_str_vector(self, name):
        return '''
        let mut {0} = get_vec::<String>(&mut input);
        '''.format(name)

    def save_int(self, name):
        return '''
        put_it(&mut output, "INT:", "{0}", {0});
        '''.format(name)

    def save_float(self, name):
        return '''
        put_it(&mut output, "FLOAT:", "{0}", {0});
        '''.format(name)

    def save_str(self, name):
        return '''
        put_it(&mut output, "STR:", "{0}", {0});
        '''.format(name)

    def save_int_vector(self, name):
        return '''
        put_vec(&mut output, "VECTOR_INT:", "{0}", {0});
        '''.format(name)

    def save_float_vector(self, name):
        return '''
        put_vec(&mut output, "VECTOR_FLOAT:", "{0}", {0});
        '''.format(name)

    def save_str_vector(self, name):
        return '''
        put_vec(&mut output, "VECTOR_STR:", "{0}", {0});
        '''.format(name)

    def prepare(self):
        filename = self.codename + ".rs"
        f = open(filename, "w")
        f.write(self.generate())
        f.close()
        log_fname = "{}.compile_log".format(self.codename)
        cmd = 'rustc -o {} {} 2>{}'.format(self.codename, filename, log_fname)
        #logging.info("Running: %s", cmd)
        return os.system(cmd), open(log_fname).read()

    def execute(self, in_memory, out_memory):
        log_fname = "{}.runtime_log".format(self.codename)
        cmd = './{} {} {} 2> {}'.format(self.codename, in_memory, out_memory, log_fname)
        #logging.info('Executing: %s', cmd)
        return os.system(cmd), open(log_fname).read()


if __name__ == '__main__':
    init = InitRunner()
    init.create_init_memory('tmp/memory.txt')
    runner = RustRunner(
      '{0} = vec!["0".to_string(), "2".to_string(), "4".to_string(), "6".to_string()];'.format(
        init.SOME_STR_VECTOR), 'tmp/tmp')
    runner.simple_full_run('tmp/memory.txt', 'tmp/memory2_rust.txt')
    print(init.load_memory('tmp/memory2_rust.txt'))
    runner2 = RustRunner('{0} = 0.11;'.format(
      init.SOME_FLOAT), 'tmp/tmp')
    runner2.simple_full_run('tmp/memory2_rust.txt', 'tmp/memory3_rust.txt')
    print(init.load_memory('tmp/memory3_rust.txt'))
