function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;

  havoc y;
  
  x := y + 42;

  assume(%M:i%);
  	
  while (x >= 0)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    y := 2 * y - x;
    x := (y + x) div 2;

    i := i - 1;
  }
}
