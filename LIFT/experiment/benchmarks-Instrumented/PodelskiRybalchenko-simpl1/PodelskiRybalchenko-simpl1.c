#include <stdio.h>
#include <stdlib.h>

int _nondet_int() {
  return rand();
}
int _nondet_2() {
  return rand()%2;
}
int main() {
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  int newx, newy;
  while (x > 0 && y > 0) {
    printf("x:%d,y:%d,newx:%d,newy:%d\n", x, y, newx, newy);
    if (_nondet_2()) {

      newx = _nondet_int();
      if (newx >= x) break;
      x = newx;

      newy = _nondet_int();
      if (newy <= y) break;
      y = newy;

    } else {

      newy = _nondet_int();
      if (newy >= y) break;
      y = newy;

    }
  }
  return 0;
}
