export OMP_NUM_THREADS=32
nohup python ../py/poem_interactive.py 2>&1 > ../log/poemserver.interactive.log &
