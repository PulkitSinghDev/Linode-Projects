#!/bin/bash

ip=$(echo "$QUERY_STRING" | cut -d"=" -f2 | egrep -e "^([0-9]+\.){3}[0-9]+$")
whois "$ip"
