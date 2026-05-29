#include <stdio.h>
#include <stdlib.h>

int _nondet_int() {
  return rand()%100;
}
int _nondet_2() {
  return rand()%2;
}

int main() {
  int x, y, d;
  scanf("%d%d%d", &x, &y, &d);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  while (x > 0 && y > 0 && d > 0) {
    printf("x:%d,y:%d,d:%d\n", x, y, d);
    if (_nondet_2()) {
      x = x - 1;
      d = _nondet_int();
    } else {
      x = _nondet_int();
      y = y - 1;
      d = d - 1;
    }
  }
}
