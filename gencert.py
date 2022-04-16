#! /bin/env python3

# Generate a key, self-signed certificate, and certificate request.
# Usage: gencert hostname [hostname...]
#
# When more than one hostname is provided, a SAN (Subject Alternate Name)
# certificate and request are generated.  The first hostname is used as the
# primary CN for the request.
#
# Author: James E. Blair <jeblair@berkeley.edu>  2010-06-18
# With help from this thread:
# http://www.mail-archive.com/openssl-users@openssl.org/msg47641.html
# Updated by Blake Dworaczyk <blaked@tamu.edu>

import os
import stat
import subprocess
import sys
import tempfile

OPENSSL_CNF = """
[ req ]
default_bits		= 2048
default_md		    = sha1
distinguished_name	= req_distinguished_name
prompt              = no
%(req)s

[ req_distinguished_name ]
C=US
ST=Texas
L=College Station
O=Texas A&M University
OU=College of Engineering
%(cn)s

[ v3_req ]
basicConstraints    = CA:FALSE
keyUsage            = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName      = @alt_names

[ v3_ca ]
subjectKeyIdentifier    = hash
authorityKeyIdentifier  = keyid:always,issuer:always
basicConstraints        = CA:true
subjectAltName          = @alt_names

[ alt_names ]
%(alt)s
"""

SAN_REQ = """
x509_extensions	= v3_ca	# The extentions to add to the self signed cert
req_extensions  = v3_req # The extensions to add to a certificate request
"""


def run(args):
    p = subprocess.Popen(args,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         close_fds=True)
    p.stdin.close()
    while True:
        o = p.stdout.read(1)
        if not o:
            break
        sys.stdout.write(o.decode())
        sys.stdout.flush()
    r = p.wait()
    if r:
        raise Exception(f'Error running {args}')


if __name__ == "__main__":
    names = sys.argv[1:]
    if not names:
        print('Usage: gencert hostname [hostname...]\n')
        print('  Please provide at least one hostname on the command line.')
        print('  Mulitple hostnames may be provided to generate a SAN request.\n')
        sys.exit(1)
    params = {'req': '', 'dn': '', 'alt': ''}
    if len(names) > 1:
        # SAN
        san_names = ""
        for i, name in enumerate(names):
            san_names += f'DNS.{i} = {name}\n'
        params['req'] = SAN_REQ
        params['alt'] = san_names
        san_fn = '-san'
    else:
        san_fn = ''
    params['cn'] = f'CN={names[0]}'
    keyfile = f'private/{names[0]}{san_fn}.key'
    crt_file = f'certs/{names[0]}{san_fn}.cert'
    csr_file = f'certs/{names[0]}{san_fn}.csr'
    (fh, cnf_file) = tempfile.mkstemp()

    # Make sure that our 'certs' and 'private' subdirectories exist
    for the_dir in ['certs', 'private']:
        if not os.path.exists(the_dir):
            os.mkdir(the_dir)

    os.write(fh, str.encode(OPENSSL_CNF % params))
    os.close(fh)

    if os.path.exists(crt_file):
        print("Certificate file exists, aborting")
        print("  ", crt_file)
        sys.exit(1)

    if os.path.exists(csr_file):
        print("Certificate request file exists, aborting")
        print("  ", csr_file)
        sys.exit(1)

    if os.path.exists(keyfile):
        print("Key file exists, skipping key generation")
    else:
        run(['openssl', 'genrsa', '-out', keyfile, '2048'])
        os.chmod(keyfile, stat.S_IREAD)
    run(['openssl', 'req', '-config', cnf_file, '-new', '-nodes', '-key', keyfile, '-out', csr_file])
    run(['openssl', 'req', '-config', cnf_file, '-new', '-nodes', '-key', keyfile, '-out', crt_file, '-x509'])
    run(['openssl', 'req', '-in', csr_file, '-text'])

    os.unlink(cnf_file)
