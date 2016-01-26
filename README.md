# SMSgateway

A simple python Asterisk AGI script that foward received SMS message to Wechat enterprise account.

## Requirements

Asterisk 10+ with 3G dongle driver [asterisk-chan-dongle](https://github.com/bg111/asterisk-chan-dongle) installed. A 3G dongle with SIM card has been connected to Asterisk correctly.

## Usage

Clone the repo with `git`, copy `weixin.py` and `config.py` to Asterisk AGI directory (default: `/var/lib/asterisk/agi-bin/`).
```
$ git clone https://github.com/cyanife/SMSgateway.git
$ cd SMSgateway
$ sudo cp -b *.py /var/lib/asterisk/agi-bin/
```

Edit `config.py`, add your enterprise account's corpid and secret code, replace the values in `MESSAGE_CONF` to fit your own configuration, [reference here](http://qydev.weixin.qq.com/wiki/index.php?title=%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F).

Edit Asterisk extensions config file (default: `/etc/asterisk/extensions.conf`), the script need to be called as this format:

```
AGI(weixin.py,"${SENDER_NUMBER}","${RECEIVING_TIME}","${SMS_CONTENT}")
``` 

For example, the `[from-trunk-dongle]` block in `extensions.conf` can be set as below:

```
[from-trunk-dongle]
exten => sms,1,Verbose(Incoming SMS from ${CALLERID(num)} ${BASE64_DECODE(${SMS_BASE64})})
exten => sms,n,Set(FILE(/var/log/asterisk/sms.txt,,,a)=${STRFTIME(${EPOCH},,%Y-%m-%d %H:%M:%S)} - ${DONGLENAME} - ${CALLERID(num)}: ${BASE64_DECODE(${SMS_BASE64})})
exten => sms,n,AGI(weixin.py,${CALLERID(num)},${STRFTIME(${EPOCH},,%Y-%m-%d %H:%M:%S)},${BASE64_DECODE(${SMS_BASE64})})
exten => sms,n,Hangup()
exten => _.,1,Set(CALLERID(name)=${CALLERID(num)})
exten => _.,n,Goto(from-trunk,${EXTEN},1)
```

Then SMS messages received by 3G dongle will be forward to specified wechat enterprise account automatically. 