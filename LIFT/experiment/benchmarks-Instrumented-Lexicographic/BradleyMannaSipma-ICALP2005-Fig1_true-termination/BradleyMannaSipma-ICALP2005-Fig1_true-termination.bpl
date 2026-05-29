function {:existential true} b0(x:int, y:int, N:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var x,y,N %VD%, TR1, TR2: int;
  havoc x;
  havoc y;
  havoc N;
  
  assume(N < 536870912 && x < 536870912 && y < 536870912 && x >= -1073741824);
  assume(x + y >= 0);
  %BE%
TR1 := 0;
TR2 := 0;
  
  while (x <= N)
  invariant b0(x,y,N %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;

    if (*){
TR1 := 1;
      x := 2 * x + y;
      y := y + 1;
    }
    else {
TR2 := 1;
      x := x + 1;
    }
    %IT%
  }
}
