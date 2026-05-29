function {:existential true} b0(a:int, b:int, olda:int, i:int %Decl:i% ): bool;

procedure main()
{
  var a,b,olda,i: int;
  havoc a;
  havoc b;

  assume(%M:i%);
  	
  while (a > 0)
  invariant b0(a,b,olda,i %Inv:i%);
  {
    assert(i > 0);
    olda := a;
    a := 3*olda - 4*b;
    b := 4*olda + 3*b;
    i := i - 1;
  }
}
