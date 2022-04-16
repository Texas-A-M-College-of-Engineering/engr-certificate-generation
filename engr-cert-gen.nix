#This will fetch anything we need from our own repo once it exists
#builtins.fetchGit { url = "https://github.com/NixOS/patchelf"; }

with (import <nixpkgs> {});
let
    repo = builtins.fetchGit {
        url = "https://github.com/Texas-A-M-College-of-Engineering/engr-certificate-generation.git";
        ref = "main";
    };
in
    derivation {
      name = "engr-cert-gen";
      builder = "${bash}/bin/bash";
      args = [ "${repo.outPath}/builder.sh" ];
      inherit bash coreutils openssl python310;
      src = "${repo.outPath}/gencert.py";
      system = builtins.currentSystem;
    }
