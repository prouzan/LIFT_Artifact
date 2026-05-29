function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;

  havoc x;
  havoc y;

  assume(x > 1);
  assume(y > 1);
  assume(%M:i%);
  	
  while (x < 10000)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    x := x * y;
    
    i := i - 1;
  }
}
