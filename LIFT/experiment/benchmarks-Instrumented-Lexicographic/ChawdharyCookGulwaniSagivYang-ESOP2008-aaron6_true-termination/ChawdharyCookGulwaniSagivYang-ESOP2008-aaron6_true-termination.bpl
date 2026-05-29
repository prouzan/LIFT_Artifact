function {:existential true} b0(x:int, tx:int, y:int, ty:int, n:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var x,tx,y,ty,n %VD%, TR1, TR2: int;
  havoc x;
  havoc tx;
  havoc y;
  havoc ty;
  havoc n;

  assume(x + y >= 0);
  %BE%
TR1 := 0;
TR2 := 0;

  while (x <= n && x >= 2 * tx + y && y >= ty + 1 && x >= tx + 1)
  invariant b0(x,tx,y,ty,n %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if (*) {
TR1 := 1;
      tx := x;
      ty := y;
      havoc x;
      havoc y;
    } else {
TR2 := 1;
      tx := x;
      havoc x;
    }
    %IT%
  }
}
