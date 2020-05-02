import os

#print("borrar en temp")
#for i in os.listdir("temp/"):
#    try:
#        os.system('rm --r -f ' + i + '/*')  # borra temporales del programa
#    except:
#        pass

print("borrar los temp/")
try:
    os.system('rm --r -f /LUSTRE/home/fmsanchez/GDarkSUSY/temp/*')  # borra temporales del programa
except:
    pass

print("borrar los RUN*.txt")
# os.system('rm --r -f temp/*')  # borra temporales del programa
try:
    os.system('find /LUSTRE/home/fmsanchez/GDarkSUSY/data/ -name "RUN*.txt" -delete')  # borra los run del programa realizados de esta manera se ejecutaran
except:
    pass

print("borrar los COPY*.txt")
try:
    os.system('find /LUSTRE/home/fmsanchez/ -name "COPY*.txt" -delete')  # borra los run del programa realizados de esta manera se ejecutaran
except:
    pass

# Ejecutar subida
os.system('sbatch Acarus_genera.sh')

