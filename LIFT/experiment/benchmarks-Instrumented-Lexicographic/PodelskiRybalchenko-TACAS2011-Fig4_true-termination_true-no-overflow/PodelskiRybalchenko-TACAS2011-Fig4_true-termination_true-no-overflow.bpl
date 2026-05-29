function {:existential true} b0(x:int, y:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var x,y %VD%, TR1, TR2: int;
  havoc x;
  havoc y;

  %BE%
TR1 := 0;
TR2 := 0;

  while (x > 0 && y > 0)
  invariant b0(x,y %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if (*) {
TR1 := 1;
      x := x - 1;
      havoc y;
    } else {
TR2 := 1;
      y := y - 1;
    }
    %IT%
  }
}
