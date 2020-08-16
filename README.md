# Anonymous-Chat
A chat that can provide anonymity with end to end encryption and no need to trust the server !

The server runs on port 4488 by default

## Setup

### Ubuntu
    
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
   
   To check if the service is running
    
    sudo service tor status
   
   If the service is closed
    
    sudo service tor start
    

## Note !
They key files can not be send through the server for extra safety !

You will need to send them to the person that you want to talk face to face or something.

This way the server will never be able to store your keys and then decrypt and log your data.
