function {:existential true} b0(x:int, y:int, d:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var x,y,d %VD%, TR1, TR2: int;
  havoc x;
  havoc y;
  havoc d;

  %BE%
TR1 := 0;
TR2 := 0;

  while (x > 0 && y > 0 && d > 0)
  invariant b0(x,y,d %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if (*) {
TR1 := 1;
      x := x - 1;
      havoc d;
    } else {
TR2 := 1;
      havoc x;
      y := y - 1;
      d := d - 1;
    }
    %IT%
  }
}
