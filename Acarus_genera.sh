#!/bin/bash       
                                                                                                                                             
#SBATCH --ntasks=20
#SBATCH --distribution=cyclic:cyclic
#SBATCH --out=generar.txt


#SBATCH --job-name=DarkSUSY                                                                                                                             
#SBATCH --time=168:0:0                                                                                                                                          
#SBATCH --partition=general                                                                                                                                    
#SBATCH --constraint=broadwell                                                                                                                                 

srun python genera_v5.py
