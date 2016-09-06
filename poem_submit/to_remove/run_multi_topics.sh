IFS=$'\n'       # make newlines the only separator
set -f          # disable globbing
for i in $(cat "$1"); do
  echo $i;
  echo $i >> $2;
  echo "----------------------" >> $2;
  python ../RunMe.py $i >> $2;
done
