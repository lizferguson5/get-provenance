import argparse
import urllib2
import json
import sys

UFRAME_URL = 'http://ooiufs01.ooi.rutgers.edu:12576'

def get_response(url):
    try:
        response = urllib2.urlopen(url)
        return response.read()
    except:
        return None

def get_json_response(url):
    data = get_response(url)
    if data:
        return json.loads(data)
    return None

def main(args):
    ref_des_parts = args.ref_des[0].split('-')
    if len(ref_des_parts) != 4:
        print 'You must specify a reference designator in the following format: {node}-{subsite}-{sensor}'
        sys.exit(1)
    
    methods_url = '%s/sensor/inv/%s/%s/%s-%s' % (UFRAME_URL, ref_des_parts[0], ref_des_parts[1], ref_des_parts[2], ref_des_parts[3])
    stream_methods = get_json_response(methods_url)
    if stream_methods:
        for method in stream_methods:
            streams_url = '%s/%s' % (methods_url, method)
            streams = get_json_response(streams_url)
            if streams:
                for stream in streams:
                    stream_url = '%s/%s?user=%s&include_provenance=true' % (streams_url, stream, args.user[0])
                    data = get_response(stream_url)
                    if data:
                        print data
    else:
        print 'No data found for reference designator: %s' % args.ref_des[0]
        sys.exit(2)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description=main.__doc__)
    arg_parser.add_argument('-r',
        nargs=1,
        dest='ref_des',
        help='Specify a reference designator in the following format: {node}-{subsite}-{sensor}')
    arg_parser.add_argument('-u',
        nargs=1,
        dest='user',
        help='Specify a username')
    main(arg_parser.parse_args())