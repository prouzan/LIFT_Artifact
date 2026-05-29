#include <stdio.h>
#include <stdlib.h>

int _nondet_int() {
  return rand()%100;
}
int _nondet_3() {
  return rand()%3;
}
int _nondet_2() {
  return rand()%2;
}
int main() {
  int x, y, z;
  scanf("%d%d%d", &x, &y, &z);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  while (x > 0 && y > 0 && z > 0) {
    printf("x:%d,y:%d,z:%d\n", x, y, z);
    if (0 == _nondet_3()) {
      x = x - 1;
    } else if (_nondet_2()) {
      y = y - 1;
      z = _nondet_int();
    } else {
      z = z - 1;
      x = _nondet_int();
    }
  }
}
