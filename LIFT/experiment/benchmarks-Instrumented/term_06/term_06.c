#include <stdio.h>

int main()
{
  int x = 0;
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  while (x < 1000)
  {
    printf("x:%d\n", x);
    if (x != 7777) x++;
  }
}
