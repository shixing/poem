export OMP_NUM_THREADS=32
nohup python poem_interactive.py 2>&1 > poemserver.interactive.log &
