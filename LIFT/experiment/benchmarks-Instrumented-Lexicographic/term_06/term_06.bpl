function {:existential true} b0(x:int %FD%, TR1:int): bool;

procedure main()
{
  var x %VD%, TR1: int;

  x := 0;

  %BE%
TR1 := 0;

  while (x < 1000)
  invariant b0(x %IC%, TR1);
  {
    %BT%
TR1 := 0;
    if (x != 7777) {
TR1 := 1; x := x + 1; }
    %IT%
  }
}
