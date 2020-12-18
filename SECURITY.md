# Security Policy

If you find a Vulnerability, do not publish it until it is fixed.
Send a report which you explain it, or even suggest a solution.

## Supported Versions

* Latest

# Reporting a Vulnerability

First see if I have already found this vulnerability and I have created a draft for security advisor [here](https://github.com/AndreasKarageorgos/SPC-Chat/security/advisories). If not read below.

Report a Vulnerability to my email: andreas_karageorgos@protonmail.com

The Subject must be: Vulnerability [Critical/medium/low] (Select one)

In the body you must describe analytically the Vulnerability.

#### The body must be encrypted to a "readable" form with my public key.

* See the key [here](https://github.com/AndreasKarageorgos/SPC-Chat/blob/master/public.asc)

* If you are using GnuPG to encrypt your message I recomend this command:

        $ gpg -a -o spc-mail -e [your message]

* Then copy the message and send it to my email. The email must be in this form:

        -----BEGIN PGP MESSAGE-----
        ....
        ....
        -----END PGP MESSAGE-----

* You can skip the encryption part only if you are using protonmail.
