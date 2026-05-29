function {:existential true} b0(x:int, y:int %FD%): bool;

procedure main()
{
  var x,y %VD%: int;
  havoc x;
  havoc y;

  assume(!(x <= 0));
  assume(!(y <= 0));

  x := x*y;

  %BE%

  while (x != 0)
  invariant b0(x,y %IC%);
  {
    %BT%
    x := x - y;
    %IT%
  }
}
