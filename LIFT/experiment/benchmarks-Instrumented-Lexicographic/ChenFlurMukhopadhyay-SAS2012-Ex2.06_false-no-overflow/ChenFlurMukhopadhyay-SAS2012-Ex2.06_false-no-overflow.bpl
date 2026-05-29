function {:existential true} b0(x:int, y:int, oldx:int %FD%): bool;

procedure main()
{
  var x,y,oldx %VD%: int;
  havoc x;
  havoc y;

  %BE%

  while (4*x + y > 0)
  invariant b0(x,y,oldx %IC%);
  {
    %BT%
    oldx := x;
    x := -2*oldx + 4*y;
    y := 4*oldx;
    %IT%
  }
}
