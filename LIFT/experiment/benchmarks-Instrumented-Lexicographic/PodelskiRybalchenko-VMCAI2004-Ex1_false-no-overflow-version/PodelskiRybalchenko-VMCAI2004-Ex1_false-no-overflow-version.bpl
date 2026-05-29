function {:existential true} b0(_i:int, j:int, _i1:int, j1:int %FD%, TR1:int, TR2:int, TR3:int, TR4:int): bool;

procedure main()
{
  var _i,j,nondetNat,nondetPos,_i1,j1,nondetNat1,nondetPos1 %VD%, TR1, TR2, TR3, TR4: int;

  havoc _i;
  havoc j;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
  	
  while (_i + _i1 - j - j1 >= 1)
  invariant b0(_i,j,_i1,j1 %IC%, TR1, TR2, TR3, TR4);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
    havoc nondetNat;
    if (nondetNat < 0)
    {
TR1 := 1;
      nondetNat := - nondetNat;
    }
    _i := _i - nondetNat;
    havoc nondetPos;
    if (nondetPos < 0)
    {
TR2 := 1;
      nondetPos := - nondetPos;
    }        
    nondetPos := nondetPos + 1;
    j := j + nondetPos;
    
    havoc nondetNat1;
    if (nondetNat1 < 0)
    {
TR3 := 1;
      nondetNat1 := - nondetNat1;
    }
    _i1 := _i1 - nondetNat1;
    havoc nondetPos1;
    if (nondetPos1 < 0)
    {
TR4 := 1;
      nondetPos1 := - nondetPos1;
    }        
    nondetPos1 := nondetPos1 + 1;
    j1 := j1 + nondetPos1;

    %IT%
  }
}
