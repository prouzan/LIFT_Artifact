#include <stdio.h>
#include <stdlib.h>

int _nondet_int() {
  return rand();
}

int main() {
  int x, y, z;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  while (x / 50 == y) {

    printf("x:%d,y:%d,z:%d\n", x, y, z);

    z = _nondet_int();
    x = x + 1 + 50*z;
    y = y + z;

  }
  return 0;
}
