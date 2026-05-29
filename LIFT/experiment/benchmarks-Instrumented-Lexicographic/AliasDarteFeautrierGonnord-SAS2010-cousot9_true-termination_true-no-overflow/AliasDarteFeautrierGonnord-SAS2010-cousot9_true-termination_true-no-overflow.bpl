function {:existential true} b0(_i:int, j:int, N:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var _i,j,N %VD%, TR1, TR2: int;
  havoc j;
  havoc N;
  _i := N;

  %BE%
TR1 := 0;
TR2 := 0;

  while (_i > 0)
  invariant b0(_i,j,N %IC%, TR1, TR2);
  {
	%BT%
TR1 := 0;
TR2 := 0;
	if (j > 0) {
TR1 := 1;
		j := j - 1;
	} else {
TR2 := 1;
		j := N;
		_i := _i - 1;
	}
	%IT%
  }
}
