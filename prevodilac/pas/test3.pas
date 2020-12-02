procedure fun(a, b: integer; s: char);
var 
	x: integer;
	c: char;
begin
	writeln(a, ' ', b, ' ', s, x);
	readln(x);
	readln(c);
	writeln(x, ' ', b);
end;

function fun2(x, y: integer; c: char) : integer;
var 
	a: integer;
begin
	writeln(a, x, y, c);
	fun2 := x + y;
	readln(a);
end;

function fun3(p, q, r: integer) : integer;
var 
	a: integer;
begin
	fun3 := q + r;
	writeln(q, ' ', r, a);
	readln(a);
end;

var
	x, y, i: integer;
	arr1: array [1..3] of integer;
	arr2: array [1..3] of integer = (1, 23, 456);
	arr3: array [1..3] of integer;

begin
	y := 5 ;

	for i := 1 to 3 do
	begin
		arr1[i] := arr2[i];
		arr1[i] := fun2(arr1[i], arr2[i]);
		fun(arr1[i], arr2[i]);
	end;
end.
