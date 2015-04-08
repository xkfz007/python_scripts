#!/bin/python
import  lib

enc = lib.Encoder_prop()
print enc.id
print enc.exe

enc.set_encoder_path("f:/da/fa/")
print enc.exe
enc.set_encoder_id("x265")
print enc.exe

lib.Encoder_prop.SET_PATH("as265","f:/a/1/")
lib.Encoder_prop.SET_PATH("x265","f:/b/2/")
enc.set_encoder_id("as265")
print enc.exe
enc.set_encoder_id("x265")
print enc.exe
