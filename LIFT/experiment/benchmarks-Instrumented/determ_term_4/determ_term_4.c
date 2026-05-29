#include<stdio.h>

int main() {
  int x = 4;
  int y = -5;
  int z = 1;
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  
  while (x + y != z) {
    printf("x:%d,y:%d,z:%d\n", x, y, z);
    x = x * -3;
    y = y + 2;
    z = z - 36;
  }
  return 0;
}
