#! /usr/bin/python3

import atheris
import sys
import io

# example code on https://github.com/pallets/itsdangerous README

with atheris.instrument_imports():
    from itsdangerous import URLSafeSerializer, Signer, Serializer
    from itsdangerous.exc import BadSignature

def fuzz_singleInput(input_bytes):
    fdp = atheris.FuzzedDataProvider(input_bytes)
    data_string = fdp.ConsumeUnicodeNoSurrogates(sys.maxsize)
    data_int = fdp.ConsumeInt(sys.maxsize)

    auth_s = URLSafeSerializer(data_string, data_string) # "secret key", "auth"
    token = auth_s.dumps({data_string: data_string, data_string: data_string}) # {"id": 5, "name": "itsdangerous"}

    data = auth_s.loads(token)

    try:
        s = Signer(input_bytes)
        s.sign(data_string)
        s.unsign(str(input_bytes))
    except BadSignature:
        pass

    try:
        s = Serializer(input_bytes)
        s.loads(data_string)
    except BadSignature:
        pass

def main():
    atheris.Setup(sys.argv, fuzz_singleInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()