function {:existential true} b0(x:int, y:int %FD%, TR1:int, TR2:int, TR3:int, TR4:int, TR5:int, TR6:int, TR7:int, TR8:int, TR9:int, TR10:int): bool;

procedure main()
{
  var x,y %VD%, TR1, TR2, TR3, TR4, TR5, TR6, TR7, TR8, TR9, TR10: int;

  havoc x;
  havoc y;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;
TR6 := 0;
TR7 := 0;
TR8 := 0;
TR9 := 0;
TR10 := 0;
  	
  while (x > y)
  invariant b0(x,y %IC%, TR1, TR2, TR3, TR4, TR5, TR6, TR7, TR8, TR9, TR10);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;
TR6 := 0;
TR7 := 0;
TR8 := 0;
TR9 := 0;
TR10 := 0;

    if(*)
    {
TR1 := 1;
      x := x - 1;
    }
    else if(*)
    {
TR2 := 1;
      y := y + 1;
    }
    else if(*)
    {
TR3 := 1;
      x := x - 2;
    }
    else if(*)
    {
TR4 := 1;
      y := y + 2;
    }
    else if(*)
    {
TR5 := 1;
      x := x - 3;
    }
    else if(*)
    {
TR6 := 1;
      y := y + 3;
    }
    else if(*)
    {
TR7 := 1;
      x := x - 4;
    }
    else if(*)
    {
TR8 := 1;
      y := y + 4;
    }
    else if(*)
    {
TR9 := 1;
      x := x - 5;
    }
    else
    {
TR10 := 1;  
      y := y + 5;
    }

    %IT%
  }
}
