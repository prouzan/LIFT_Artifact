#include <stdio.h>

int main()
{
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  while (x != 0)
  {
    printf("x:%d,y:%d\n", x, y);
    y--;
    if (x < 10)
      x++;
    else
      x = y;
  }
}