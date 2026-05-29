function {:existential true} b0(K:int, x:int, i:int %Decl:i%): bool;

procedure main()
{
  var K,x,i: int;
  havoc K;
  havoc x;
  
  assume(%M:i%);
  	
  while (x != K)
  invariant b0(K,x,i %Inv:i%);
  {
    assert(i > 0);
    if(x > K){
        x := x - 1;
    }
    else{
        x := x + 1;
    }
    i := i - 1;
  }
}
