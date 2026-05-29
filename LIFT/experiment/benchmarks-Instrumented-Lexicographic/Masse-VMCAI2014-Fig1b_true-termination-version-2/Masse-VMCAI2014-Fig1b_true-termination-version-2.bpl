function {:existential true} b0(x:int %FD%, TR1:int, TR2:int, TR3:int, TR4:int): bool;

procedure main()
{
  var x %VD%, TR1, TR2, TR3, TR4: int;
  havoc x;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;

  while (x <= 100)
  invariant b0(x %IC%, TR1, TR2, TR3, TR4);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
TR4 := 0;
    if (*) {
TR1 := 1;
        x := - 2 * x + 2;
    } else if (*) {
TR2 := 1;
        x := - 3 * x - 2;
    } else if (*) {
TR3 := 1;
        x := - 4 * x + 2;
    } else {
TR4 := 1;
        x := - 5 * x - 2;
    }
    %IT%
  }
}
