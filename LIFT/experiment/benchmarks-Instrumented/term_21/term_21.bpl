function {:existential true} b0(z:int, i:int %Decl:i%, ATTM$z_MOD_5:int): bool;

procedure main()
{
  var z,i: int;
  havoc z;

  assume(%M:i%);

  while (z >= 0)
  invariant b0(z,i %Inv:i%, z mod 5);
  {
    assert(i > 0);
    if (z mod 5 == 0) { z := z - 5; }
      else { z := z + 1; }
    i := i - 1;
  }
}
