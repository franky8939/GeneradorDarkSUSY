#!/bin/bash                                                                                                                                                    


#SBATCH --job-name=DarkSUSY_clear_and_prepare                                                                                                                                
#SBATCH --time=168:0:0                                                                                                                                          
#SBATCH --partition=general                                                                                                                                    
#SBATCH --constraint=broadwell                                                                                                                                 
#SBATCH --out=clearfile.txt

srun python Acarus_clear.py
