# engr-certificate-generation

This is a simple python script to generate CSRs for engr.tamu.edu
certificates. You can optionally specify multiple FQDNs to create SAN certs.

Although you can install OpenSSL and Python3 yourself, the recommended way to
run this is by using Nix.

## Intalling Nix

### Installing Nix on Windows (using WSL2)
1. If you don't have it already, install WSL2 (Windows Subsystem for Linux 2).
Open a PowerShell prompt as administrator and type:
```powershell
PS > wsl --install
```
Now reboot your machine.

2. Enter WSL and Install Nix (from either PowerShell or CMD):
```bash
PS > wsl
PS > sh <(curl -L https://nixos.org/nix/install) --no-daemon
```

### Installing Nix on Mac
```bash
$ sh <(curl -L https://nixos.org/nix/install)
```

### Installing Nix on Linux
```bash
$ sh <(curl -L https://nixos.org/nix/install) --daemon
```

## Installing the engr-cert-gen application

```bash
$ nix-env -i git   # This is optional if you already have git installed and you're not running Windows
$ curl -o engr_cert_gen.nix -L https://raw.githubusercontent.com/Texas-A-M-College-of-Engineering/engr-certificate-generation/main/engr_cert_gen.nix
$ nix-env -i $(nix-build engr_cert_gen.nix)
```

## Generating CSRs (Certificate Signing Requests)
CSRs, or Certificate Signing Requests, are what you use to have a certificate signed by a Certificate Authority.
You can take a CSR and go to [cert.tamu.edu](https://cert.tamu.edu) and have a certificate signed, which results
in a valid, usable certificate.

You should create your own certificate directory that you switch to every time that you generate a new CSR.
Then, you simply run the `engr-cert-gen` application with one or more FQDNs (Fully Qualified Domain Names).
If you specify more than one name at a time, a SAN cert CSR is created for you.

When you run the `engr-cert-gen` application, it will create two directories, *certs* and *private*. The *certs* 
directory will contain the *.csr* file that you will provide to cert.tamu.edu. The *private* directory will contain
the *.key* file that will be needed along with the cert that you download from cert.tamu.edu.

### Example cert creation
If you've installed both Nix and the engr-cert-gen application, you can generate a cert as follows (using the CLI):

1. Switch to your certificate directory (or create one if this is your first time)
This command creates a cert directory if it doesn't exist, and switches to it
```bash
$ cd ~/engr_certs || mkdir ~/engr_certs && cd ~/engr_certs
```
2. Generate the CSR for your cert using the FQDN. In this case, I use *blaketest.engr.tamu.edu*. Note that I've
only included one FQDN, *blaketest.engr.tamu.edu*, so this will not be a SAN cert, just a normal one.
```bash
$ engr-cert-gen blaketest.engr.tamu.edu
```
If I wanted a SAN cert, I could have done something like this:
```bash
$ engr-cert-gen blaketest.engr.tamu.edu certtest.engr.tamu.edu
```
This would have created a SAN cert that was valid for both FQDNs.

3. Get the CSR contents or file. When you go to cert.tamu.edu, it will ask for you to either paste the CSR
contents (text), or provide the CSR file. The last step output the CSR contents to the screen, so you can
just copy that text. An example of the CSR output text that you want to copy/paste would be:

```
-----BEGIN CERTIFICATE REQUEST-----
MIIC2jCCAcICAQAwgZQxCzAJBgNVBAYTAlVTMQ4wDAYDVQQIDAVUZXhhczEYMBYG
A1UEBwwPQ29sbGVnZSBTdGF0aW9uMR0wGwYDVQQKDBRUZXhhcyBBJk0gVW5pdmVy
c2l0eTEfMB0GA1UECwwWQ29sbGVnZSBvZiBFbmdpbmVlcmluZzEbMBkGA1UEAwwS
YmxhaC5lbmdyLnRhbXUuZWR1MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKC
AQEAyG6McuK88RkY8VhTI9C7dJYmXAd6ic4P1CYlqHyZZNkgSRbMfZFxQ9R++GZG
o4xwhjPeNfc9YLtmfD3Fk+y6/iNDm4lcQQROnsfCIEUOMoHMuu07rzlF2Hz10DYo
WqqJ6yynp05KnH4hJpNxum+4ZUr93FP5/U7ZNEpGTu593eyQ9zV1KDH428iqtKIr
M1vylQtCLsgZ9NbBWdpCQQf1SpXmYEpP6+qVC9/vAF4qZ709kEKMRu5dzbl5KsUq
6Bxluogp0P75zm+cPs89IKOv5xhTP/E5qgBLm96qRSheg/YepfnWBfaAPtdLkj0X
/bywhoFPA9r3SpagzezE/QM6/wIDAQABoAAwDQYJKoZIhvcNAQEFBQADggEBAGd3
LK/kvbrMFxJV/7T5j6ntdR4b8pHr8GPr0RMLqIy6K8dL6C/9OezHD16ZxgBu7lmv
eODcNn6EzzinvG1hg28gSWirpAuGo8y0llA8wHfyc4y8nsNCRie+OpAgpBFUMIJG
0NcW7RpNnu/pz10MJsCDiOnqPlCdUJNWVs6wn3nrli2wadXkVioyA6+tVjQKxA1B
CTsTeYT0/FIsYrxPA3gqX5iqSSCmjcMFYrEU7ORsFBqGeDib4XzxiI3F6BPUAuKc
UIH1slbPom7Iz6+Io2FgOCxlucFVjKwZJpIYhJwm91QADkzZ7jBGH984RpPWHnUb
okzpos+nD1zNbHfwobY=
-----END CERTIFICATE REQUEST-----
```

You can just copy/paste the text (make sure that you include the *-----BEGIN CERTIFICATE REQUEST-----* and
the *-----END CERTIFICATE REQUEST-----*) and use it on cert.tamu.edu.

If, on the other hand, you lost this text, you could also find it in a file in your cert directory. The file is named
based on the FQDN of the cert. So, for *blaketest.engr.tamu.edu*, listing the file would look like (from your engr_certs
directory):
```bash
$ ls certs/blaketest.engr.tamu.edu.csr
```
which would show up as
```
certs/blaketest.engr.tamu.edu.csr
```

You could copy/paste the contents of this file, or you could upload the file itself to cert.tamu.edu. Cert.tamu.edu
gives you both options when creating a certificate.

## Using a certificate
Once your certificate is ready from cert.tamu.edu (you will receive an email), you download the certificate. However,
this is only half of what you need. To use a certificate, you need both the certificate and the private key. You
download the certificate from cert.tamu.edu, but the private key was generated when you ran the engr-cert-gen app, and 
it never left that location. This is good, because the private key, unlike the certificate, needs to be kept secret.

Just like we examined the location of the CSR earlier, we can do the same thing with the private key. For example (from
your *engr_certs* directory):
```bash
$ ls private/blaketest.engr.tamu.edu.key
```

which would show up as:
``` 
private/blaketest.engr.tamu.edu.key
```

So you could go to your *engr_certs/private* directory and get the private key to use with the certificate that you
downloaded from cert.tamu.edu. Now you have the public/private pair that you need to use the certificate somewhere.
