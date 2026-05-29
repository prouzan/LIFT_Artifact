#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
  return rand()%2;
}

int main() {
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  while (x > 0 && y > 0) {
    printf("%d,%d\n", x, y);
    if (_nondet_2()) {
printf("L1\n");
      x = x - 1;
      y = 2 * y;
    } else {
printf("L2\n");
      y = y - 1;
    }
  }
  return 0;
}
