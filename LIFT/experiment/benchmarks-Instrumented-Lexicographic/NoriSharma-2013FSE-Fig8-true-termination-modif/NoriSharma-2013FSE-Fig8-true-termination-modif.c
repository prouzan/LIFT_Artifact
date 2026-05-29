#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
    return rand()%2;
}

int main() {
  int x, y, z;
  scanf("%d%d%d", &x, &y, &z);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  while (x >= y) {
    printf("%d,%d,%d\n", x, y, z);
    if (0 == _nondet_2()) {
printf("L1\n");
      z = z - 1;
      x = x + z;
    } else {
printf("L2\n");
      y = y + 1;
    }
  }
}
