# Secure Private Connections - Chat
A chat that can provide privacy with end to end encryption, tor and without the need to trust the server ! 

This project is targeting people that trully need privacy.

eg. Politicians , military , journalist , lawyers , companies ... etc

The server runs on port 4488 by default

### Donations
 To keep updating this project I will need your support.

 You can help me by donating.

 * paypal : https://paypal.me/AndreasKarageorgos/20

 * BlockChain : https://www.blockchain.com/btc/address/1DJqJtMGRzG12NZk1SJ5DnCfpeunTX1z1V
 
 If you want me to asign you a new BTC address for you to donate, you can send me email and ask for it.
 
 * andreas_karageorgos@protonmail.com
 
 I will delete the email after I read it.



# Installetion

* Ubuntu

    * sudo apt update

    * sudo apt install git -y

    * sudo apt install python3-pip -y
    
    * sudo apt install python3-tk -y
    
    * sudo apt install tor -y

    * pip3 install pycryptodome

    * pip3 install pysocks

    * git clone https://github.com/AndreasKarageorgos/SPC-Chat.git

* All commands in one:
    
    * sudo apt update &&  sudo apt install git -y && sudo apt install python3-pip -y && sudo apt install python3-tk -y && sudo apt install tor -y && pip3 install pycryptodome && pip3 install pysocks && git clone https://github.com/AndreasKarageorgos/SPC-Chat.git


# Server setup
You will need to edid the torrc file if you want to run the server.
  
locate the torrc file under /etc/tor/
  
and uncomment the HiddenService options.
  
You should edid them like this:
  
    HiddenServiceDir /var/lib/tor/hidden_service/
    
    HiddenServicePort 4488 127.0.0.1:4488
  
After that restart the tor service
    
    sudo service tor restart
  
and locate your onion address under /var/lib/tor/hidden_service/
    
    sudo su
    
    cat /var/lib/tor/hidden_service/hostname
    
    exit

after that you can run the server by cd in SPC-Chat/server/ and run

    python3 server.py

# Client setup
  
The client use tor as proxy to connect to a server, the only thing that you have to do as client is to make sure that the tor service is running
   
* To check if the service is running
    
        sudo service tor status
   
 * If the service is closed
    
        sudo service tor start

After that you can cd in SPC-Chat/client/ and run:

    python3 client.py
 
 # Key
 There is 1 key file
 
 * Key.key

 under SPC-Chat/client/data/key/
 
 The key is for encrypting and decrypting messages. You can generate it using the key_generator.py located in SPC-Chat/client/

    python3 key_generator.py

 Your messages can be decrypted only with this key , so keep it safe and share it only with the person that you want to send messages. Change your keys often for extra safety

 If you create your own key , make sure that it is at least 20 characters long. Small keys can be cracked really fast.

# Note !
They Key file can not be send through the server for extra safety !

You will need to send it to the person that you want to talk face to face using a usb ...etc.

This way the server will never be able to store your key and then decrypt and log your messages.

# Clinet Example

In order 2 clients to talk to each other, they must connect to the same server with the same AES key (Key.key file).

* Client1 Key.key = "This is an AES key" Server: example_link.onion

        >> python3 client.py
        

* Client2 Key.key = "This is an AES key" Server: example_link.onion
        
        >> python3 client.py
 
 * Client3 Key.key = "Hello !" Server: example_link.onion
    
        >> python3 client.py
 

Client1 and Client2 have the same keys, this way they are going to be able to see the messages of each other. 
Client4 has different key so it wont be able to decrypt or send messages to Client1 and Client2 and the opposite. (The server broadcasts to every client all the messages)
