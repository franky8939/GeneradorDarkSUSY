import os

for i in os.listdir("temp/"):
    try:
        os.system('rm --r -f ' + i + '/*')  # borra temporales del programa
    except:
        pass

# os.system('rm --r -f temp/*')  # borra temporales del programa
os.system('find data/ -name "RUN*.txt" -delete')  # borra los run del programa realizados de esta manera se ejecutaran

# Ejecutar subida
os.system('sbatch Acarus_genera.sh')

