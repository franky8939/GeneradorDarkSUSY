#!/bin/bash                                                                                                                                                    
#SBATCH --nodes=10                                                                                                                                              
#SBATCH --ntasks-per-node=10                                                                                                                                   
#SBATCH --job-name=serial_test                                                                                                                                 
#SBATCH --time=168:0:0                                                                                                                                          
#SBATCH --partition=general                                                                                                                                    
#SBATCH --constraint=broadwell                                                                                                                                 

srun python genera_v4.py
