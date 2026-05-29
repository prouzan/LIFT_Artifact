function {:existential true} b0(_i:int, j:int, k:int, i:int %Decl:i%): bool;

procedure main()
{
  var _i,j,k,i: int;
  _i := 100;
  j := -1;
  k := 1;

  assume(%M:i%);

  while (_i + j + k >= 1)
  invariant b0(_i,j,k,i %Inv:i%);
  {
    assert(i > 0);
    _i := _i - 1;
    j := j - 1;
    k := k + 1;
    i := i - 1;
  }
}
