function {:existential true} b0(_i:int, j:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var _i, j %VD%, TR1, TR2: int;

  havoc _i;
  havoc j;

  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (j > 0 && _i > 0 && _i != j)
  invariant b0(_i,j %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if (j < _i)
    {
TR1 := 1;
      j := j - 1;
      havoc _i;
    }
    else if (_i < j)
    {
TR2 := 1;
      _i := _i - 1;
      havoc j;
    }

    %IT%
  }
}
