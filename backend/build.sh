#!/bin/bash

export GOARCH=amd64
export GOOS=linux

cd src/SpoofDPI/cmd/spoofdpi
go build -ldflags '-w -s'

mkdir -p /backend/out
mv spoofdpi /backend/out/spoofdpi
