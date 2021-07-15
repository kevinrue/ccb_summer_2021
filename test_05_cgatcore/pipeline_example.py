
import sys
import os

from ruffus import transform, suffix, merge
from cgatcore import pipeline as P


# load options from the config file
PARAMS = P.get_parameters(
    ["%s/pipeline.yml" % os.path.splitext(__file__)[0],
    "../pipeline.yml",
    "pipeline.yml"])

print(f"integer = {PARAMS['integer']}")
print(f"string = {PARAMS['string']}")

@transform( '*.input', suffix('.input'), '.output')
def copy( infile, outfile ):
    job_threads = 2
    job_memory = "1G"
    to_cluster = False

    statement = '''cp -v %(infile)s %(outfile)s'''

    P.run(statement, job_condaenv='cgatcore')


@transform( copy, suffix('.output'), '.lines')
def count_lines( infile, outfile ):
    job_threads = 2
    job_memory = "1G"
    to_cluster = False

    statement = '''wc -l %(infile)s > %(outfile)s'''

    P.run(statement, job_condaenv='cgatcore')


@merge(count_lines, 'output.concatenate.lines')
def concatenate( infiles, outfile ):
    job_threads = 2
    job_memory = "1G"
    to_cluster = False

    infiles_str = " ".join(infiles)

    number_lines = PARAMS['integer']

    # Warning: 'head' generates a harmless pipe error, because it returns
    # and is not there any more to catch the rest of the pipe'd information/
    statement = '''cat %(infiles_str)s
        | head -n %(number_lines)s
        > %(outfile)s'''

    P.run(statement, job_condaenv='cgatcore')


if __name__ == "__main__":
    sys.exit(P.main(sys.argv))
