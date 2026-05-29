function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;

  havoc x;
  havoc y;

  assume(%M:i%);
  	
  while (x > y)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);

    if(*)
    {
      x := x - 1;
    }
    else if(*)
    {
      y := y + 1;
    }
    else if(*)
    {
      x := x - 2;
    }
    else if(*)
    {
      y := y + 2;
    }
    else if(*)
    {
      x := x - 3;
    }
    else if(*)
    {
      y := y + 3;
    }
    else if(*)
    {
      x := x - 4;
    }
    else if(*)
    {
      y := y + 4;
    }
    else if(*)
    {
      x := x - 5;
    }
    else
    {  
      y := y + 5;
    }

    i := i - 1;
  }
}
