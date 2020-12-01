#include <stdio.h>

void getData (int* dividend, int* divisor);
void divide	 (int dividend, int divisor, int* quotient, int* remainder);
void print	 (int quotient, int remainder);

int main(void){
	int dividend, divisor, quotient, remainder;
	
	getData(&dividend, &divisor);
	divide	 (dividend,divisor, &quotient, &remainder);
	print(quotient, remainder);
	
}

void getData (int* dividend, int* divisor){
	scanf("%d,%d",dividend,divisor);
}

void divide	 (int dividend, int divisor, int* quotient, int* remainder){
	*quotient = dividend/divisor;
	*remainder = dividend%divisor;
}

void print	 (int quotient, int remainder){
	printf("%d...%d",quotient,remainder);
}
