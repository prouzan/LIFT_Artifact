function {:existential true} b0(a:int, b:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var a,b %VD%, TR1, TR2: int;
  havoc a;
  havoc b;

  %BE%
TR1 := 0;
TR2 := 0;

  while (a >= 0)
  invariant b0(a,b %IC%, TR1, TR2);
  {
	%BT%
TR1 := 0;
TR2 := 0;
	a := a + b;
	if (b >= 0) {
TR1 := 1;
		b := -b - 1;
	} else {
TR2 := 1;
		b := -b;
	}
	%IT%
  }
}
