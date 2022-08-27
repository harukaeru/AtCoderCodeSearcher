python3 -m http.server 9000 &
docker exec -it sqlpad wget -O atcoder.db http://host.docker.internal:9000/atcoder.db
