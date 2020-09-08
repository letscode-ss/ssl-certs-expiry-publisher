from flask import Response, Flask, request
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time
from JsonParser import *
from FindDaysToExpire import *
import sys, getopt
import constant


app = Flask(__name__)

_INF = float("inf")

registry = CollectorRegistry()
graphs = {}


graphs['c'] = prometheus_client.Gauge(
    constant.CERT_MONITORING_GAUGE_NAME,
    constant.CERT_MONITORING_GAUGE_DES,
    ["name","common_name","path"],
    registry=registry,
)

#/ entrypoint will generate cert info and publish it to /metrics
#
@app.route("/")
def generate_gauge():
    certs_data = {}
    certs_arr = json_parser(app.config.get('app_config_path'))
    for info in certs_arr:
        if (info['type'] == 'JKS'):
            certs_data = get_jks_days_to_expire(info)
        elif(info['type'] == 'PEM'):
            certs_data = get_pem_days_to_expire(info)
        elif(info['type'] == 'PKCS'):
            certs_data = get_pkcs_days_to_expire(info)
        elif(info['type'] == 'P12'):
            certs_data = get_p12_days_to_expire(info)
        elif(info['type'] == 'URL'):
            certs_data = get_remote_expiry_days(info)
        else: 
            print('INFO: ',info['name'])
            print('Format not supported')  
        for paths in certs_data:
            for common_name in certs_data[paths]:
                graphs['c'].labels(info['name'], common_name, paths).set(certs_data[paths][common_name])
    return 'Check the /metrics for more details'

#/metrics uri will expose all metrics for prometheus 
#
@app.route("/metrics")
def requests_gauge():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")

#Options for app.py
#
def usage():
    print('Usage: app.py -c <config-json> [optional]')
    print('    -c  : specify json config')
    print('    -p  : port (default: 9100')
    print('    -h  : host (default: 0.0.0.0)')

#Main function which get configurations 
#
def main(argv):
    #App config vars
    #
    app_config_path = constant.CONFIG
    app_port = constant.PORT
    app_host = constant.HOST
    try:
        opts, args = getopt.getopt(argv, "c:p:h:")
    except getopt.GetoptError as exc:
        print('Invalid option ' + exc.opt + ' : ' + exc.msg)
        usage()
        sys.exit(1)
    
    for opt, arg in opts:
        if opt == '-c':
            app_config_path = arg
        elif opt == '-p':
            app_port = arg
        elif opt == '-h':
            app_host = arg
    json_parser(app_config_path)
    print('INFO: Config : ->', app_config_path)
    print('INFO: Port : -> ', app_port)
    print('INFO: Port : -> ', app_host)
    return [app_config_path,app_host,app_port]

if __name__ == "__main__":
    conf_vars = main(sys.argv[1:])
    app.config['app_config_path'] = conf_vars[0]
    app.run(host=conf_vars[1], port=conf_vars[2], debug=True)
