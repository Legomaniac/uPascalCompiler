{
13
11
}

program test;

var x:integer; y:integer;

function fone(a:integer):integer;
 begin
 a := a+1;
 fone := a;
 end;

function ftwo(var c:integer):integer;
 begin
 c := c+1;
 ftwo := c;
 end;

begin
  x := 10;
  y := 20;

  y := ftwo(x);
  y := fone(y);

  writeln(y+1);
  writeln(x);

end.
