rm -f /tmp/dupa || true
mkfifo /tmp/dupa

seq 10000000 > /tmp/dupa &
cat /tmp/dupa | wc -l