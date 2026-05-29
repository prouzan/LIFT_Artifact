function {:existential true} b0(j:int, b:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var j,b %VD%, TR1, TR2: int;

  havoc j;
  havoc b;

  assume(b > 1);
  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (j < 100)
  invariant b0(j,b %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if (j <= 0)
    {
TR1 := 1;
      j := 1;
    }
    else
    {
TR2 := 1;
      j := j * b;
    }
    
    %IT%
  }
}
