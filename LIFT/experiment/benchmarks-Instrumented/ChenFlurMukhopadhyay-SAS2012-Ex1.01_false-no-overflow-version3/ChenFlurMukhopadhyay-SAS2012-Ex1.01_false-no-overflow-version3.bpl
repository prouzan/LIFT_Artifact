function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;
  havoc x;
  havoc y;
  
  assume(%M:i%);
  	
  while (x < 0 && y > 0)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    x := -3 * x - 17;
    y := -4 * y + 8;
    
    i := i - 1;
  }
}
