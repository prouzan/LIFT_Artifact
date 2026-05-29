#include <stdio.h>

int main() {
  int x, y;
  scanf("%d", &x);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  y = 0;
  while (x > 0)
  {
    printf("x:%d,y:%d\n", x, y);
    if (y == 2) x = x - 3; else x = x + 1;
    if (y == 2) y = 0; else y = y + 1;
  }
}
