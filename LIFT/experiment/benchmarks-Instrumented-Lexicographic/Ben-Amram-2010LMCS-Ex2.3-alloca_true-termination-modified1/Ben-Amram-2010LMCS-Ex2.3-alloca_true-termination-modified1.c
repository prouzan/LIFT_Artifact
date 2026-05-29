#include <stdio.h>
#include <stdlib.h>
int _nondet_int() {
    return rand()%100;
}

int main() {
  int x,y,z;
  scanf("%d%d%d", &x, &y, &z);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  while (x > 0 && y > 0 && z > 0) {
    printf("%d,%d,%d\n", x,y,z);
    if (y > x) {
printf("L1\n");
      y = z;
      z = _nondet_int();
      x = z + 1;
    } else {
printf("L2\n");
      z = z - 1;
      y = _nondet_int();
      x = y + 1;
    }
  }
  return 0;
}
