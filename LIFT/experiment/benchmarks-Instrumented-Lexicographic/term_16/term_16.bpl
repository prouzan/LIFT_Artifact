function {:existential true} b0(x:int, y:int, z:int %FD%, ATTM$x_DIV_50:int): bool;

procedure main()
{
  var x,y,z %VD%: int;
  havoc x;
  havoc y;

  %BE%

  while (x div 50 == y)
  invariant b0(x,y,z %IC%, x div 50);
  {
    %BT%
    havoc z;
    x := x + 1 + 50*z;
    y := y + z;
    %IT%
  }
}
