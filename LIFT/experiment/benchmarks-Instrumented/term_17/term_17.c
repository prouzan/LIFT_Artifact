#include <stdio.h>

int main() {
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  int x, y;
  x = 0;
  y = 0;

  while (x < 49) {
    printf("x:%d,y:%d\n", x, y);
    x = y%50;
    y ++;
  }
  return 0;
}
