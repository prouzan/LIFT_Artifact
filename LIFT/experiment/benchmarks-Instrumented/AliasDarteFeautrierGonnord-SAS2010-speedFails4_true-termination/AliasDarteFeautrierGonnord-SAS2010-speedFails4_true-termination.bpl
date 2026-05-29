function {:existential true} b0(x:int, n:int, b:int, t:int, i:int %Decl:i% ): bool;

procedure main()
{
  var x,n,b,t,i: int;
  havoc x;
  havoc n;
  havoc b;
  
  
  if(b >= 1){
      t := 1;
  }
  else{
      t := -1;
  }
  assume(%M:i%);
  	
  while (x <= n)
  invariant b0(x,n,b,t,i %Inv:i%);
  {
    assert(i > 0);
    if(b >= 1){
        x := x + t;
    }
    else{
        x := x - t;
    }
    i := i - 1;
  }
}
