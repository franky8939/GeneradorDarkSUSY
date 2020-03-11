#!/bin/bash                                                                                                                                                    
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=20
#SBATCH --job-name=DarkSUSY_CMS                                                                                                                                 
#SBATCH --time=168:0:0                                                                                                                                          
#SBATCH --partition=general                                                                                                                                    
#SBATCH --constraint=broadwell                                                                                                                                 

srun python genera_v4.py
