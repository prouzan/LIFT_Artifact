#include <stdio.h>

int main()
{
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  if (x >= 0 && y >= 0)
  {
    while (x - y > 2 || y - x > 2)
    {
      printf("x:%d,y:%d\n", x, y);
      if (x < y)
      {
        x = x + 1;
      }
      else
      {
        y = y + 1;
      }
    }
  }
  return 0;
}
