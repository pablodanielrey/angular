avconv -i rtsp://163.10.17.5/video.h264 -c copy -map 0 -f ssegment -segment_list v.m3u8 -segment_list_flags +live -segment_time 10 -segment_format ts "v-%09d.ts"

