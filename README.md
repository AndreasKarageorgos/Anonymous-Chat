# Secure Private Connections - Chat
A chat that can provide privacy with end to end encryption, tor and without the need to trust the server to keep your keys safe ! 

# Donations
 
 This programm is free and it will continue to be free.
 
 This is why I need your support.

 * paypal : https://paypal.me/AndreasKarageorgos/

 * BlockChain (BTC) : https://www.blockchain.com/btc/address/1DJqJtMGRzG12NZk1SJ5DnCfpeunTX1z1V
 
 * Bitcoin Cash (BCH) : qpfmk88awqcwulau4txu9pg8t8w70mn885m7xjrhh5
 
 * Stellar Lumen (XLM) : GCJX6O7NF2RXRL72FAKFDIXD4P6CE4OSYFQM43ECPUP564K2ZZUHQIML


# Discord

 * Discord server: https://discord.gg/wSsr73z

# Installation

* Linux

    * First make sure that you have git installed on your system 
        
        Ubuntu:
            
            $ sudo apt update

            $ sudo apt install git

        Fedora:

            $ sudo dnf -y update

            $ sudo dnf -y install git

        Manjaro:

            $ sudo pacman -Sy

            $ sudo pacman -S git

    * Then clone the Chat to your Home folder

            $ git clone https://github.com/AndreasKarageorgos/SPC-Chat.git

    * locate the "install" folder inside the SPC-Chat
    and run the installer for your os.

    For example in Ubuntu:
            
            $ cd SPC-Chat/install/          
            
            $ chmod +x Ubuntu.sh
            
            $ ./Ubuntu.sh
    


* Windows

  * Download python3 from [here](https://www.python.org/) and select the box "add python to path".

  * Download Tor Windows Expert Bundle from [here](https://www.torproject.org/download/tor/)

  * Download SPC-Chat for windows from [here](https://github.com/AndreasKarageorgos/SPC-Chat/releases).

  * Inside the install folder run the windows.bat . In case of error download [visual studio](https://visualstudio.microsoft.com/vs/features/cplusplus/) with C++ and after that run the Windows.bat again.
        

   

# Server setup
The server is running on port 4488.
 You will need to edid the torrc file if you want to run the server.

* Linux
  
        $ sudo nano /etc/tor/torrc
 
In the torrc file you must add these 2 lines:

    HiddenServiceDir /var/lib/tor/spc-chat/
    
    HiddenServicePort 4488 127.0.0.1:4488

  
After that restart the tor service

* Ubuntu:
    
        $ sudo service tor restart

* Fedoea

        $ sudo service tor restart

* Manjaro

        $ sudo systemctl restart tor

  
and locate your onion address under /var/lib/tor/spc-chat/
    
    $ sudo cat /var/lib/tor/spc-chat/hostname

after that you can run the server by cd in SPC-Chat/server/ and run

    $ python3 server.py

* windows

        Just ask for help in the Discord server.

# Client setup
  
The client use tor as proxy to connect to a server, the only thing that you have to do as client is to make sure that the tor service is running
   
* To check if the service is running

  * Ubuntu

        $ sudo service tor restart
  
  * Fedora
        
        $ sudo service tor restart

  * manjaro
        
        $ sudo systemctl restart tor


After that you can cd in SPC-Chat/client/ and run:

    $ python3 chat.py

### Windows
* Tor

        To run Tor on windows you will need to use "Windows Expert Bundle"
        
   * You can download it from [here](https://www.torproject.org/download/tor/)
 
* Chat
        
        Go to client folder and run the chat.py

        (It will not run without your Key)

 # Key
 There is 1 key file
 
 * Key.key

 under SPC-Chat/client/data/key/
 
 The key is for encrypting and decrypting messages. You can generate it using the key_generator.py located in SPC-Chat/client/

    $ python3 key_generator.py

 Your messages can be decrypted only with this key , so keep it safe and share it only with the person that you want to send messages. Change your keys often for extra safety

 If you create your own key , make sure that it is at least 20 characters long. Small keys can be cracked really fast.


# Note !
They Key file can not be send through the server for extra safety !

exchange your key by using pgp encryption.

 If you send it online you may want to use protonmail.

This way the server will never be able to store your key and then decrypt and log your messages.

# Chat

when you run the chat it will ask you for a password. This password is they password that has been used to encrypt the Key.key file.

(You can not start the chat withoud a key)

# Chat - Keyboard shortcuts

* <Enter\> Sends the message.
* <Tab\> shows you the connected people in the room that you are connected.

# Client Example

In order 2 clients to talk to each other, they must connect to the same server with the same key (Key.key file).

* Client1 Key.key = "This is a key" Server: example_link.onion

        >> python3 chat.py
        

* Client2 Key.key = "This is a key" Server: example_link.onion
        
        >> python3 chat.py
 
 * Client3 Key.key = "this is a different key" Server: example_link.onion
    
        >> python3 chat.py
 

Client1 and Client2 have the same keys, this way they are going to be able to see and send messages to each other. 
Client4 has different key so it wont be able to send messages to Client1 and Client2 and the opposite.

Server creates private chat rooms based on your keys (Server never gets your keys). People with different keys are going to be in different chat rooms.

# key_generator

This tool will help you to generate strong keys.

The generator automatically replaces the old key. Make sure that you have back ups.

It is also asking you to set up a password. This password it is used to encrypt the key for extra safety.

# key_loader

This tool will help you to load a key. If the key it is not encrypted it will ask you to set up a password otherwise it will load it as it is.

(try to use keys that are generated with the key_generator)

### the old key is going to be replaced

# key extractor

This tool will extract your key, decrypt it and save it as Key.key.unsafe.

This key can be loaded to key_loader.
