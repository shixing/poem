export OMP_NUM_THREADS=32
nohup python poem.py 2>&1 > poemserver.log &
