#include <stdio.h>

int main() {
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  int x, y;
  x = 0;
  y = 0;

  while (x < 49) {
    printf("#\n");
    x = y%50;
    y ++;
  }
  return 0;
}
