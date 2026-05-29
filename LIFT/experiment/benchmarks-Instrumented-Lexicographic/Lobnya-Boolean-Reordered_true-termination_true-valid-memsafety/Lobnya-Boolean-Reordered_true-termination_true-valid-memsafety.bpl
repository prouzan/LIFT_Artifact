function {:existential true} b0(x:int, b:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var x,b %VD%, TR1, TR2: int;

  havoc x;
  havoc b;
  
  assume(x >= -2147483647);
  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (b != 0)
  invariant b0(x,b %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    havoc b;
    x := x - 1;
    if (x >= 0){
TR1 := 1;
        b := 1;
    }
    else{
TR2 := 1;
        b := 0;
    }
    %IT%
  }
}
