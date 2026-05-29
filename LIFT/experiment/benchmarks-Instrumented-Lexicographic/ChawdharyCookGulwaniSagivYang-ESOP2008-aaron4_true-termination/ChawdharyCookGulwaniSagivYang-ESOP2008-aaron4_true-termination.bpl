function {:existential true} b0(_i:int, j:int, k:int, an:int, bn:int, tk:int %FD%, TR1:int, TR2:int, TR3:int, TR4:int, TR5:int, TR6:int, TR7:int): bool;

procedure main()
{
  var _i,j,k,an,bn,tk %VD%, TR1, TR2, TR3, TR4, TR5, TR6, TR7: int;
  havoc _i;
  havoc j;
  havoc k;
  havoc an;
  havoc bn;
  havoc tk;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;
TR6 := 0;
TR7 := 0;

  while (((an >= _i && bn >= j) || (an >= _i && bn <= j) || (an <= _i && bn >= j)) && k >= tk + 1)
  invariant b0(_i,j,k,an,bn,tk %IC%, TR1, TR2, TR3, TR4, TR5, TR6, TR7);
  {
	%BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;
TR6 := 0;
TR7 := 0;
	if (an >= _i && bn >= j) {
TR1 := 1;
		if (*) {
TR2 := 1;
			j := j + k;
			tk := k;
			havoc k;
		} else {
TR3 := 1;
			_i := _i + 1;
		}
	} else {
TR4 := 1;if (an >= _i && bn <= j) {
TR5 := 1;
		_i := _i + 1;
	} else {
TR6 := 1;if (an <= _i && bn >= j) {
TR7 := 1;
		j := j + k;
		tk := k;
		havoc k;
	}}}
	%IT%
  }
}
