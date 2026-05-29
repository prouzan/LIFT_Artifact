#include <stdio.h>

int main()
{
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  while (x != 0)
  {
    printf("%d,%d\n", x, y);
    y--;
    if (x < 10)
      {
printf("L1\n");x++;}
    else
      {
printf("L2\n");x = y;}
  }
}