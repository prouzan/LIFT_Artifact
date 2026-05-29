function {:existential true} b0(K:int, x:int, y:int %FD%, TR1:int, TR2:int, TR3:int, TR4:int, TR5:int): bool;

procedure main()
{
  var K,x,y %VD%, TR1, TR2, TR3, TR4, TR5: int;
  havoc K;
  havoc x;
  havoc y;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;

  while (y != K)
  invariant b0(K,x,y %IC%, TR1, TR2, TR3, TR4, TR5);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;
    if (x > K) {
TR1 := 1;
      x := x - 1;
    } else if (x < K) {
TR2 := 1;
      x := x + 1;
    } else {
TR3 := 1; x := K + 1; }
    if (y > x) {
TR4 := 1;
      y := y - 1;
    } else if (y < x) {
TR5 := 1;
      y := y + 1;
    }
    %IT%
  }
}
