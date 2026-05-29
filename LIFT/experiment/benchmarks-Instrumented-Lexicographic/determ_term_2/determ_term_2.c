#include<stdio.h>

int main() {
  int x = -36;
  int y = 0;
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  
  while (x != 0) {
    printf("#\n");
    x = x + y;
    y = y + 1;
  }
  return 0;
}
