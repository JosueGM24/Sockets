#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

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

char* convertToHexaOfDecimal(double number) {
    int integerPart = (int)number;
    double fractionalPart = number - integerPart;
    static char hexa[60];  // Increased size to handle both parts together
    int index = 0;

    // Convert integer part to hexadecimal
    char intPartHexa[30];
    int intIndex = 0;
    do {
        int temp = integerPart % 16;
        intPartHexa[intIndex++] = (temp < 10) ? temp + '0' : temp - 10 + 'A';
        integerPart /= 16;
    } while (integerPart > 0);

    // Store integer part in reverse
    for (int i = intIndex - 1; i >= 0; i--) {
        hexa[index++] = intPartHexa[i];
    }
    hexa[index] = '\0';

    // Convert fractional part to hexadecimal
    if (fractionalPart > 0) {
        hexa[index++] = '.';
        for (int i = 0; i < 10 && fractionalPart > 0; i++) { // Limiting to 10 digits for simplicity
            fractionalPart *= 16;
            int temp = (int)fractionalPart;
            hexa[index++] = (temp < 10) ? temp + '0' : temp - 10 + 'A';
            fractionalPart -= temp;
        }
        hexa[index] = '\0';
    }

    return hexa;
}

double power(double base, int exponent) {
    double result = 1.0;
    for (int i = 0; i < exponent; i++) {
        result *= base;
    }
    return result;
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
        
        if (isDigit(expression[i]) || expression[i] == '.') {
            double operand = 0;
            int decimalPlace = -1;
            while (isDigit(expression[i]) || expression[i] == '.') {
                if (expression[i] == '.') {
                    decimalPlace = 1;
                } else {
                    if (decimalPlace > 0) {
                        operand += charToInt(expression[i]) / power(10, decimalPlace);
                        decimalPlace++;
                    } else {
                        operand = operand * 10 + charToInt(expression[i]);
                    }
                }
                i++;
            }
            operandTop++;
            operandStack[operandTop] = operand;
        } else if (expression[i] == '(') {
            operatorTop++;
            operatorStack[operatorTop] = '(';
            i++;
        } else if (expression[i] == ')') {
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
        } else {
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
        printf("Operacion---> %s  Resultado ----> %.2f\n", operacion, resultado);
        printf("Resultado en hexadecimal: %s\n", convertToHexaOfDecimal(resultado));
        
        operacion = va_arg(argumentos, const char*);
    }
    
    va_end(argumentos);
}

#define MCAST_GRP "224.1.1.1"
#define MCAST_PORT 5004

int main() {
    int sockfd;
    struct sockaddr_in addr;
    struct ip_mreq mreq;
    socklen_t addrlen = sizeof(addr);
    char buffer[10240];

    // Create a UDP socket
    sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sockfd < 0) {
        perror("socket creation failed");
        exit(1);
    }

    // Set reuse address option
    int reuse = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0) {
        perror("setsockopt failed");
        exit(1);
    }

    // Bind to INADDR_ANY to receive on all interfaces
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(MCAST_PORT);
    if (bind(sockfd, (struct sockaddr *)&addr, addrlen) < 0) {
        perror("bind failed");
        exit(1);
    }

    // Join the multicast group
    mreq.imr_multiaddr.s_addr = inet_addr(MCAST_GRP);
    mreq.imr_interface.s_addr = INADDR_ANY;
    if (setsockopt(sockfd, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq)) < 0) {
        perror("setsockopt failed");
        exit(1);
    }

    printf("Joined multicast group %s on port %d\n", MCAST_GRP, MCAST_PORT);
    operaciones("30.2*103.5", NULL);
    while (1) {
        printf("Waiting for data...\n");
        ssize_t bytes_received = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&addr, &addrlen);
        if (bytes_received < 0) {
            perror("recvfrom failed");
            exit(1);
        }

        printf("Data received\n");

        // Null-terminate the received data (assuming it's a string)
        buffer[bytes_received] = '\0';

        printf("Operation received: %s\n", buffer);
        operaciones(buffer, NULL);
    }

    close(sockfd);
    return 0;
}
