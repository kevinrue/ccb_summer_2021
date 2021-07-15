#!/bin/bash
#SBATCH --partition=batch
#SBATCH --job-name=kevin_test_copy
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=00-00:01:00
#SBATCH --output=%j_%x.out
#SBATCH --error=%j_%x.err
#SBATCH --mail-user=kevin.rue-albrecht@imm.ox.ac.uk
#SBATCH --mail-type=end,fail

cd /stopgap/sims-lab/albrecht/test_03_rmd

module load R-cbrg/202106

R -e "rmarkdown::render('script.Rmd', output_file='output.html')"
