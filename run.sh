docker build -t ssl-certs-expiry-publisher:latest  .
docker run -it -p 9100:9100 -v  ssl-certs-expiry-publisher:latest
