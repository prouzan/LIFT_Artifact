function {:existential true} b0(x:int, y:int %FD%): bool;

procedure main()
{
  var x,y %VD%: int;
  havoc x;
  havoc y;

  assume(!(x <= 0 || y <= 0));
  %BE%

  while (x > 0)
  invariant b0(x,y %IC%);
  {
    %BT%
    x := -5*x - 6*y + 18;
    %IT%
  }
}
