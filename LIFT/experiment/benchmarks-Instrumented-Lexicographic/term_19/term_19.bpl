function {:existential true} b0(x:int, y:int %FD%, TR1:int, TR2:int, ATTM$x_MOD_5:int): bool;

procedure main()
{
  var x,y %VD%, TR1, TR2: int;
  havoc x;
  y := 5;

  assume(!(x <= 10));
  %BE%
TR1 := 0;
TR2 := 0;

  while (x != 2*y)
  invariant b0(x,y %IC%, TR1, TR2, x mod 5);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if (x mod 5 == 1) {
TR1 := 1; x := x + 1; }
      else {
TR2 := 1; x := x - 2; }
    %IT%
  }
}
