function {:existential true} b0(x:int, y:int, z:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,z,i: int;

  havoc x;
  havoc y;
  havoc z;
  
  assume(10 * y > z && z < 10);
  assume(%M:i%);
  	
  while (x >= 0)
  invariant b0(x,y,z,i %Inv:i%);
  {
    assert(i > 0);
    x := x - 10 * y + z;

    i := i - 1;
  }
}
