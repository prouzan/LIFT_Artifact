function {:existential true} b0(_i:int, j:int, i:int %Decl:i%): bool;

procedure main()
{
  var _i,j,nondetNat,nondetPos,i: int;

  havoc _i;
  havoc j;

  assume(%M:i%);
  	
  while (_i - j >= 1)
  invariant b0(_i,j,i %Inv:i%);
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
    
    i := i - 1;
  }
}
