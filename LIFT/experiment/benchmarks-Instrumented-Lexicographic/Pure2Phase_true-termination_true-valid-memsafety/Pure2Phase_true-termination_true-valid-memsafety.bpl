function {:existential true} b0(y:int, z:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var y,z %VD%, TR1, TR2: int;

  havoc y;
  havoc z;

  assume(-1073741823 <= y && y <= 1073741823);
  assume(z <= 1073741823);
  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (z >= 0)
  invariant b0(y,z %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;

    y := y - 1;
    if(y >= 0)
    {
TR1 := 1;
        havoc z;
        assume(z <= 1073741823);
    }
    else
    {
TR2 := 1;
        z := z - 1;
    }

    %IT%
  }
}
