#!/bin/bash

# This script will stream content to the NavCoffee Twitch 
# channel

# Resources:
# https://trac.ffmpeg.org/wiki/EncodingForStreamingSites

STREAM_URL="rtmp://live.twitch.tv/app/"
KEY="ENTER YOUR TWITCH STREAM KEY HERE"

# Set zoom
v4l2-ctl --set-ctrl=zoom_absolute=250

# Start streaming command
cmd=$(ffmpeg -thread_queue_size 512 -y -f video4linux2 -r 15 -s 640x360 -vcodec mjpeg \
-i /dev/video0 -pix_fmt yuv420p \
-i /home/pi/Documents/nav_qr.png -pix_fmt yuv420p -filter_complex \
"[0:v]scale=-1:-1,setpts=PTS-STARTPTS[bg]; \
 [1:v]scale=170:-1,setpts=PTS-STARTPTS[fg]; \
 [bg][fg]overlay=10:10[out]; \
 [out]drawbox=y=320:color=black@0.4:width=iw:height=30:t=max[out]; \
 [out]drawtext=text='          Coffees Donated               Donations Made               Coffees Redeemed':x=(w-w/2-text_w/2):y=(h-text_h-20):fontfile=OpenSans.ttf:fontsize=15:fontcolor=white[out]; \
 [out]drawtext=textfile=/home/pi/Documents/coffees_donated.txt:x=20:y=(h-text_h-20):fontfile=OpenSans.ttf:fontsize=15:fontcolor=white:reload=1[out]; \
 [out]drawtext=textfile=/home/pi/Documents/donations.txt:x=215:y=(h-text_h-20):fontfile=OpenSans.ttf:fontsize=15:fontcolor=white:reload=1[out]; \
 [out]drawtext=textfile=/home/pi/Documents/redemptions.txt:x=410:y=(h-text_h-20):fontfile=OpenSans.ttf:fontsize=15:fontcolor=white:reload=1[out]" \
-map "[out]" -c:v libx264 -preset veryfast -maxrate 1984k -bufsize 3968k \
-g 60 -c:a aac -ar 44100 \
-f flv "$STREAM_URL/$KEY" &> /dev/null)

# If stream errors out, restart it
until $cmd ; do
	echo "Error encountered, restarting stream"
	sleep 2
done
