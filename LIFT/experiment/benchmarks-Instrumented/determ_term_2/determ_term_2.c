#include<stdio.h>

int main() {
  int x = -36;
  int y = 0;
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  
  while (x != 0) {
    printf("x:%d,y:%d\n", x, y);
    x = x + y;
    y = y + 1;
  }
  return 0;
}
