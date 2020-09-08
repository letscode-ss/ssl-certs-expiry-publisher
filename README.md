# ssl-certs-expiry-publisher

This repo contain python code to read a json file which contain certificate details and publish there expiry days at /metrics endpoint.

### Metrics Format
```
# HELP get_certs_days_to_expire get remaining days for certificate to expire
# TYPE get_certs_days_to_expire gauge
```

### How to run this program
```
python app.py -c <config-json-path>
```


### Config json format
```
{
    "certs":
    [
        {
            "name":"jks certs",
            "passphrase":"changeit",
            "path":"certs/mock*.jks",
            "type":"JKS"
        },
        {
            "name":"pkcs12 certs",
            "passphrase":"changeit",
            "path":"certs/mock*.pkcs12",
            "type":"PKCS"
        },
        {
            "name":"google certs",
            "passphrase":"NA",
            "path": "google.com",
            "port": "443",
            "type":"URL"
        }

    ]
}
```

### How to build the image
```
docker build -t cert-checker:latest .
```

### Supported certificate formats
#### - JKS
#### - P12
#### - PEM
#### - PKCS
#### - URLs


### Example generate some certificate

#### Generate certs
```
mkdir certs 
keytool -genkey -alias mock-1 -storetype jks -keystore certs/mock-1.jks -keyalg RSA -keysize 2048 -validity 20
keytool -genkey -alias mock-2 -storetype pkcs12 -keystore certs/mock-2.pkcs12 -keyalg RSA -keysize 2048 -validity 10
```
#### Build dockerfile
```
docker build -t cert-checker:latest .
```
#### Run application
```
docker run -it -d -p 9100:9100 cert-checker:latest
```
#### Generate metrics metrics
```
$ wget localhost:9100
--2020-07-02 21:46:02--  http://localhost:9100/
Resolving localhost (localhost)... 127.0.0.1, ::1
Connecting to localhost (localhost)|127.0.0.1|:9100... connected.
HTTP request sent, awaiting response... 200 OK
Length: 35 [text/html]
Saving to: ‘index.html’

100%[======================================>] 35          --.-K/s   in 0s

2020-07-02 21:46:02 (3.82 MB/s) - ‘index.html’ saved [35/35]

$ wget localhost:9100/metrics
--2020-07-02 21:46:09--  http://localhost:9100/metrics
Resolving localhost (localhost)... 127.0.0.1, ::1
Connecting to localhost (localhost)|127.0.0.1|:9100... connected.
HTTP request sent, awaiting response... 200 OK
Length: 470 [text/plain]
Saving to: ‘metrics’

100%[======================================>] 470         --.-K/s   in 0s

2020-07-02 21:46:09 (74.7 MB/s) - ‘metrics’ saved [470/470]

$ cat metrics
# HELP get_certs_days_to_expire Get remaining days for certificate to expire
# TYPE get_certs_days_to_expire gauge
# HELP get_certs_days_to_expire Get remaining days for certificate to expire
# TYPE get_certs_days_to_expire gauge
get_certs_days_to_expire{common_name="test cert 1 ",name="mock certs jks",path="certs/mock-1.jks"} 20.0
get_certs_days_to_expire{common_name="test cert 2 ",name="mock certs jks",path="certs/mock-2.jks"} 10.0
get_certs_days_to_expire{common_name="test cert 3 ",name="mock certs pkcs12",path="certs/mock-3.pkcs12"} 20.0
get_certs_days_to_expire{common_name="test cert 4 ",name="mock certs pkcs12",path="certs/mock-4.pkcs12"} 10.0$
```

#### Enable prometheus scraping
```
apiVersion: v1
kind: Service
metadata:
  annotations:
    prometheus.io/scrape: "true"
....

```
