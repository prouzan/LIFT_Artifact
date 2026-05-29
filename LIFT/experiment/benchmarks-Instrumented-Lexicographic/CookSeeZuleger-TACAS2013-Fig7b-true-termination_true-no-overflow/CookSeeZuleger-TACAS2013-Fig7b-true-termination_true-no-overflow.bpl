function {:existential true} b0(x:int, y:int, z:int %FD%, TR1:int, TR2:int, TR3:int): bool;

procedure main()
{
  var x,y,z %VD%, TR1, TR2, TR3: int;
  havoc x;
  havoc y;
  havoc z;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;

  while (x > 0 && y > 0 && z > 0)
  invariant b0(x,y,z %IC%, TR1, TR2, TR3);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
    if (*) {
TR1 := 1;
      x := x - 1;
    } else if (*) {
TR2 := 1;
      y := y - 1;
      havoc z;
    } else {
TR3 := 1;
      z := z - 1;
      havoc x;
    }
    %IT%
  }
}
