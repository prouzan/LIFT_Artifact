function {:existential true} b0(x:int, y:int, z:int, N:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,z,N,cond1,cond2,cond3,cond4,i: int;
  x := 0;
  y := 0;
  z := 1;
  havoc N;

  assume(%M:i%);

  while (x < N)
  invariant b0(x,y,z,N,i %Inv:i%);
  {
    assert(i > 0);
    havoc cond1;
    havoc cond2;
    havoc cond3;
    havoc cond4;
    if      (cond1 == 0 && z == 1) { y := 5; z := 0; }
    else if (cond2 == 0 && z == 0) { y := -3; z := 1; }
    else if (cond3 == 0 && z == 1) { y := 7; z := 0; }
    else if (cond4 == 0 && z == 0) { y := -2; z := 1; }
    else { y := 1; }

    x := x + y;
    i := i - 1;
  }
}
