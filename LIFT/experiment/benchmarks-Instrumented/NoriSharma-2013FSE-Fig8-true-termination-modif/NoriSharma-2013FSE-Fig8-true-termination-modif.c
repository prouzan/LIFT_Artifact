#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
    return rand()%2;
}

int main() {
  int x, y, z;
  scanf("%d%d%d", &x, &y, &z);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  while (x >= y) {
    printf("x:%d,y:%d,z:%d\n", x, y, z);
    if (0 == _nondet_2()) {
      z = z - 1;
      x = x + z;
    } else {
      y = y + 1;
    }
  }
}
