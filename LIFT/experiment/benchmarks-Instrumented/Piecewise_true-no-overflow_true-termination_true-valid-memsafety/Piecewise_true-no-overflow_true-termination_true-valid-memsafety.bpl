function {:existential true} b0(_i:int, j:int, i:int %Decl:i%): bool;

procedure main()
{
  var _i, j, i: int;

  havoc _i;
  havoc j;

  assume(%M:i%);
  	
  while (j > 0 && _i > 0 && _i != j)
  invariant b0(_i,j,i %Inv:i%);
  {
    assert(i > 0);
    if (j < _i)
    {
      j := j - 1;
      havoc _i;
    }
    else if (_i < j)
    {
      _i := _i - 1;
      havoc j;
    }

    i := i - 1;
  }
}
