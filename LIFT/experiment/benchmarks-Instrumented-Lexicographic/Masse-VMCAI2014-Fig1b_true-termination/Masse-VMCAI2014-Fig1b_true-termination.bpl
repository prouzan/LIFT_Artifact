function {:existential true} b0(x:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var x %VD%, TR1, TR2: int;
  havoc x;

  %BE%
TR1 := 0;
TR2 := 0;

  while (x <= 100)
  invariant b0(x %IC%, TR1, TR2);
  {
	%BT%
TR1 := 0;
TR2 := 0;
	if (*) {
TR1 := 1;
		x := -2*x + 2;
	} else {
TR2 := 1;
		x := -3*x - 2;
	}
	%IT%
  }
}
