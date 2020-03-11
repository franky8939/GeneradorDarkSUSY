#!/bin/bash                                                                                                                                                    
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=DarkSUSY_clearandprepare                                                                                                                                
#SBATCH --time=168:0:0                                                                                                                                          
#SBATCH --partition=general                                                                                                                                    
#SBATCH --constraint=broadwell                                                                                                                                 

srun python Acarus_clear.py
