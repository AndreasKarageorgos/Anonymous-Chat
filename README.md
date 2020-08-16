# Anonymous-Chat
A chat that can provide anonymity with end to end encryption and no need to trust the server !

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

## Key word
This option can be left blank if you are in a private server.

If you are on a public server you and the person that you want to send a message, you must have the same AES,IV keys and same key word !

If you are on a private server and a you left the key word blank and the other person adds a word then you will not be able to see the messages.

They client it is programmed to not showing messages with deferent key word but this does not mean that the other person can't read your data.

The only way to keep your messages safe is by not sharing your keys with people that you do not want to talk.

## Note !
They key files can not be send through the server for extra safety !

You will need to send them to the person that you want to talk face to face or something.

This way the server will never be able to store your keys and then decrypt and log your data.

Also do not forget that this chat is in alpha version.

### Clinet Example

In order 2 clients to talk to each other, they must connect to the same server with the same AES,IV keys and same key words.

* Client1

        >> python3 client.py
        
        Enter a key word: Test
        
        Onion link: example_link.onion

* Client2
        
        >> python3 client.py
        
        Enter a key word: Test
        
        Onion link: example_link.onion
    
* Client3
        
        >> python3 client.py
        
        Enter a key word: test
        
        Onion link: example_link.onion
 
 * Client4
        
        >> python3 client.py
        
        Enter a key word: Test
        
        Onion link: example_link.onion
 

Client3 even with the same AES,IV keys it is not going to display any message. (It is going to be able to uncrypt the data because it has the same AES,IV keys)

Client4 has the same key word with Client1 and Client2 but different AES,IV keys , that means Client4 will not be able to decrypt and see the data.
