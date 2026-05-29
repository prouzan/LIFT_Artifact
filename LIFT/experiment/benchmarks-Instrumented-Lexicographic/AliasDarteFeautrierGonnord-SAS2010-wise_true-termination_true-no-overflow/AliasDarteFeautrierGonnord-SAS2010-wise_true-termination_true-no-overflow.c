#include <stdio.h>

int main()
{
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  if (x >= 0 && y >= 0)
  {
    while (x - y > 2 || y - x > 2)
    {
      printf("%d,%d\n", x,y);
      if (x < y)
      {
printf("L1\n");
        x = x + 1;
      }
      else
      {
printf("L2\n");
        y = y + 1;
      }
    }
  }
  return 0;
}
