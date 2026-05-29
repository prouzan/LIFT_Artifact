function {:existential true} b0(c:int, x:int, i:int %Decl:i%): bool;

procedure main()
{
  var c,x,i: int;

  havoc c;
  havoc x;

  assume(c >= 2);
  assume(%M:i%);
  	
  while (x + c >= 0)
  invariant b0(c,x,i %Inv:i%);
  {
    assert(i > 0);
    x := x - c;
    c := c + 1;
    
    i := i - 1;
  }
}
