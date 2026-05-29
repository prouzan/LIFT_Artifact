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
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  //prevent overflows
  if (!(-1073741823 <= tx && tx <= 1073741823))
    return 0;
  if (!(-1073741823 <= z && z <= 1073741823))
    return 0;
  if (!(-1073741823 <= x && x <= 1073741823))
    return 0;
  if (!(y <= 1073741823))
    return 0;

  while (x >= y && x <= tx + z)
  {
    printf("%d,%d,%d,%d\n", x, y, z, tx);
    if (_nondet_2())
    {
printf("L1\n");
      z = z - 1;
      tx = x;
      x = _nondet_int();
      if (!(-1073741823 <= x && x <= 1073741823))
        return 0;
    }
    else
    {
printf("L2\n");
      y = y + 1;
    }
  }
  return 0;
}
