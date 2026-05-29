function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;

  havoc x;
  havoc y;

  assume(x > y);
  assume(y > 1);
  assume(%M:i%);
  	
  while (x > y)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    if(*)
    {
      x := x mod y;
    }
    else
    {
      x := x - y;
    }
    
    i := i - 1;
  }
}
