function {:existential true} b0(x:int, y:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var x,y %VD%, TR1, TR2: int;
  havoc x;
  havoc y;

  assume(y <= 0); 

  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (x != 0)
  invariant b0(x,y %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if(x < 10){
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
