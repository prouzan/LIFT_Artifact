function {:existential true} b0(x:int, y:int, old_x:int, old_y:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var x,y,old_x,old_y %VD%, TR1, TR2: int;
  havoc x;
  havoc y;

  %BE%
TR1 := 0;
TR2 := 0;

  while (x > 0 && y > 0)
  invariant b0(x,y,old_x,old_y %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    old_x := x;
    old_y := y;
    if (*) {
TR1 := 1;
      x := old_x - 1;
      y := old_x;
    } else {
TR2 := 1;
      x := old_y - 2;
      y := old_x + 1;
    }
    %IT%
  }
}
