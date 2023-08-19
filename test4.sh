rm /tmp/test.sock || true
nc -lU  /tmp/test.sock | wc -l &
seq 10000000 | nc -U /tmp/test.sock
wait