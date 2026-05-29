#include <stdio.h>
#include <stdlib.h>
int _nondet_int(void)
{
  return rand();
}

int main()
{
  int x, y, z, tx;
  scanf("%d%d%d%d", &x, &y, &z, &tx);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  while (x >= y && x <= tx + z)
  {
    printf("%d,%d,%d,%d\n", x, y, z, tx);
    z = z - 1;
    tx = x;
    x = _nondet_int();
  }
  return 0;
}
