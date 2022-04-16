#!/usr/bin/env bash

export PATH=$coreutils/bin

mkdir $out

cp $src $out/gencert.py
cat <<EOF > $out/engr-cert-gen
#!${bash}/bin/bash
PATH=${PATH}:${python310}/bin:${openssl}/bin
python $out/gencert.py "\$@"
EOF
chmod +x $out/engr-cert-gen
