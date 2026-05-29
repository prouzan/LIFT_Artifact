#include <stdio.h>

int main() {
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  while (x / 50 == y) {

    printf("x:%d,y:%d\n", x, y);

    x = x + 51;
    y = y + 1;

  }
  return 0;
}
