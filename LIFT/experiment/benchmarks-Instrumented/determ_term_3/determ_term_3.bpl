function {:existential true} b0(x:int, y:int, z:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,z,i: int;
  x := 5;
  y := 1;
  z := 17;
  
  assume(%M:i%);
  	
  while (! (x == y && y == z))
  invariant b0(x,y,z,i %Inv:i%);
  {
    assert(i > 0);
    x := x + 1;
    y := y * 2;
    z := z - 3;

    i := i - 1;
  }
}
