function {:existential true} b0(x:int, y:int, n:int, b:int %FD%, TR1:int, TR2:int, TR3:int, TR4:int): bool;

procedure main()
{
  var x,y,n,b %VD%, TR1, TR2, TR3, TR4: int;
  havoc n;
  havoc b;
  havoc x;
  havoc y;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;

  while (x >= 0 && 0 <= y && y <= n)
  invariant b0(x,y,n,b %IC%, TR1, TR2, TR3, TR4);
  {
	%BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
	if (b == 0) {
TR1 := 1;
			y := y + 1;
			if (*) {
TR2 := 1;
				b := 1;
      }
		} else {
TR3 := 1;
			y := y - 1;
			if (*) {
TR4 := 1;
				x := x - 1;
				b := 0;
			}
		}
	%IT%
  }
}
