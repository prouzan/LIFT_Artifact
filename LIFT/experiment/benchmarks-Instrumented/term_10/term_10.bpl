function {:existential true} b0(K:int, x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var K,x,y,i: int;

  havoc K;
  havoc x;
  havoc y;

  assume(%M:i%);
  	
  while (y != K)
  invariant b0(K,x,y,i %Inv:i%);
  {
    assert(i > 0);

    if(x > K)
    {
      x := x - 1;
    }
    else if(x < K)
    {
      x := x + 1;
    }
    if(y > x)
    {
      y := y - 1;
    }
    else if(y < x)
    {
      y := y + 1;
    }

    i := i - 1;
  }
}
