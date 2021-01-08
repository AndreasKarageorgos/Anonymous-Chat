[![Discord](https://discord.com/api/guilds/758523764735606795/widget.png)](https://discord.gg/wSsr73z)

# Secure Private Connections - Chat
* A chat that can provide privacy with end to end encryption, tor and without the need to trust the server to keep your keys safe ! The Keys that you will use to encrypt your messages are created and encypted localy to your computer, this way the server never has your keys and therefor it is not possible to store them. You are risponsible for your self ! To talk with someone you must share the same key, to do that you [extract](https://github.com/AndreasKarageorgos/SPC-Chat#key-extractor) your key and after that it is highly recommended to encrypt it with a public key and then send it.

* The chat runs fully on tor, this way the internet traffic is encrypted and anonymous

* Video tutorial: https://www.youtube.com/watch?v=6o1UnxU8dgo

* website: https://spcchat.com/

# Linux

* Ubuntu:

        $ sudo apt update && sudo apt install git -y 
        $ git clone https://github.com/AndreasKarageorgos/SPC-Chat.git        
        $ cd SPC-Chat/install        
        $ chmod +x Ubuntu.sh        
        $ ./Ubuntu.sh

* Fedora

        $ sudo dnf -y update && sudo dnf -y install git        
        $ git clone https://github.com/AndreasKarageorgos/SPC-Chat.git        
        $ cd SPC-Chat/install        
        $ chmod +x Fedora.sh        
        $ sudo ./Fedora.sh

* Manjaro

        $ sudo pacman -Sy       
        $ wget https://github.com/AndreasKarageorgos/SPC-Chat/releases/download/v1.11.c.1.7.s/Manjaro.tar.xz        
        $ tar -xf Manjaro.tar
        $ cd SPC-Chat/install       
        $ chmod +x manjaro.sh
        $ sudo ./manjaro.sh

* Tails Os

        $ wget https://github.com/AndreasKarageorgos/SPC-Chat/releases/download/v1.11.c.1.7.s/TAILS.tar.xz
        $ tar -xf Manjaro.tar
        $ cd SPC-Chat/client

# Windows

* Download python3 from [here](https://www.python.org/)

* Download Tor Windows Expert Bundle from [here](https://www.torproject.org/download/tor/)

* Download SPC-Chat for windows from [here](https://github.com/AndreasKarageorgos/SPC-Chat/releases)

* Inside the install folder run the windows.bat . In case of error download [visual studio](https://visualstudio.microsoft.com/vs/features/cplusplus/) with C++ and after that run the Windows.bat again.

# Server setup

### Linux

---
        $ sudo nano /etc/tor/torrc
---

In the torrc file you must add these 2 lines:

---
        HiddenServiceDir /var/lib/tor/spc-chat/
        HiddenServicePort 4488 127.0.0.1:4488

---

Then restart the tor service

---
* Ubuntu

        $ sudo service tor restart

* Fedora

        $  sudo service tor restart

* Manjaro

        $ sudo systemctl restart tor
---

Locate your onion address

---
        $ sudo cat /var/lib/tor/spc-chat/hostname
---

Start the server

---
        $ python3 server.py
---

If you want to run the server in the background (optional)

---
        $ python3 server.py --bgh &
---


### Windows

* First run tor for the first time and close it.

* Go to C:\Users\%username%\AppData\Roaming\tor\ and create a file with the name torrc (Make sure that the file does not have an ending like .txt ...etc).

* In the torrc file paste [this](https://gitweb.torproject.org/tor.git/plain/src/config/torrc.sample.in).

* add at the end of the file these lines:
---
        HiddenServiceDir C:\SPC-Chat\

        HiddenServicePort 4488 127.0.0.1:4488
---

* Run tor.

* locate your address in C:\SPC-Chat\hostname.

* Run the server.

---

If you want to run the server in the background rename the server from server.py to server.pyw

---
---
---
# How to use

* first run the chat and generte a room.
* use the key extractor to extract the key.
* send the key to the person that you want to chat.
* if you are the one that receives the key use the key loader to load it to the chat.
* select a shared server with the same room and start chatting.
---
# Key sharing

The best way to share a key is by storing it to a usb drive and then by giving it to the person that you want to chat face to face.

If you can't do that and you want to use for example an email service, use [pgp](https://en.wikipedia.org/wiki/Pretty_Good_Privacy) encryption to encrypt the extracted key.

If you are on linux you probably have already [GnuPG](https://gnupg.org/) to your computer.

To check type to your terminal:

        $ gpg --version

If you are on windows download GnuPG from [here](https://gpg4win.org/download.html).

I found this video on how to use GnuPG on windows and Linux

* For Windows click [here](https://www.youtube.com/watch?v=CEADq-B8KtI)

* For Linux click [here](https://youtu.be/CEADq-B8KtI?t=819)