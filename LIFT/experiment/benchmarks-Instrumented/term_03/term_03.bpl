function {:existential true} b0(x:int, y:int, z:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,z,i: int;

  havoc x;
  havoc y;
  havoc z;

  assume(%M:i%);
  	
  while (x > y || y > z)
  invariant b0(x,y,z,i %Inv:i%);
  {
    assert(i > 0);
    x := x - 3;
    y := y - 2;
    z := z - 1;
    
    i := i - 1;
  }
}
