function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;

  havoc x;
  havoc y;
  
  assume(5*y >= 1);
  assume(%M:i%);
  	
  while (x >= 0)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    x := x - 4 * y + 3;

    i := i - 1;
  }
}
