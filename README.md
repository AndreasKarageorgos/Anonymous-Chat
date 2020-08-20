# Anonymous-Chat
A chat that can provide privacy with end to end encryption and no need to trust the server !

The server runs on port 4488 by default

## Setup

#### Ubuntu
    
    sudo apt update

    sudo apt install python3-pip -y
    
    sudo apt install python3-tk -y
    
    sudo apt install tor -y

    pip3 install pycryptodome

    pip3 install pysocks

## Tor For the server
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

## Tor For the client
  
The client use tor as proxy to connect on a server, the only thing that you have you do is to make sure that the tor service is running
   
* To check if the service is running
    
        sudo service tor status
   
 * If the service is closed
    
        sudo service tor start
 
 ## Keys
 There are 2 key files
 * AES.key
 * IV.key
 
 These keys are for encrypting and decrypting messages. You can generate them using the key_generator.py
 
 cd to the folder of the chat and type:
        
        cd data/
        
        python3 key_generator.py
        
 Your messages can be decrypted only with those keys , so keep them safe and share them only with the person that you want to talk.

## Note !
They key files can not be send through the server for extra safety !

You will need to send them to the person that you want to talk face to face or something.

This way the server will never be able to store your keys and then decrypt and log your messages.

Also do not forget that this chat is in alpha version.

### Clinet Example

In order 2 clients to talk to each other, they must connect to the same server with the same AES,IV keys.

* Client1 AES.key = "GtR29" , IV.key = "Uiqw"

        >> python3 client.py
        
        Onion link: example_link.onion

* Client2 AES.key = "GtR29" , IV.key = "Uiqw"
        
        >> python3 client.py
        
        Onion link: example_link.onion
 
 * Client3 AES.key = "Hgfw" , IV.key = "bhwg"
        
        >> python3 client.py
        
        Onion link: example_link.onion
 

Client1 and Client2 have the same pair of keys, this way they are going to be able to see the messages of each other. Client4 has different keys so it wont

be able to decrypt or send messages to Client1 and Client2. (The server broadcasts to every client all the messages)


## DISCLAIMER

The author(s) of this programm are not responsible for any damage(s).
