function {:existential true} b0(_i:int, j:int, _i1:int, j1:int, i:int %Decl:i%): bool;

procedure main()
{
  var _i,j,nondetNat,nondetPos,_i1,j1,nondetNat1,nondetPos1,i: int;

  havoc _i;
  havoc j;

  assume(%M:i%);
  	
  while (_i + _i1 - j - j1 >= 1)
  invariant b0(_i,j,_i1,j1,i %Inv:i%);
  {
    assert(i > 0);
    havoc nondetNat;
    if (nondetNat < 0)
    {
      nondetNat := - nondetNat;
    }
    _i := _i - nondetNat;
    havoc nondetPos;
    if (nondetPos < 0)
    {
      nondetPos := - nondetPos;
    }        
    nondetPos := nondetPos + 1;
    j := j + nondetPos;
    
    havoc nondetNat1;
    if (nondetNat1 < 0)
    {
      nondetNat1 := - nondetNat1;
    }
    _i1 := _i1 - nondetNat1;
    havoc nondetPos1;
    if (nondetPos1 < 0)
    {
      nondetPos1 := - nondetPos1;
    }        
    nondetPos1 := nondetPos1 + 1;
    j1 := j1 + nondetPos1;

    i := i - 1;
  }
}
