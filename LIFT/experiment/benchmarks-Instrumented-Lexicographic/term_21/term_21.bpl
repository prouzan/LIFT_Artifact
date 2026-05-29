function {:existential true} b0(z:int %FD%, TR1:int, TR2:int, ATTM$z_MOD_5:int): bool;

procedure main()
{
  var z %VD%, TR1, TR2: int;
  havoc z;

  %BE%
TR1 := 0;
TR2 := 0;

  while (z >= 0)
  invariant b0(z %IC%, TR1, TR2, z mod 5);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if (z mod 5 == 0) {
TR1 := 1; z := z - 5; }
      else {
TR2 := 1; z := z + 1; }
    %IT%
  }
}
