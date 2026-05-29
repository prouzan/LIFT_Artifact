#include <stdio.h>

int main() {
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  if (x <= 0) return 0;
  if (y <= 0) return 0;
  if (x % y != 0) return 0;

  while (x != 0)
  {
    printf("%d,%d\n", x, y);
    x = x - y;
  }
}
