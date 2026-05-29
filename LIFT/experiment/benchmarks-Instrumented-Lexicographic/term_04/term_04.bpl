function {:existential true} b0(j:int, d:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var j,d %VD%, TR1, TR2: int;

  havoc j;
  havoc d;

  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (j > 0 && d > 0)
  invariant b0(j,d %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if(*)
    {
TR1 := 1;
      j := j - 1;
    }
    else
    {
TR2 := 1;
      d := d - 1;
    }
    
    %IT%
  }
}
