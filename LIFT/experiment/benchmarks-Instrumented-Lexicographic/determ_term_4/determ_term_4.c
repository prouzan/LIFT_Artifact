#include<stdio.h>

int main() {
  int x = 4;
  int y = -5;
  int z = 1;
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  
  while (x + y != z) {
    printf("#\n");
    x = x * -3;
    y = y + 2;
    z = z - 36;
  }
  return 0;
}
