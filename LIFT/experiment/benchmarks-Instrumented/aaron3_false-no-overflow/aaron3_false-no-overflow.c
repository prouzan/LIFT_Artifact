#include <stdio.h>
#include <stdlib.h>
int _nondet_int(void)
{
  return rand();
}
int _nondet_2(void)
{
  return rand() % 2;
}

int main()
{
  int x, y, z, tx;
  scanf("%d%d%d%d", &x, &y, &z, &tx);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  while (x >= y && x <= tx + z)
  {
    printf("x:%d,y:%d,z:%d,tx:%d\n", x, y, z, tx);
    if (_nondet_2())
    {
      z = z - 1;
      tx = x;
      x = _nondet_int();
    }
    else
    {
      y = y + 1;
    }
  }
  return 0;
}
