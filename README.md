Original code from [pimylifeup](https://github.com/YudiNz/MFRC522-python-SimpleMFRC522).
`RPi.GPIO` doesn't support the Raspberry Pi 5. In this fork I used `gpiozero` instead of `RPi.GPIO` to support also the Raspberry Pi 5.

Create virtual environment and install
---------------------

Follow the steps below as an example for how to create a python environment and install `MFRC522.py`
Note: You have to enable SPI in `sudo raspi-config` and RST-Pin is GPIO22.
Note: You don't have to use `nano`, you can use your favorite editor. 
Note: Add the "Example Code" below in `read_tag.py`.
```bash
dennis@test:~ $ mkdir mfrc522_test/src -p
dennis@test:~ $ python -m venv mfrc522_test/.venv
dennis@test:~ $ git clone https://github.com/Dennis-89/MFRC522-python-SimpleMFRC522.git mfrc522_test/src/
Cloning into 'mfrc522_test/src'...
remote: Enumerating objects: 211, done.
remote: Counting objects: 100% (160/160), done.
remote: Compressing objects: 100% (74/74), done.
remote: Total 211 (delta 96), reused 145 (delta 86), pack-reused 51 (from 1)
Receiving objects: 100% (211/211), 59.00 KiB | 1.34 MiB/s, done.
Resolving deltas: 100% (97/97), done.
dennis@test:~ $ . mfrc522_test/.venv/bin/activate
(.venv) dennis@test:~ $ pip install lgpio
(.venv) dennis@test:~ $ cd mfrc522_test/src
(.venv) dennis@test:mfrc522_test/src $ pip install .
(.venv) dennis@test:mfrc522_test $ cd ..
(.venv) dennis@test:mfrc522_test $ nano read_tag.py
(.venv) dennis@test:mfrc522_test $ python read_tag.py
```

## Example Code

The following code will read a tag from the MFRC522

```python
from time import sleep
from mfrc522 import SimpleMFRC522


def main():
    reader = SimpleMFRC522()
    while True:
        print("Hold a tag near the reader")
        tag_id, text = reader.read()
        print(f'ID: {tag_id}\nText: {text}')
        sleep(1)

if __name__ == '__main__':
    main()
```

Original ReadMe-Description:
-----------------------------

# mfrc522

A python library to read/write RFID tags via the budget MFRC522 RFID module.

This code was published in relation to a [blog post](https://pimylifeup.com/raspberry-pi-rfid-rc522/) and you can find out more about how to hook up your MFRC reader to a Raspberry Pi there.

## Installation

Until the package is on PyPi, clone this repository and run `python setup.py install` in the top level directory.

## Example Code

The following code will read a tag from the MFRC522

```python
from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id,text))
        sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
```
