function {:existential true} b0(x:int, y:int, newx:int, newy:int %FD%, TR1:int, TR2:int, TR3:int, TR4:int, TR5:int): bool;

procedure main()
{
  var x,y,newx,newy %VD%, TR1, TR2, TR3, TR4, TR5: int;
  havoc x;
  havoc y;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;

  while (x > 0 && y > 0)
  invariant b0(x,y,newx,newy %IC%, TR1, TR2, TR3, TR4, TR5);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;

    if (*) {
TR1 := 1;

      havoc newx;
      if (newx >= x) {
TR2 := 1; break; }
      x := newx;

      havoc newy;
      if (newy <= y) {
TR3 := 1; break; }
      y := newy;

    } else {
TR4 := 1;

      havoc newy;
      if (newy >= y) {
TR5 := 1; break; }
      y := newy;

    }

    %IT%
  }
}
