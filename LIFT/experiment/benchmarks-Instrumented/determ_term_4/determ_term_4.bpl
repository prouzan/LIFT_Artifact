function {:existential true} b0(x:int, y:int, z:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,z,i: int;
  x := 4;
  y := -5;
  z := 1;
  
  assume(%M:i%);
  	
  while (x + y != z)
  invariant b0(x,y,z,i %Inv:i%);
  {
    assert(i > 0);
    x := x * -3;
    y := y + 2;
    z := z - 36;

    i := i - 1;
  }
}
