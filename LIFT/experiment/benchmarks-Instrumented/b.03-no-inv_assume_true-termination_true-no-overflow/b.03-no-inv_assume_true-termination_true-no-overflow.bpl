function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;
  havoc x;
  havoc y;
  
  assume(x > 0);
  assume(%M:i%);
  
  while (x > y && y <= 2147483647 - x)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    
    y := y + x;
    i := i - 1;
  }
}
