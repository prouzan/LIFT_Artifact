function {:existential true} b0(a7:int, output:int, input:int %FD%, TR1:int, TR2:int, TR3:int): bool;

procedure main()
{
  var a7,output,input %VD%, TR1, TR2, TR3: int;
  a7 := 0;
  output := -1;

  %BE%
TR1 := 0;
TR2 := 0;
TR3 := 0;

  while (output != 0)
  invariant b0(a7,output,input %IC%, TR1, TR2, TR3);
  {
    %BT%
TR1 := 0;
TR2 := 0;
TR3 := 0;
    havoc input;
    if ((input != 1) && (input != 2) && (input != 3) && (input != 4) && (input != 5) && (input != 6)) {
TR1 := 1;
      return;
    }
    a7 := a7 + 1;
    if (a7 == 10) {
TR2 := 1; output := 0; } else {
TR3 := 1; output := input - 1; }
    %IT%
  }
}
