function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;
  x := -10;
  y := 1;
  
  assume(%M:i%);
  	
  while (x != 0)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    x := x + y;
    y := y + 1;

    i := i - 1;
  }
}
