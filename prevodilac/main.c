void fun(int a, int b, char s){ 
	int x;
	char c;
	printf("%d %d %c%d\n", a, b, s, x);
	scanf("%d", &x);
	scanf("%c", &c);
	printf("%d %d\n", x, b);
}
int fun2(int x, int y, char c){ 
	int a;
	printf("%d%d%d%d%c%c\n", a, x, y, c);
	return x + y;
}
int fun3(int p, int q, int r){ 
	int a;
	return q + r;
	printf("%d %d%d%d\n", q, r, a);
}
int main() {
	int x, y, i;
	int arr1[3];
	int arr2[3] = {1, 23, 456};
	int arr3[3];
	y = 5;
	for (i = 1; i <= 3; i = i + 1) {
		arr1[i] = arr2[i];
		arr1[i] = fun2(arr1[i], arr2[i]);
		fun(arr1[i], arr2[i]);
	}
	return 0;
}