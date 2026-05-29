function {:existential true} b0(x1:int, x2:int, x3:int %FD%, TR1:int, TR2:int, TR3:int): bool;

procedure main()
{
  var x1,x2,x3 %VD%, TR1, TR2, TR3: int;

  havoc x1;
  havoc x2;
  havoc x3;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
  	
  while (x1 > 0 && x2 > 0 && x3 > 0)
  invariant b0(x1,x2,x3 %IC%, TR1, TR2, TR3);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
    
    if(*)
    {
TR1 := 1;
        x1 := x1 - 1;
    }
    else if(*)
    {
TR2 := 1;
        x2 := x2 - 1;
    }
    else
    {
TR3 := 1;
        x3 := x3 - 1;
    }
    %IT%
  }
}
