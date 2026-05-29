function {:existential true} b0(_i:int, j:int, k:int, i:int %Decl:i%): bool;

procedure main()
{
  var _i,j,k,i: int;

  havoc _i;
  havoc j;
  havoc k;

  assume(%M:i%);
  	
  while (_i + j + k >= 0)
  invariant b0(_i,j,k,i %Inv:i%);
  {
    assert(i > 0);

    if(*)
    {
      _i := _i - 1;
    }
    else
    {
      j := j + 1;
    }
    k := k - 2;

    i := i - 1;
  }
}
