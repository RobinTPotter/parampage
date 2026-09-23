 ____       ____                                        _ 
|  _ \ __ _|  _ \ __ _ _ __ ___  _ __   __ _  __ _  ___| |
| |_) / _` | |_) / _` | '_ ` _ \| '_ \ / _` |/ _` |/ _ \ |
|  __/ (_| |  _ < (_| | | | | | | |_) | (_| | (_| |  __/_|
|_|   \__,_|_| \_\__,_|_| |_| |_| .__/ \__,_|\__, |\___(_)
                                |_|          |___/        

it's parameters on a page.


run:

```
python osc_relay.py
```

and visit http://localhost:12340?param=range:0:100:1:/param a1,range:0:1:0.01:/param a2

python serves static content but delivers osc
message to 57120 based on params.

update url parameters to your liking, parameters generated for `params` with each in list separated
by comma. `sendto` also available to set the host:port of the relay.
