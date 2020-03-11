#!/bin/bash                                                                                                                                                    

##SBATCH --cpus-per-task=1            # Number of cores per MPI task 
#SBATCH --nodes=1                    # *Maximum number of nodes to be allocated
##SBATCH --ntasks-per-node=12         # *Maximum number of tasks on each node
#SBATCH --ntasks=5 
##SBATCH --ntasks-per-socket=6        # Maximum number of tasks on each socket
##SBATCH --distribution=cyclic:cyclic # Distribute tasks cyclically first among nodes and then among sockets within a node


#SBATCH --mail-type=END,FAIL         # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=fmartinez8939@gmail.com     # Where to send mail	

#SBATCH --job-name=DarkSUSY_CMS                                                                                                                                 
#SBATCH --time=168:0:0                                                                                                                                          
#SBATCH --partition=general                                                                                                                                    
#SBATCH --constraint=broadwell                                                                                                                                 

srun python genera_v5.py
