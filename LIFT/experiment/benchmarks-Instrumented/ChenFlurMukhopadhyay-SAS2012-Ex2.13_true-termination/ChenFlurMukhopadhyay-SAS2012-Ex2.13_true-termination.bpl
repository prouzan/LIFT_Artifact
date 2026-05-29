function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;
  havoc x;
  havoc y;
  
  assume(%M:i%);
  	
  while (x - y > 0)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    x := y - x;
    y := y + 1;
    
    i := i - 1;
  }
}
