function {:existential true} b0(x:int, y:int, z:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var x,y,z %VD%, TR1, TR2: int;
  havoc x;
  havoc y;
  havoc z;

  %BE%
TR1 := 0;
TR2 := 0;

  while (x >= y)
  invariant b0(x,y,z %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if (z > 1) {
TR1 := 1;
      z := z - 1;
      x := x + z;
    } else {
TR2 := 1;
      y := y + 1;
    }
    %IT%
  }
}
