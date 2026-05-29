function {:existential true} b0(x:int, y:int %FD%, ATTM$x_MOD_y:int): bool;

procedure main()
{
  var x,y %VD%: int;
  havoc x;
  havoc y;

  assume(!(x <= y));
  assume(!(y <= 1));
  %BE%

  while (0 != x mod y)
  invariant b0(x,y %IC%, x mod y);
  {
    %BT%
    y := y - 1;
    %IT%
  }
}
