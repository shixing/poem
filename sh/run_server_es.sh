export OMP_NUM_THREADS=32
nohup python ../py/poem_es.py 2>&1 > ../log/poemserver_es.log &
