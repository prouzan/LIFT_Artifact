function {:existential true} b0(x:int, y:int %FD%, TR1:int, TR2:int, TR3:int, TR4:int): bool;

procedure main()
{
  var x,y,c %VD%, TR1, TR2, TR3, TR4: int;
  havoc x;
  havoc y;
  
  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
  
  c := 0;
  while (x + y > 0)
  invariant b0(x,y %IC%, TR1, TR2, TR3, TR4);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
    if (x > y){
TR1 := 1;
      x := x - 1;
    }
    else {
TR2 := 1;
      if (x == y){
TR3 := 1;
        x := x - 1;
      }
      else {
TR4 := 1;
        y := y - 1;
      }
    }
    %IT%
  }
}
