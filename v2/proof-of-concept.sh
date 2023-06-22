#!/bin/bash

samples=200
sampleratehz=44100
length=`ffprobe -i "input/Gymnopedie No. 1.mp3" -show_entries format=duration -v quiet -of csv="p=0"`
echo "Length: $length"

samplerate=`python -c "print($length/$samples * $sampleratehz)"`
echo "Rate: $samplerate"

output=`ffmpeg -v quiet -i "input/Gymnopedie No. 1.mp3" -af aresample=$sampleratehz,asetnsamples=$samplerate,astats=metadata=1:reset=1:length=0.05,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=- -f null -`

echo $output | awk 'BEGIN{ RS = " " ; FS = "=" } /lavfi.astats.Overall.RMS_level/ {print $2}' | tr -s '\n' | head --bytes=-1 > data.txt

echo $output > raw.txt