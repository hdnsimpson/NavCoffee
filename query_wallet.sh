#!/bin/bash

# This script will get data from our wallet

# Get wallet data
data="$(wget -qO- https://www.navexplorer.com/address/NgZNDCxF8DGzxjPi5NiUcHGkKhtYS1LY51/tx.json)"

# Get amount of donations made
donations="$(echo "${data}" | tr ',' $'\n' | grep -c RECEIVE)"

# Write to donations file
echo "${donations}" > /home/pi/Documents/donations.txt.tmp
echo "${donations}" > /home/pi/Documents/donations2.txt.tmp
perl -pi -e 'chomp if eof' /home/pi/Documents/donations.txt.tmp
perl -pi -e 'chomp if eof' /home/pi/Documents/donations2.txt.tmp
mv /home/pi/Documents/donations.txt.tmp /home/pi/Documents/donations.txt
mv /home/pi/Documents/donations2.txt.tmp /home/pi/Documents/donations2.txt

# Get amount donated
received_amounts="$(echo "${data}" | tr ',' $'\n' | grep '"received":' | cut -d':' -f 2)"

# Write transaction history to file
echo "${received_amounts}" > /home/pi/Documents/txn_history.txt.tmp
perl -pi -e 'chomp if eof' /home/pi/Documents/txn_history.txt.tmp
mv /home/pi/Documents/txn_history.txt.tmp /home/pi/Documents/txn_history.txt

# Sum donations
total_received="$(LC_NUMERIC="C" awk '{sum += $1} END {print sum}' txn_history.txt)"

# Calculate coffees donated
coffees="$(echo $(("${total_received}" / 5)))"

# Write coffees donated
echo "${coffees}" > /home/pi/Documents/coffees_donated.txt.tmp
echo "${coffees}" > /home/pi/Documents/coffees_donated2.txt.tmp
perl -pi -e 'chomp if eof' /home/pi/Documents/coffees_donated.txt.tmp
perl -pi -e 'chomp if eof' /home/pi/Documents/coffees_donated2.txt.tmp
mv /home/pi/Documents/coffees_donated.txt.tmp /home/pi/Documents/coffees_donated.txt
mv /home/pi/Documents/coffees_donated2.txt.tmp /home/pi/Documents/coffees_donated2.txt

# Format other files
perl -pi -e 'chomp if eof' /home/pi/Documents/redemptions.txt
perl -pi -e 'chomp if eof' /home/pi/Documents/redemptions2.txt
