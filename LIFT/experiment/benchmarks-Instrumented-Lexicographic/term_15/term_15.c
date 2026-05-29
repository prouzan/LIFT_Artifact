#include <stdio.h>

int main() {
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  while (x / 50 == y) {

    printf("%d,%d\n", x, y);

    x = x + 51;
    y = y + 1;

  }
  return 0;
}
