import json, sys

#Json Parser function to parse config file
#
def json_parser(config_file):
    try:
        with open(config_file, "r") as read_file:
            developer = json.load(read_file)
            for key, certs_details in developer.items():
                return certs_details
    except:
        print('ERROR:', config_file , ' dont exits. please set CONFIG var or -c argument')
        usage()
        sys.exit(1)
