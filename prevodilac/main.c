void fun(int a, int b) {
	printf(" \n", a, b);
}
int fun2(int x, int y) {
	fun2 = x + y;
}
int fun3(int p, int q, int r) {
	fun3 = q + r;
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