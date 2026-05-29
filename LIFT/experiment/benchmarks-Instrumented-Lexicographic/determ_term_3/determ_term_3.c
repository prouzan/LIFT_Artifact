#include<stdio.h>

int main() {
  int x = 5;
  int y = 1;
  int z = 17;
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  
  while (!(x == y && y == z)) {
    printf("#\n");
    x = x + 1;
    y = y * 2;
    z = z - 3;
  }
  return 0;
}
