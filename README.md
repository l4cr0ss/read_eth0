###What it does
A short python script that sends a text message to a cellphone with the inet4 address assigned to an interface.

### What you need
A Linux/Unix machine with `python v2.7` and the `ifconfig` tool

### How it works
This script works by sending a string via STMP to a cell phone carrier's SMS gateway. Set it up by 
downloading it and entering the following details into the code (specified by angle brackets):

1. The email address and password to send the message from (line `68`, `69`)
2. The cell phone number of the recipient (line `70`)
3. The email address of the cell carrier's SMS gateway (line `70`)

### Installing the script
Place the script in the folder of scripts run by the networking service immediately after it ups the interfaces. On the machine used to write this script, that folder is /etc/network/if-up.d/

If the script needs to run more often than this, consider creating a cronjob for it.

### Customizing the message
Change the message sent to the phone by editing the values of `str_success` and `str_failure` on lines `46` and `47`.
The default messages looks like this:

    2000-01-23 12:34:56 
    My device has booted with an IP address of 192.168.1.2

    2000-01-23 12:34:56 
    My device has booted, but without an IP address
 
### Customizing the interface name
By default, the script searches for an interface called `eth0`. Change the interface that the script searches for by passing the name of the interface as a string to the function `get_iface_addr` on line `56`

