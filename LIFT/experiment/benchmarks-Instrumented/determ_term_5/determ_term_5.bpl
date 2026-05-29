function {:existential true} b0(_i:int, j:int, l:int, i:int %Decl:i%): bool;

procedure main()
{
  var _i,j,k,i: int;
  _i := -7;
  j := 2;
  k := 8;
  
  assume(%M:i%);
  	
  while (_i != j)
  invariant b0(_i,j,k,i %Inv:i%);
  {
    assert(i > 0);
    _i := _i + j - k;
    j := j * 2;
    k := k - 1;

    i := i - 1;
  }
}
