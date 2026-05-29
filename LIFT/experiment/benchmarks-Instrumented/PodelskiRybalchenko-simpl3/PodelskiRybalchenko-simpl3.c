#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
  return rand()%2;
}

int main() {
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  while (x > 0 && y > 0) {
    printf("x:%d,y:%d\n", x, y);
    if (_nondet_2()) {
      x = x - 1;
      y = 2 * y;
    } else {
      y = y - 1;
    }
  }
  return 0;
}
