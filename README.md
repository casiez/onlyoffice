[![PyPI Version](https://img.shields.io/pypi/v/onlyoffice)](https://pypi.org/project/onlyoffice/)
[![License](https://img.shields.io/github/license/casiez/onlyoffice)](LICENSE)

# onlyoffice

Provides a python API for OnlyOffice API

## Install
```pip install onlyoffice --upgrade```

Work in progress to provide a python API for the [OnlyOffice API](https://api.onlyoffice.com/portals/method/)

## Minimal example

```
import onlyoffice
oo = onlyoffice.OnlyOffice('https://yourportal.onlyoffice.com', 'username', 'password')
# download file ID 123
oo.download(['123'], 'file.zip')

```

## Supported commands
Read [onlyoffice/OnlyOffice.py](onlyoffice/OnlyOffice.py)
