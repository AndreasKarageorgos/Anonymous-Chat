# Anonymous-Chat
A chat that can provide anonymity with end to end encryption and no need to trust the server !

The server runs on port 4488 by default

## Setup

### Ubuntu

  sudo apt install python3-pip -y

  sudo apt install tor -y

  pip3 install pycryptodome

  pip3 install pysocks

## Tor
  You will need to edid the torrc file if you want to run the server.
  
  locate the torrc file under /etc/tor/
  
  and uncomment the HiddenService options
  You should edid them like this:
  
    HiddenServiceDir /var/lib/tor/hidden_service/
    
    HiddenServicePort 4488 127.0.0.1:4488
  
  

## Note !
They key files are not sended through the server for extra safety !

You will need to send them to the person that you want to talk face to face or something.
