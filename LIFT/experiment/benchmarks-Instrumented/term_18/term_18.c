#include <stdio.h>

int main() {
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  int x, y, z;
  x = 0;
  y = 0;
  z = 0;

  while (x <= 97) {
    printf("x:%d,y:%d,z:%d\n", x, y, z);
    x = y%50 + z%50;
    y ++;
    z ++;
  }
  return 0;
}
