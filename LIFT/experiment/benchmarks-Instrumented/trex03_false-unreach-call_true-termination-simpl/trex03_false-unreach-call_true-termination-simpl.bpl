function {:existential true} b0(x1:int, x2:int, x3:int, i:int %Decl:i%): bool;

procedure main()
{
  var x1,x2,x3,i: int;

  havoc x1;
  havoc x2;
  havoc x3;

  assume(%M:i%);
  	
  while (x1 > 0 && x2 > 0 && x3 > 0)
  invariant b0(x1,x2,x3,i %Inv:i%);
  {
    assert(i > 0);
    
    if(*)
    {
        x1 := x1 - 1;
    }
    else if(*)
    {
        x2 := x2 - 1;
    }
    else
    {
        x3 := x3 - 1;
    }
    i := i - 1;
  }
}
