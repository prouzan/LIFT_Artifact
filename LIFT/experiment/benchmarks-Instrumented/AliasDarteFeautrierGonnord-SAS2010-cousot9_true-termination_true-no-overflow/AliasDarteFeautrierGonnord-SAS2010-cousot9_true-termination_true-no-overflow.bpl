function {:existential true} b0(_i:int, j:int, N:int, i:int %Decl:i%): bool;

procedure main()
{
  var _i,j,N,i: int;
  havoc j;
  havoc N;
  _i := N;

  assume(%M:i%);

  while (_i > 0)
  invariant b0(_i,j,N,i %Inv:i%);
  {
	assert(i > 0);
	if (j > 0) {
		j := j - 1;
	} else {
		j := N;
		_i := _i - 1;
	}
	i := i - 1;
  }
}
