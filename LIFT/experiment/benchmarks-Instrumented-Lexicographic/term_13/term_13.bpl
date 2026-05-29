function {:existential true} b0(_i:int, j:int, k:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var _i,j,k %VD%, TR1, TR2: int;

  havoc _i;
  havoc j;
  havoc k;

  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (_i + j + k >= 0)
  invariant b0(_i,j,k %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;

    if(*)
    {
TR1 := 1;
      _i := _i - 1;
    }
    else
    {
TR2 := 1;
      j := j + 1;
    }
    k := k - 2;

    %IT%
  }
}
