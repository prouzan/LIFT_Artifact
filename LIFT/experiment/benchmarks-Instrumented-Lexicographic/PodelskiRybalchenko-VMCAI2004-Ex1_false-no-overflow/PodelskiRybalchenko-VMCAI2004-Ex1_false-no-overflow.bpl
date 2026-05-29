function {:existential true} b0(_i:int, j:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var _i,j,nondetNat,nondetPos %VD%, TR1, TR2: int;

  havoc _i;
  havoc j;

  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (_i - j >= 1)
  invariant b0(_i,j %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
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
    
    %IT%
  }
}
