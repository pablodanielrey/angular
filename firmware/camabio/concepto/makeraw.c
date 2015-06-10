
#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>

struct termios tp;


void main() {

  char *path = "/dev/ttyUSB0";
  int fd = open(path, O_RDWR | O_NOCTTY | O_NONBLOCK);

  tcgetattr(fd, &tp);
  cfmakeraw(&tp);
  cfsetspeed(&tp, B9600);
  tcsetattr(fd, TCSANOW, &tp);

  close(fd);
}
