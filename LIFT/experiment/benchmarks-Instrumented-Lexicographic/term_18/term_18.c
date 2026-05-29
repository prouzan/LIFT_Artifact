#include <stdio.h>

int main() {
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  int x, y, z;
  x = 0;
  y = 0;
  z = 0;

  while (x <= 97) {
    printf("#\n");
    x = y%50 + z%50;
    y ++;
    z ++;
  }
  return 0;
}
