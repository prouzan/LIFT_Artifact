function {:existential true} b0(x:int, y:int, N:int %FD%, TR1:int, TR2:int, ATTM$i$ADD$x:int): bool;

procedure main()
{
  var x,y,N %VD%, TR1, TR2: int;
  havoc x;
  havoc y;
  havoc N;
  assume(y <= 0); 
  assume(N > 0);

  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (x != 0)
  invariant b0(x,y,N %IC%, TR1, TR2, i+x);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if(x < N){
TR1 := 1;
      x := x + 1;
    }
    else {
TR2 := 1;
      x := y;
    }
    %IT%
  }
}
