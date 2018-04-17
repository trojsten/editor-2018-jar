from runners.runner import Runner

import os
#import logging

#logging.basicConfig(level=logging.INFO)


class PerlRunner(Runner):

    NAME = 'Perl'

    def begin_ceremony(self):
        code = (
          'use strict;\n'+
          'my $tmpstr="";\n'+
          'open(my $in,  "<", $ARGV[0])  or die "Cant open";\n'+
          'open(my $out,  ">", $ARGV[1])  or die "Cant open";\n'
        )
        return code

    def end_ceremony(self):
        code = (
          'close $in;\n' +
          'close $out\n'
        )
        return code

    def load_int_vector(self, vector):
        code = (
          'my @' + vector + ' = ();\n' +
          'my $tmpstr  = <$in>;\n' +
          'my $tmpstr  = <$in>;\n' +
          'my $tmpstr  = <$in> + 0;\n' +
          '$#' + vector + ' = $tmpstr;\n' +
          'for my $tmpi (0 .. $tmpstr) {\n' + 
          '  $'+vector+'[$tmpi] = <$in>+0;\n' +
          '}\n'
        )
        return code

    def load_float_vector(self, vector):
        code = (
          'my @' + vector + ' = ();\n' +
          'my $tmpstr  = <$in>;\n' +
          'my $tmpstr  = <$in>;\n' +
          'my $tmpstr  = <$in> + 0;\n' +
          '$#' + vector + ' = $tmpstr;\n' +
          'for my $tmpi (0 .. $tmpstr) {\n' + 
          '  $'+vector+'[$tmpi] = <$in>+0.0;\n' +
          '}\n'
        )
        return code

    def load_str_vector(self, vector):
        code = (
          'my @' + vector + ' = ();\n' +
          'my $tmpstr  = <$in>;\n' +
          'my $tmpstr  = <$in>;\n' +
          'my $tmpstr  = <$in> + 0;\n' +
          '$#' + vector + ' = $tmpstr;\n' +
          'for my $tmpi (0 .. $tmpstr) {\n' + 
          '  $'+vector+'[$tmpi] = <$in>+"";\n' +
          '}\n'
        )
        return code

    def load_int(self, intt):
        code = (
          'my $tmpstr  = <$in>;\n' +
          'my $' + intt + ' = <$in>+0;\n'
        )
        return code

    def load_float(self, floatt):
        code = (
          'my $tmpstr  = <$in>;\n' +
          'my $' + floatt + ' = <$in>+0.0;\n'
        )
        return code

    def load_str(self, strr):
        code = (
          'my $tmpstr  = <$in>;\n' +
          'my $' + strr + ' = <$in>+"";\n'
        )
        return code

    def save_int_vector(self, vector):
        code = (
          'print $out "VECTOR_INT:\\n{}\\n";\n'.format(vector) +
          'print $out $#{}+1, "\\n";\n'.format(vector) +
          'for my $tmpi (0 .. $#%s) {\n'%(vector) + 
          '  print $out $%s[$tmpi],"\\n";\n'%(vector) +
          '}\n'
        )
        return code

    def save_float_vector(self, vector):
        code = (
          'print $out "VECTOR_FLOAT:\\n{}\\n";\n'.format(vector) +
          'print $out $#{}+1,"\\n";\n'.format(vector) +
          'for my $tmpi (0 .. $#%s) {\n'%(vector) + 
          '  print $out $%s[$tmpi],"\\n";\n'%(vector) +
          '}\n'
        )
        return code

    def save_str_vector(self, vector):
        code = (
          'print $out "VECTOR_STR:\\n{}\\n";\n'.format(vector) +
          'print $out $#{}+1,"\\n";\n'.format(vector) +
          'for my $tmpi (0 .. $#%s) {\n'%(vector) + 
          '  print $out $%s[$tmpi],"\\n";\n'%(vector) +
          '}\n'
        )
        return code

    def save_int(self, intt):
        code = (
          'print $out "INT:\\n{}\\n";\n'.format(intt) +
          'print $out ${},"\\n";\n'.format(intt)
        )
        return code

    def save_float(self, floatt):
        code = (
          'print $out "FLOAT:\\n{}\\n";\n'.format(floatt) +
          'print $out ${},"\\n";\n'.format(floatt)
        )
        return code

    def save_str(self, strr):
        code = (
          'print $out "STR:\\n{}\\n";\n'.format(strr) +
          'print $out ${},"\\n";\n'.format(strr)
        )
        return code

    def prepare(self):
        code_file = open(self.codename+".pl", "w")
        code_file.write(self.generate())
        code_file.close()
        return 0, ''

    def execute(self, in_memory, out_memory):
        log_fname = "{}.log_file".format(self.codename)
        cmd = 'perl {}.pl {} {} 2> {}'.format(self.codename, in_memory, out_memory, log_fname)
        return os.system(self.timeout(cmd)), open(log_fname).read()


if __name__ == '__main__':
    from runners.init_runner import InitRunner
    init = InitRunner()
    init.create_init_memory('tmp/memory.txt')
    init.create_init_memory('tmp/memory2_pl.txt')
    runner = PerlRunner(
      '@'+init.SOME_STR_VECTOR + '=("a","bb","dss");\n'+ 
      '@'+init.SOME_INT_VECTOR + '=(1,2,3);\n'+ 
      '@'+init.SOME_FLOAT_VECTOR + '=(11.0,21.0,31);\n'+
      '$'+init.SOME_INT + ' += $'+init.SOME_INT_VECTOR+'[1];\n',
      'tmp/tmp')
    runner.simple_full_run('tmp/memory.txt', 'tmp/memory2_pl.txt')
    mem = init.load_memory('tmp/memory2_pl.txt')
    assert mem[init.SOME_STR_VECTOR] == ["a","bb","dss"]
    assert mem[init.SOME_INT_VECTOR] == [1,2,3]
    assert mem[init.SOME_FLOAT_VECTOR] == [11.0,21.0,31]
    assert mem[init.SOME_INT] == 2
    