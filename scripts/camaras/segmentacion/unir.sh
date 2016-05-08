cat *.ts > movie.ts
ffmpeg -i movie.ts -acodec copy -vcodec copy movie.mp4

