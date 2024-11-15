#!/usr/bin/env python3

from . import MFRC522
from itertools import chain


class SimpleMFRC522:
    KEYS = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    BLOCK_ADDRESSES = [8, 9, 10]

    def __init__(self):
        self.reader = MFRC522()

    def read(self):
        while True:
            tag_id, text = self._read_no_block()
            if tag_id:
                return tag_id, text

    def write(self, text):
        while True:
            tag_id, text_in = self._write_no_block(text)
            if tag_id:
                return tag_id, text_in

    def _read_id(self):
        while True:
            id_tag = self._read_id_no_block()
            if id_tag:
                return id_tag

    def _read_id_no_block(self):
        status, _ = self.reader.mfrc522_request(self.reader.PICC_REQIDL)
        if status != self.reader.MI_OK:
            return None
        status, uid = self.reader.mfrc522_anticoll()
        return None if status != self.reader.MI_OK else self._uid_to_number(uid)

    def _read_no_block(self):
        status, _ = self.reader.mfrc522_request(self.reader.PICC_REQIDL)
        if status != self.reader.MI_OK:
            return None, None
        status, uid = self.reader.mfrc522_anticoll()
        if status != self.reader.MI_OK:
            return None, None
        tag_id = self._uid_to_number(uid)
        self.reader.mfrc522_select_tag(uid)
        status = self.reader.mfrc522_auth(
            self.reader.PICC_AUTHENT1A, 11, self.KEYS, uid
        )
        text_read = ""
        if status == self.reader.MI_OK:
            data = list(
                chain.from_iterable(
                    self.reader.mfrc522_read(address)
                    for address in self.BLOCK_ADDRESSES
                    if self.reader.mfrc522_read(address)
                )
            )
            text_read = "".join(chr(i) for i in data)
        self.reader.mfrc522_stop_crypto1()
        return tag_id, text_read

    def _write_no_block(self, text):
        status, _ = self.reader.mfrc522_request(self.reader.PICC_REQIDL)
        if status != self.reader.MI_OK:
            return None, None
        status, uid = self.reader.mfrc522_anticoll()
        if status != self.reader.MI_OK:
            return None, None
        tag_id = self._uid_to_number(uid)
        self.reader.mfrc522_select_tag(uid)
        status = self.reader.mfrc522_auth(
            self.reader.PICC_AUTHENT1A, 11, self.KEYS, uid
        )
        self.reader.mfrc522_read(11)
        if status == self.reader.MI_OK:
            data = bytearray()
            data.extend(
                bytearray(text.ljust(len(self.BLOCK_ADDRESSES) * 16).encode("ascii"))
            )
            for index, block_num in enumerate(self.BLOCK_ADDRESSES):
                self.reader.mfrc522_write(
                    block_num, data[(index * 16) : (index + 1) * 16]
                )
        self.reader.mfrc522_stop_crypto1()
        return tag_id, text[: len(self.BLOCK_ADDRESSES) * 16]

    @staticmethod
    def _uid_to_number(uid):
        number = 0
        for index, character in enumerate(uid):
            number = number * 256 + character
            if index == 4:
                return number
