function {:existential true} b0(x:int, y:int %FD%, ATTM$x_DIV_y:int): bool;

procedure main()
{
  var x,y %VD%: int;
  havoc x;
  havoc y;

  assume(!(x < y));
  assume(!(y <= 1));
  %BE%

  while (x > 0)
  invariant b0(x,y %IC%, x div y);
  {
    %BT%
    x := x div y;
    %IT%
  }
}
