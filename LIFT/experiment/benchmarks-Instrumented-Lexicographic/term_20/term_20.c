#include <stdio.h>

int main() {
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  int x = 0;
  int y = 0;
  int z = 0;

  while (x < 100) {
    printf("#\n");
    x = x + y;
    y = z + 1;
    z = y - 1;
  }
  return 0;
}
