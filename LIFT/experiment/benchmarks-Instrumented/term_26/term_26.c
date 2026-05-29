#include <stdio.h>

int main() {
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  int c1 = 0;
  int c2 = 0;

  while (x == y){
    printf("x:%d,y:%d,c1:%d,c2:%d\n", x, y, c1, c2);
    x = x + c1 % 2;
    y = y + c2 % 3;
    c1++; c2++;
  }
}
