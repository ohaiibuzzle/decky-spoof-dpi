#!/bin/bash

cd src/SpoofDPI/cmd/spoofdpi
go build 

mkdir -p /backend/out
mv spoofdpi /backend/out/spoofdpi
