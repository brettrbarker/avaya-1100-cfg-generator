# avaya-1100-cfg-generator

## Summary
This python script will take a CSV input with MAC address and Phone numbers and generate individual files in the format SIP[MAC].cfg for the purpose of setting the AUTOLOGIN parameters.

## Details
The Avaya 1100 series phones (ex. 1120 and 1140) take a series of configuration files. The first file that it pulls from the provisioning server is the main .cfg in the model specific format of 1xxxeSIP.cfg (ex. 1120eSIP.cfg). This file then dictates the additional files to pull and the order in which they are installed.

These other files to pull would include phone firmware, trusted root certificates, device certificate, the dial plan, device configuration, and a device specific configuration file.

This script is to create that last file for the IP Deskphone-specific configuration file: [USER_CONFIG]

### Usage
```
python cfg-generator sample-csv.csv
```
or specifically calling python 3 if it is not the default.
```
python3 cfg-generator sample-csv.csv
```

### Output
Sample Output file: *SIP581626091238.cfg*
```
SLOW_START_200OK NO

ENABLE_LOCAL_ADMIN_UI NO

AUTO_UPDATE YES

AUTO_UPDATE_TIME 2200

MAX_LOGINS 2

AUTOLOGIN_ENABLE 2

AUTOLOGIN_ID_KEY01 5551238@uc.mil

AUTOLOGIN_PASSWD_KEY01 123456

AUTOLOGIN_ID_KEY02 5551240@uc.mil

AUTOLOGIN_PASSWD_KEY02 123456
```