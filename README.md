[![Discord](https://discord.com/api/guilds/758523764735606795/widget.png)](https://discord.gg/wSsr73z)

# Secure Private Connections - Chat
* A chat that can provide privacy with end to end encryption, tor and without the need to trust the server to keep your keys safe ! The Keys that you will use to encrypt your messages are created and encypted localy to your computer, this way the server never has your keys and therefor it is not possible to store them. You are risponsible for your self ! To talk with someone you must share the same key, to do that you [extract](https://github.com/AndreasKarageorgos/SPC-Chat#key-extractor) your key and after that it is highly recommended to encrypt it with a public key and then send it.

* The chat runs fully on tor, this way the connections are encrypted and anonymous

* Video tutorial: https://www.youtube.com/watch?v=6o1UnxU8dgo

* website: https://spcchat.com/


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

        Tails:

            Git is pre-installed on tails

    * Then clone the Chat to your Home folder

            $ git clone https://github.com/AndreasKarageorgos/SPC-Chat.git
    ---
    * Or if you are using Tails download the binary files from [here](https://github.com/AndreasKarageorgos/SPC-Chat/releases/)
    ---
    * Manjaro: Here is the fixed window for manjaro => [Download](https://github.com/AndreasKarageorgos/SPC-Chat/releases/)

    * locate the "install" folder inside the SPC-Chat
    and run the installer for your os. (You do not need installer for tails)

    For example in Ubuntu:
            
            $ cd SPC-Chat/install/          
            
            $ chmod +x Ubuntu.sh
            
            $ ./Ubuntu.sh
    


* Windows (Python-code)

  * Download python3 from [here](https://www.python.org/) and select the box "add python to path".

  * Download github Desktop from [here](https://desktop.github.com/)

  * Download SPC-Chat from [here](https://github.com/AndreasKarageorgos/SPC-Chat/archive/master.zip) or clone it to your computer.

  * Download Tor Windows Expert Bundle from [here](https://www.torproject.org/download/tor/)

  * Inside the install folder run the windows.bat . In case of error download [visual studio](https://visualstudio.microsoft.com/vs/features/cplusplus/) with C++ and after that run the Windows.bat again.
        
* Windows (Binary)

   * Download SPC-Chat for windows from [here](https://github.com/AndreasKarageorgos/SPC-Chat/releases)
   

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

  * First run [tor](https://www.torproject.org/download/tor/) for the first time and close it.

  * Go to C:\Users\\%username%\AppData\Roaming\tor\ and create a file with the name torrc (Make sure that the file does not have an ending like .txt ...etc).

  * In the torrc file paste [this](https://gitweb.torproject.org/tor.git/plain/src/config/torrc.sample.in)

  * then add to the end of the file:

        HiddenServiceDir C:\SPC-Chat\
        
        HiddenServicePort 4488 127.0.0.1:4488

  * Run tor

  * locate yout address in C:\SPC-Chat\hostname

  * Now you can run the server.
        

# Client setup
  
The client use tor as proxy to connect to a server, the only thing that you have to do as client is to make sure that the tor service is running
   
* To check if the service is running

  * Ubuntu

        $ sudo service tor restart
  
  * Fedora
        
        $ sudo service tor restart

  * manjaro
        
        $ sudo systemctl restart tor

  * Tails

        on Tails tor service is on by default


After that you can cd in SPC-Chat/client/ and run:

    $ python3 chat.py

or if you are on tails you run:

    $ ./chat 

### Windows
* Tor

        To run Tor on windows you will need to use "Windows Expert Bundle"
        
   * You can download it from [here](https://www.torproject.org/download/tor/)
 
* Chat
        
        Go to client folder and run the chat.py or chat.exe


 # Key

Your keys are your rooms. You can have multiple keys. Locate them under SPC-Chat/client/data/key/
 
 The keys are for encrypting and decrypting messages. You can generate them using the key_generator.py located in SPC-Chat/client/

    $ python3 key_generator.py

 Your messages can be decrypted only with the key that you use , so keep it safe and share it only with the person that you want to send messages. Change your keys often for extra safety.

* You can find instructions on how to exchange your keys without risking your messages on the [discord server](https://github.com/AndreasKarageorgos/SPC-Chat#discord)


# Note !
They Key file can not be send through the server for extra safety !

exchange your key by using pgp encryption.

 If you send it online you may want to use protonmail.

This way the server will never be able to store your key and then decrypt and log your messages.

# Chat

when you run the chat it will ask you for a password. This password is they password that has been used to encrypt your key (room)

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
 

Client1 and Client2 have the same keys, this way they are going to be on the same room and be able to see and send messages to each other. 
Client4 has different key so it is going to be on different room an it wont be able to send messages to Client1 and Client2 and the opposite.

Server creates private chat rooms based on your keys (Server never gets your keys). People with different keys are going to be in different chat rooms.

# key_generator

This tool will help you to generate strong keys.

The generator will ask you to input a name. If you have already a key with this name it is going to be replaced.

It is also asking you to set up a password. This password it is used to encrypt the key for extra safety.

# key loader

Use this tool to load a key. If the key ends with .unsafe it is going to ask you to set up a password. If it ens with .key it is going to load it as it is. If there is already a key with the same name that you are trying to load it is going to be replaced.


# key extractor

Use this tool to extract a key so you can send it. When you extract a key the key gets unencrypted and saved with the ending ".unsafe" . If you want to send it online use pgp encyption.
