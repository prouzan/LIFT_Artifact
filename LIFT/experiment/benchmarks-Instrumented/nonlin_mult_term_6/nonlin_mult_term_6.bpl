function {:existential true} b0(d:int, b:int, i:int %Decl:i%): bool;

procedure main()
{
  var d,b,i: int;

  havoc d;
  havoc b;

  assume(%M:i%);
  	
  while (d * b > 0)
  invariant b0(d,b,i %Inv:i%);
  {
    assert(i > 0);
    b := -b;
    
    i := i - 1;
  }
}
