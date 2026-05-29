function {:existential true} b0(a7:int, output:int, input:int, i:int %Decl:i%): bool;

procedure main()
{
  var a7,output,input,i: int;
  a7 := 0;
  output := -1;

  assume(%M:i%);

  while (output != 0)
  invariant b0(a7,output,input,i %Inv:i%);
  {
    assert(i > 0);
    havoc input;
    if ((input != 1) && (input != 2) && (input != 3) && (input != 4) && (input != 5) && (input != 6)) {
      return;
    }
    a7 := a7 + 1;
    if (a7 == 10) { output := 0; } else { output := input - 1; }
    i := i - 1;
  }
}
