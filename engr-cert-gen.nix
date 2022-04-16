#This will fetch anything we need from our own repo once it exists
#builtins.fetchGit { url = "https://github.com/NixOS/patchelf"; }

with (import <nixpkgs> {});
derivation {
  name = "engr-cert-gen";
  builder = "${bash}/bin/bash";
  args = [ ./builder.sh ];
  inherit bash coreutils openssl python310;
  src = ./gencert.py;
  system = builtins.currentSystem;
}
