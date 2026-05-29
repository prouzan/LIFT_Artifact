function {:existential true} b0(a:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var a %VD%, TR1, TR2: int;
  havoc a;
  
  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (a > 1)
  invariant b0(a %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    
    if(a mod 2 == 0){
TR1 := 1;
      a := a div 2;
    }
    else {
TR2 := 1;
      a := a - 1;
    }
    %IT%
  }
}
