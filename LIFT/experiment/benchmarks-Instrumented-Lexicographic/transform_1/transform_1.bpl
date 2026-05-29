function {:existential true} b0(x:int, y:int, z:int %FD%, TR1:int, TR2:int, TR3:int, TR4:int): bool;

procedure main()
{
  var x,y,z %VD%, TR1, TR2, TR3, TR4: int;
  havoc x;
  havoc y;
  assume(!(y <= 1));
  z := 0;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;

  while (x > 0)
  invariant b0(x,y,z %IC%, TR1, TR2, TR3, TR4);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
    x := x - y;
    y := y - z;
    if (z == 0) {
TR1 := 1; z := 13; }
      else if (z == 13) {
TR2 := 1; z := -20; }
        else if (z == -20) {
TR3 := 1; z := 7; }
          else {
TR4 := 1; z := 0; }
    %IT%
  }
}
