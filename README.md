# echo

The  primary usage of the echo worker as a test probe in the Digi:T stack. The worker takes a parameter that determines what is echoes. Only one parameter is allowed. The possible parameters are:
## TIMESTAMP

*?TIMESTAMP*

The current time is returned as "timestamp" parameter, {'timestamp':datetime.now().__str__()}

## DELAY

*?DELAY=<delay>*

Delays the amount of time i seconds. Default is 1 second.

## RANDELAY

*?RANDELAY=<delay>*

Delays a random amount of time between zero and <delay>. Default is 10 seconds.

## USERID

The user ID of the caller is returned. This parameter is always set på Optimizely to the logged in user. An empty value means that the user is not logged in.
Returned parameter is "loggedinuser".

## IPIFY

*?IPIFY*
Returns the outgoing IP-adress of the cluster. The request, *https://api.ipify.org/?format=json*, is routed through the internal Haninge network proxy. Will return the cluster IP in the "ip" parameter.
This is primarily a connectivity test.

## EMAIL

Will send a simple e-mail through the proxy. The only parameter is "EMAIL=*recipients e-mail adress*". The message sent is *Hej hopp i lingonskogen!*.
