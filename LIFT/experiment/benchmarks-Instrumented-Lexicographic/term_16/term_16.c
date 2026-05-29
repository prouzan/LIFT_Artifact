#include <stdio.h>
#include <stdlib.h>

int _nondet_int() {
  return rand();
}

int main() {
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  while (x / 50 == y) {

    printf("%d,%d\n", x, y);

    int z = _nondet_int();
    x = x + 1 + 50*z;
    y = y + z;

  }
  return 0;
}
