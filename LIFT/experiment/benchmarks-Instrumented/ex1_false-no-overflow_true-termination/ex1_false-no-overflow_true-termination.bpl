function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i,r: int;
  havoc x;
  havoc y;

  r := 1;
  
  assume(%M:i%);
  	
  while (y > 0)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    r := r * x;
    y := y - 1;

    i := i - 1;
  }
}
