#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
    return rand()%2;
}

int main() {
  int x, y, z;
  scanf("%d%d%d", &x, &y, &z);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  if (0 == _nondet_2()) {
    x = 1;
  } else {
    x = -1;
  }
  while (y < 100 && z < 100) {
    printf("%d,%d,%d\n", x, y, z);
    y = y + x;
    z = z - x;
  }
  return 0;
}
