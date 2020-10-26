# card-scanner

---

刷卡程序 - 服务版

---

### 依赖

- [devicer](<https://github.com/YHYJ/Devicer>)
- evdev
- requests
- toml

---

### 配置项

```toml
[device]
    keyword = ''                    # Device type, 'usb', 'ALSA'... (Case sensitive)

[interval]
    heartbeat = 30                  # Heartbeat interval

[url]
    url = ''                        # Url used to receive the card number
    getip_ip = ''                   # In order to get their own ip address
    getip_port = 80                 # In order to get their own ip address

[log]
    [log.loggers]
        [log.loggers.main]
            handlers = ['console', 'rotate_debug']
```

> keyword = 要监控设备的关键字
>
> heartbeat = 心跳间隔
>
> url = 输入设备所获取信息的接收对象
>
> getip_ip = 辅助ip，用来获取程序运行机器的本机ip，只要格式对并且不是`127.0.0.1`即可
>
> getip_port = 辅助port，默认的80即可
>
> handlers项在程序作为服务运行时最好把'console'取消，否则可能导致大的磁盘占用

---

### 运行方式

```shell
$ python3 run.py
```
