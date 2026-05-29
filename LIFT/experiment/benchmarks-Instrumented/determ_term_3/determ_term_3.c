#include<stdio.h>

int main() {
  int x = 5;
  int y = 1;
  int z = 17;
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  
  while (!(x == y && y == z)) {
    printf("x:%d,y:%d,z:%d\n", x, y, z);
    x = x + 1;
    y = y * 2;
    z = z - 3;
  }
  return 0;
}
