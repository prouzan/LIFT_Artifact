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
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  int newx, newy;
  while (x > 0 && y > 0) {
    printf("%d,%d\n", x, y);
    if (_nondet_2()) {
printf("L1\n");

      newx = _nondet_int();
      if (newx >= x) {
printf("L2\n");break;}
      x = newx;

      newy = _nondet_int();
      if (newy <= y) {
printf("L3\n");break;}
      y = newy;

    } else {
printf("L4\n");

      newy = _nondet_int();
      if (newy >= y) {
printf("L5\n");break;}
      y = newy;

    }
  }
  return 0;
}
