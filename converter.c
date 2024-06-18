#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>
int convertNumbers(int number,int in,int out){
    int resultado = 0;
    for (int i = 0; number != 0; i++) 
    {
        resultado = resultado + ((number % out) * pow(in,i));
        number = number / out;
    }
    return(resultado);
} 
void convertToDecimalOfBCD(int number) {
    printf("BCD:");
    while (number != 0)
    {
        int residuo = number % 10;
        switch (residuo)
        {
        case 0:
            printf(" 0000");
            break;
        case 1:
            printf(" 0001");
            break;
        case 2:
            printf(" 0010");
            break;
        case 3:
            printf(" 0011");
            break;
        case 4:
            printf(" 0100");
            break;
        case 5:
            printf(" 0101");
            break;
        case 6:
            printf(" 0110");
            break;
        case 7:
            printf(" 0111");
            break;
        case 8:
            printf(" 1000");
            break;
        case 9:
            printf(" 1001");
            break;
        default:
            break;
        }
        number = number / 10;
    }
    printf("\n");
    
}
unsigned long long convertToDecimalOfHexa(char *number){
    unsigned long long result = 0;
    unsigned long long elevado = 0;
    int x = 0,exp = 0;
    while (number[x] != '\0') {
        x++;
    }
    for (int i = x - 1;i >= 0;i--) {
        if (isdigit((int)number[i])) {
            elevado = (number[i] - '0') * pow(16,exp);
            result+= elevado;
        } else {
            switch (number[i])
            {
            case 'A':
                elevado = 10 * pow(16,exp);
                result+= elevado;
                break;
            case 'B':
                elevado = 11 * pow(16,exp);
                result+= elevado;
                break;
            case 'C':
                elevado = 12 * pow(16,exp);
                result+= elevado;
                break;
            case 'D':
                elevado = 13 * pow(16,exp);
                result+= elevado;
                break;
            case 'E':
                elevado = 14 * pow(16,exp);
                result+= elevado;
                break;
            case 'F':
                elevado = 15 * pow(16,exp);
                result+= elevado;
                break;
            default:
                printf("Algo pasa");
                break;
            }
        }
        exp++;
    }
    return result;
}
void convertToHexaOfDecimal(int number){
    int result = 0,x = 0,exp = 0;
    char hexa[30];
    int resultado = 0;
    for (int i = 0; number != 0; i++) 
    {
        if (number % 16 > 9) {
            switch (number % 16)
            {
            case 10:
                hexa[i] = 'A';
                break;
            case 11:
                hexa[i] = 'B';
                break;
            case 12:
                hexa[i] = 'C';
                break;
            case 13:
                hexa[i] = 'D';
                break;
            case 14:
                hexa[i] = 'E';
                break;
            case 15:
                hexa[i] = 'F';
                break;
            default:
                break;
            }
        } else {
            hexa[i] = (number % 16) + '0';
        }
        number = number / 16;
    }
    while (hexa[x] != '\0') {
        x++;
    }
    printf("Hexadecimal: ");
    for (int i = x - 1;i >= 0;i--) {
        printf("%c", hexa[i]);    
    }
    printf("\n");
}
int main(int argc) {
    char continueProgram;
    char hexadecimal[30];
    while (continueProgram != 'N')
    {
        int number;
        char oh[50],optionIn,optionOut;
        printf("What type of number are you going to enter?\n");
        printf("a) Decimal | b) Binary | c) Hexadecimal | d) Octal ");
        scanf("%s",&optionIn);
        switch (optionIn)
        {
        case 'a':
            printf("Writing the number in decimal\n");
            scanf("%d",&number);
            printf("Decimal: %d\n",number);
            printf("Binario :%d\n",convertNumbers(number,10,2));
            convertToHexaOfDecimal(number);
            printf("Octal: %d\n",convertNumbers(number,10,8));
            convertToDecimalOfBCD(number);
            break;
        case 'b':
            printf("Writing the number in binary\n");
            scanf("%d",&number);
            printf("Binario: %d\n",number);
            printf("Decimal: %d\n",convertNumbers(number,2,10));
            convertToHexaOfDecimal(convertNumbers(number,2,10));
            printf("Octal: %d\n",convertNumbers(convertNumbers(number,2,10),10,8));
            convertToDecimalOfBCD(convertNumbers(number,2,10));
            break;
        case 'c':
            printf("Writing the number in hexadecimal\n");
            scanf("%s",hexadecimal);
            printf("Hexadecimal: %s\n",hexadecimal);
            printf("Decimal: %llu\n",convertToDecimalOfHexa(hexadecimal));
            printf("Binario: %llu\n",convertNumbers(convertToDecimalOfHexa(hexadecimal),10,2));
            printf("Octal: %llu\n",convertNumbers(convertToDecimalOfHexa(hexadecimal),10,8));
            convertToDecimalOfBCD(convertToDecimalOfHexa(hexadecimal));
            break;
        case 'd':
            printf("Writing the number in octal\n");
            scanf("%d",&number);
            printf("Octal: %d\n",number);
            printf("Decimal: %d\n",convertNumbers(number,8,10));
            printf("Binario: %d\n",convertNumbers(convertNumbers(number,8,10),10,2));
            convertToHexaOfDecimal(convertNumbers(number,8,10));
            convertToDecimalOfBCD(convertNumbers(number,8,10));
            break;
        default:
            printf("Escribe una opcion correcta\n");
            break;
        }
        printf("Do you want continue? Y o N\n");
        scanf("%s",&continueProgram);
    }
    system("pause");
}
//CREATED BY JOSUE DANIEL GODINEZ MELECIO
