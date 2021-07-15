import sys
import re
from ruffus import *
from cgatcore import pipeline as P


## Example 1
@transform( '*.Rmd', suffix('.Rmd'), '.html')
def compile_rmd( infile, outfile ):
    job_threads = 1
    job_memory = "60G"
    to_cluster = True

    statement = '''
    R -e "rmarkdown::render(
        '%(infile)s',
        output_file='%(outfile)s',
        params = list(
            integer = 1L,
            string = 'something'
        )
    )"
    '''

    P.run(statement, job_condaenv='cgatcore')


## Example 2
@transform( '*.Rmd', suffix('.Rmd'), '.html')
def compile_rmd( infile, outfile ):
    job_threads = 1
    job_memory = "60G"
    to_cluster = True

    # outfile = 'output.pc_10.param1_1.param2_a.html'
    pc = re.compile('output.pc_(.*).param1_(.*).param2_(.*).html').search(outfile).group(1)
    param1 = re.compile('output.pc_(.*).param1_(.*).param2_(.*).html').search(outfile).group(2)
    param2 = re.compile('output.pc_(.*).param1_(.*).param2_(.*).html').search(outfile).group(3)

    statement = '''
    R -e "rmarkdown::render(
        '%(infile)s',
        output_file='%(outfile)s',
        params = list(
            pc = %(pc)s,
            param1 = %(param1)s,
            param2 = '%(param1)s'
        )
    )"
    '''

    P.run(statement, job_condaenv='cgatcore')


if __name__ == "__main__":
    sys.exit(P.main(sys.argv))
