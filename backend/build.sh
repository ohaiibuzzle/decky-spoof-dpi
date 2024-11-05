#!/bin/bash

cd src/SpoofDPI
go build
mkdir -p ../../bin

mv spoof-dpi ../../bin/spoof-dpi
