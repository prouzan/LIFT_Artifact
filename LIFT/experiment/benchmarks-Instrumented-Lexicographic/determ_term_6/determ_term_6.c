#include <stdio.h>

int main()
{
  int x = 8;
  int y = 9;
  int z = -2;
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  while (x + y + z != 0)
  {
    printf("#\n");
    int oldx = x;
    x = -y + 1;
    y = 2 * oldx + z;
    z = z * 3;
  }
  return 0;
}
