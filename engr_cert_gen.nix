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
