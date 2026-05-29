function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;

  havoc x;
  havoc y;

  assume(x div y > 1);
  assume(y > 0);
  assume(%M:i%);
  	
  while (x != y)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    x := x - 1;
    
    i := i - 1;
  }
}
