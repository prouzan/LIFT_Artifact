function {:existential true} b0(x:int, y:int, z:int, N:int %FD%, TR1:int, TR2:int, TR3:int, TR4:int, TR5:int): bool;

procedure main()
{
  var x,y,z,N,cond1,cond2,cond3,cond4 %VD%, TR1, TR2, TR3, TR4, TR5: int;
  x := 0;
  y := 0;
  z := 1;
  havoc N;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;

  while (x < N)
  invariant b0(x,y,z,N %IC%, TR1, TR2, TR3, TR4, TR5);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
TR5 := 0;
    havoc cond1;
    havoc cond2;
    havoc cond3;
    havoc cond4;
    if      (cond1 == 0 && z == 1) {
TR1 := 1; y := 5; z := 0; }
    else if (cond2 == 0 && z == 0) {
TR2 := 1; y := -3; z := 1; }
    else if (cond3 == 0 && z == 1) {
TR3 := 1; y := 7; z := 0; }
    else if (cond4 == 0 && z == 0) {
TR4 := 1; y := -2; z := 1; }
    else {
TR5 := 1; y := 1; }

    x := x + y;
    %IT%
  }
}
