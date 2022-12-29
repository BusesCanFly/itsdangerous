#! /usr/bin/python3

import atheris
import sys
import io

# example code on https://github.com/pallets/itsdangerous README

with atheris.instrument_imports():
    from itsdangerous import URLSafeSerializer

def fuzz_singleInput(input_bytes):
    fdp = atheris.FuzzedDataProvider(input_bytes)
    data_string = fdp.ConsumeUnicodeNoSurrogates(sys.maxsize)
    data_int = fdp.ConsumeInt(sys.maxsize)

    auth_s = URLSafeSerializer(data_string, data_string) # "secret key", "auth"
    token = auth_s.dumps({data_string: data_string, data_string: data_string}) # {"id": 5, "name": "itsdangerous"}

    # print(token)
    # # eyJpZCI6NSwibmFtZSI6Iml0c2Rhbmdlcm91cyJ9.6YP6T0BaO67XP--9UzTrmurXSmg
    data = auth_s.loads(token)
    # print(data["name"])
    # # itsdangerous

def main():
    atheris.Setup(sys.argv, fuzz_singleInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()