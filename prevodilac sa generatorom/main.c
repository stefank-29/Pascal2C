char cifra_stotina(char s){ 
	if (s < 100) {
		return '0';
	}
	else  {
		return chr('0' + s / 100);
	}
}
char cifra_desetica(char s){ 
	if (s < 10) {
		return '0';
	}
	else  {
		return chr('0' + s / 10 % 10);
	}
}
char cifra_jedinica(char s){ 
	return chr('0' + s % 10);
}
int main() {
	char s[100] = {0};
	char t[100] = {0};
	char ascii, tmp;
	int i, j, len;
	scanf("%s", &s);
	i = 1;
	j = 1;
	len = strlen(s);
	while (i <= len)
 {
		ascii = s[i];
		inc(i);
		tmp = cifra_stotina(ascii);
		if (tmp != '0'  ||  tmp == '0'  &&  j > 1) {
			insert(tmp, t, j);
			inc(j);
		}
		insert(cifra_desetica(ascii), t, j);
		inc(j);
		insert(cifra_jedinica(ascii), t, j);
		inc(j);
	}
	printf("%s", t);
	return 0;
}