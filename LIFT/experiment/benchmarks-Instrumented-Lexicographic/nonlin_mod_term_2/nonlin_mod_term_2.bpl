function {:existential true} b0(x:int, y:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var x,y %VD%, TR1, TR2: int;

  havoc x;
  havoc y;

  assume(x > y);
  assume(y > 1);
  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (x > y)
  invariant b0(x,y %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if(*)
    {
TR1 := 1;
      x := x mod y;
    }
    else
    {
TR2 := 1;
      x := x - y;
    }
    
    %IT%
  }
}
