function {:existential true} b0(x:int, y:int, z:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var x,y,z %VD%, TR1, TR2: int;

  havoc x;
  havoc y;
  havoc z;

  assume(x <= z && y <= z);
  %BE%
TR1 := 0;
TR2 := 0;

  while (x != y)
  invariant b0(x,y,z %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;

    x := x + 1;
    y := y + 1;
    if(x > z)
    {
TR1 := 1;
      x := z;
    }
    if(y > z)
    {
TR2 := 1;
      y := y - 1;
    }    
    %IT%
  }
}
