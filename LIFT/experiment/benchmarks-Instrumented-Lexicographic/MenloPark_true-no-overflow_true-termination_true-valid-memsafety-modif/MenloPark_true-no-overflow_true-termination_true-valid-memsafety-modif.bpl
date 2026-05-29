function {:existential true} b0(x:int, y:int, z:int %FD%): bool;

procedure main()
{
  var x,y,z %VD%: int;
  havoc x;
  havoc y;

  assume(!(y <= 1));
  %BE%

  z := 1;

  while (x > 0)
  invariant b0(x,y,z %IC%);
  {
    %BT%
    x := x - y;
    y := y - z;
    z := -z;
    %IT%
  }
}
