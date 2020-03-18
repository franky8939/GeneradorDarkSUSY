#!/bin/bash       
                                                                                                                                             
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=2
#SBATCH --distribution=cyclic:cyclic
##SBATCH --out=out.txt


#SBATCH --job-name=DarkSUSY_CMS                                                                                                                                 
#SBATCH --time=168:0:0                                                                                                                                          
#SBATCH --partition=general                                                                                                                                    
#SBATCH --constraint=broadwell                                                                                                                                 

srun python genera_v5.py
