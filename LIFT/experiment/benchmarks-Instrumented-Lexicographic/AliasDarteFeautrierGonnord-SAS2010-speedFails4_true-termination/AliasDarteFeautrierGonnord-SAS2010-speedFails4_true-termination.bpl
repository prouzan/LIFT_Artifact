function {:existential true} b0(x:int, n:int, b:int, t:int %FD%, TR1:int, TR2:int ): bool;

procedure main()
{
  var x,n,b,t %VD%, TR1, TR2: int;
  havoc x;
  havoc n;
  havoc b;
  
  
  if(b >= 1){
      t := 1;
  }
  else{
      t := -1;
  }
  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (x <= n)
  invariant b0(x,n,b,t %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if(b >= 1){
TR1 := 1;
        x := x + t;
    }
    else{
TR2 := 1;
        x := x - t;
    }
    %IT%
  }
}
