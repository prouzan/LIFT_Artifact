#include <stdio.h>
#include <stdlib.h>
int _nondet_int() {
    return rand()%100;
}

int main() {
  int x,y,z;
  scanf("%d%d%d", &x, &y, &z);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  while (x > 0 && y > 0 && z > 0) {
    printf("x:%d,y:%d,z:%d\n", x, y, z);
    if (y > x) {
      y = z;
      z = _nondet_int();
      x = z + 1;
    } else {
      z = z - 1;
      y = _nondet_int();
      x = y + 1;
    }
  }
  return 0;
}
