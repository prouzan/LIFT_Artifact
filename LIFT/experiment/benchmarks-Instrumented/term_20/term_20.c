#include <stdio.h>

int main() {
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  int x = 0;
  int y = 0;
  int z = 0;

  while (x < 100) {
    printf("x:%d,y:%d,z:%d\n", x, y, z);
    x = x + y;
    y = z + 1;
    z = y - 1;
  }
  return 0;
}
