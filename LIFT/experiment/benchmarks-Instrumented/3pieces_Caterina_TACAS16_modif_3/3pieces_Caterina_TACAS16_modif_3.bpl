function {:existential true} b0(x:int, y:int, N:int, i:int %Decl:i%, ATTM$i$ADD$x:int): bool;

procedure main()
{
  var x,y,N,i: int;
  havoc x;
  havoc y;
  havoc N;
  assume(y <= 0); 
  assume(N > 0);

  assume(%M:i%);
  	
  while (x != 0)
  invariant b0(x,y,N,i %Inv:i%, i+x);
  {
    assert(i > 0);
    if(x < N){
      x := x + 1;
    }
    else {
      x := y;
    }
    i := i - 1;
  }
}
