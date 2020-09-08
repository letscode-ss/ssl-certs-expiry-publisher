import os

# App host
#
HOST = '0.0.0.0'
if 'HOST' in os.environ: HOST = os.environ['HOST']

# App port
#
PORT = '9100'
if 'PORT' in os.environ: PORT = os.environ['PORT']

# config json
#
CONFIG = '/app/config.json'
if 'CONFIG' in os.environ: CONFIG = os.environ['CONFIG']

# Cert monitoring gauge name
#
CERT_MONITORING_GAUGE_NAME = 'get_certs_days_to_expire'
if 'CERT_MONITORING_GAUGE_NAME' in os.environ: CERT_MONITORING_GAUGE_NAME = os.environ['CERT_MONITORING_GAUGE_NAME']

# Cert monitoring gauge description
#
CERT_MONITORING_GAUGE_DES = 'Get remaining days for certificate to expire'
if 'CERT_MONITORING_GAUGE_DES' in os.environ: CERT_MONITORING_GAUGE_DES = os.environ['CERT_MONITORING_GAUGE_DES']

# exclution list of common name
#
EXCLUDE_COMMON_NAME = ["ltsbca1","ltsbca2"]
if 'EXCLUDE_COMMON_NAME' in os.environ: EXCLUDE_COMMON_NAME = os.environ['EXCLUDE_COMMON_NAME'].split(",")

# Logs will print warning if expiry days is less then WARN_THRESHOLD
#
WARN_THRESHOLD = 15
if 'WARN_THRESHOLD' in os.environ: WARN_THRESHOLD = os.environ['WARN_THRESHOLD']

# Logs will print error if expiry days is less then WARN_THRESHOLD
#
ERROR_THRESHOLD = 30
if 'ERROR_THRESHOLD' in os.environ: ERROR_THRESHOLD = os.environ['ERROR_THRESHOLD']
