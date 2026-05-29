#include <stdio.h>

int main() {
  int x, y, z;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  if (y <= 1) return 0;

  z = 1;
  while (x > 0) {
    printf("%d,%d\n", x, y);
    x = x - y;
    y = y - z;
    z = -z;
  }
  return 0;
}
