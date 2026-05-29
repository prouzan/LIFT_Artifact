function {:existential true} b0(K:int, x:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var K,x %VD%, TR1, TR2: int;
  havoc K;
  havoc x;
  
  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (x != K)
  invariant b0(K,x %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if(x > K){
TR1 := 1;
        x := x - 1;
    }
    else{
TR2 := 1;
        x := x + 1;
    }
    %IT%
  }
}
