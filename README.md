# Keras EmailMonitor
**Note: this is still a WIP. If you would like to use this, please raise an issue**

Sends an email with stats at the end of every epoch.

![alt text](./img/screenshot.png)


#### Usage:
```
from monitor import EmailMonitor
...
email_monitor = EmailMonitor(<your email address here>)
model.fit(...
          callbacks=[email_monitor])
```

#### Custom Sender Address:
Currently, the repository uses a dummy Gmail address with Gmail's security settings turned off. If you would like to use this email address as well, please raise an issue requesting access. If not, make sure that you have a `secrets.yaml` file in the root directory with the following structure:

```
sender:
    email_address: <your sender email address>
    password: <your sender password>
```

#### Requirements:
```
python==3.6
tensorflow=1.8.0
keras==2.1.6
pprint==0.1
```

#### Todo:
- [x] Create example model
- [x] Send email from default Gmail account
- [ ] Define custom SMTP server (aka better security)
- [ ] Enable user to stop model training with an email
- [ ] PyTorch integration
