rm -f /tmp/dupa || true
mkfifo /tmp/dupa
rm -f /tmp/chuj || true
mkfifo /tmp/chuj

seq 10 > /tmp/dupa &
cat << EOF | python3 - &
print("Hello world")
import os
from splice import splice
read_fd = os.open("/tmp/dupa", os.O_RDONLY)
write_fd = os.open("/tmp/chuj", os.O_WRONLY)
print(read_fd, write_fd)
splice(write_fd, read_fd, 0, 10)
EOF

cat /tmp/chuj | wc -l