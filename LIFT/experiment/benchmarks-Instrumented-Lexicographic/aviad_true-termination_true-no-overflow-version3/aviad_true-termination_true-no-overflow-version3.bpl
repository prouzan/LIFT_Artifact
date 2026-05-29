function {:existential true} b0(a:int %FD%, TR1:int, TR2:int, ATTM$a_MOD_10:int): bool;

procedure main()
{
  var a %VD%, TR1, TR2: int;
  havoc a;
  
  %BE%
TR1 := 0;
TR2 := 0;
  	
  while (a > 1)
  invariant b0(a %IC%, TR1, TR2, a mod 10);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    
    if(a mod 10 == 0){
TR1 := 1;
      a := a div 10;
    }
    else {
TR2 := 1;
      a := a - 1;
    }
    %IT%
  }
}
