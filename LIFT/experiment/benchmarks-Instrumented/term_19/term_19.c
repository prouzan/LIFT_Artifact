#include <stdio.h>

int main() {
  int x, y;
  scanf("%d", &x);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  y = 5;

  if (x <= 10) return 0;

  while (x != 2*y) {
    printf("x:%d,y:%d\n", x, y);
    if (x % 5 == 1) x++;
      else x = x - 2;
  }
  return 0;
}
