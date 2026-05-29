function {:existential true} b0(x:int, c:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var x,c %VD%, TR1, TR2: int;
  havoc x;
  c := 1;

  %BE%
TR1 := 0;
TR2 := 0;

  while (c > 0)
  invariant b0(x,c %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if (x > 100) {
TR1 := 1;
        x := x-10;
        c := c-1;
    } else {
TR2 := 1;
        x := x+11;
        c := c+1;
    }
    %IT%
  }
}
