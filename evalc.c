#include <stdio.h>
#include <stdarg.h>

int isDigit(char c) {
    return (c >= '0' && c <= '9');
}

int isSpace(char c) {
    return (c == ' ' || c == '\t' || c == '\n');
}

int charToInt(char c) {
    return c - '0';
}

int getPriority(char operator) {
    if (operator == '*' || operator == '/')
        return 2;
    else if (operator == '+' || operator == '-')
        return 1;
    else
        return 0;
}

double performOperation(double operand1, double operand2, char operator) {
    switch (operator) {
        case '*':
            return operand1 * operand2;
        case '/':
            return operand1 / operand2;
        case '+':
            return operand1 + operand2;
        case '-':
            return operand1 - operand2;
        default:
            printf("Error: Invalid operator\n");
            return 0;
    }
}

double evaluateExpression(const char* expression) {
    double operandStack[100];
    int operandTop = -1;
    
    char operatorStack[100];
    int operatorTop = -1;
    
    int i = 0;
    while (expression[i] != '\0') {
        if (isSpace(expression[i])) {
            i++;
            continue;
        }
        
        if (isDigit(expression[i])) {
            double operand = 0;
            while (isDigit(expression[i]) || expression[i] == '.') {
                if (expression[i] != '.') {
                    operand = operand * 10 + charToInt(expression[i]);
                }
                else {
                    double decimal = 0.1;
                    i++;
                    while (isDigit(expression[i])) {
                        operand = operand + charToInt(expression[i]) * decimal;
                        decimal *= 0.1;
                        i++;
                    }
                }
                i++;
            }
            operandTop++;
            operandStack[operandTop] = operand;
        }
        else if (expression[i] == '(') {
            operatorTop++;
            operatorStack[operatorTop] = '(';
            i++;
        }
        else if (expression[i] == ')') {
            while (operatorTop >= 0 && operatorStack[operatorTop] != '(') {
                double operand2 = operandStack[operandTop];
                operandTop--;
                double operand1 = operandStack[operandTop];
                operandTop--;
                char operator = operatorStack[operatorTop];
                operatorTop--;
                double result = performOperation(operand1, operand2, operator);
                operandTop++;
                operandStack[operandTop] = result;
            }
            if (operatorTop >= 0 && operatorStack[operatorTop] == '(') {
                operatorTop--;
            }
            i++;
        }
        else {
            while (operatorTop >= 0 && getPriority(operatorStack[operatorTop]) >= getPriority(expression[i])) {
                double operand2 = operandStack[operandTop];
                operandTop--;
                double operand1 = operandStack[operandTop];
                operandTop--;
                char operator = operatorStack[operatorTop];
                operatorTop--;
                double result = performOperation(operand1, operand2, operator);
                operandTop++;
                operandStack[operandTop] = result;
            }
            operatorTop++;
            operatorStack[operatorTop] = expression[i];
            i++;
        }
    }
    
    while (operatorTop >= 0) {
        double operand2 = operandStack[operandTop];
        operandTop--;
        double operand1 = operandStack[operandTop];
        operandTop--;
        char operator = operatorStack[operatorTop];
        operatorTop--;
        double result = performOperation(operand1, operand2, operator);
        operandTop++;
        operandStack[operandTop] = result;
    }
    
    return operandStack[operandTop];
}

void operaciones(const char* operacion, ...) {
    va_list argumentos;
    va_start(argumentos, operacion);
    
    while (operacion != NULL) {
        double resultado = evaluateExpression(operacion);
        printf("Operacion---> %s  Resulado ---->%.2f\n", operacion, resultado);
        
        operacion = va_arg(argumentos, const char*);
    }
    
    va_end(argumentos);
}

int main() {
    operaciones("3+5*2*2*3-9", "2*2-1/2","1*1/1-1/2+1/4", NULL);
    
    return 0;
}
