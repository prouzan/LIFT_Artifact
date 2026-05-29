function {:existential true} b0(x:int, y:int %FD%, TR1:int, TR2:int, TR3:int, TR4:int, TR5:int, TR6:int): bool;

procedure main()
{
  var x,y %VD%, TR1, TR2, TR3, TR4, TR5, TR6: int;
  havoc x;
  havoc y;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;
TR6 := 0;

  while (x != 0 && y > 0)
  invariant b0(x,y %IC%, TR1, TR2, TR3, TR4, TR5, TR6);
  {
	%BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;
TR6 := 0;
	if (x > 0) {
TR1 := 1;
      if (*) {
TR2 := 1;
			    x := x - 1;
          havoc y;
			} else {
TR3 := 1;
			    y := y - 1;
			}
		} else {
TR4 := 1;
      if (*) {
TR5 := 1;
			    x := x + 1;
			} else {
TR6 := 1;
			    y := y - 1;
          havoc x;
			}
		}
	%IT%
  }
}
