function {:existential true} b0(_i:int, j:int, a:int, b:int %FD%, TR1:int, TR2:int, TR3:int, TR4:int, ATTM$_i$ADD$j$ADD$a$ADD$b: int): bool;

procedure main()
{
  var _i,j,a,b %VD%, TR1, TR2, TR3, TR4: int;

  havoc _i;
  havoc j;
  havoc a;
  havoc b;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
  	
  while (_i + j + a + b == 0)
  invariant b0(_i,j,a,b %IC%, TR1, TR2, TR3, TR4, _i + j + a + b);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;

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
    if(*)
    {
TR3 := 1;
      a := a - 2;
    }
    else
    {
TR4 := 1;
      b := b + 2;
    }

    %IT%
  }
}
