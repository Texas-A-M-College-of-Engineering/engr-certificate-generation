#!/usr/bin/env bash

export PATH=$coreutils/bin

mkdir -p $out/bin

cp $src $out/bin/gencert.py
cat <<EOF > $out/bin/engr-cert-gen
#!${bash}/bin/bash
PATH=${PATH}:${python310}/bin:${openssl}/bin
python $out/bin/gencert.py "\$@"
EOF
chmod +x $out/bin/engr-cert-gen
