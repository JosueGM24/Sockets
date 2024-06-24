
clear;

function hexString = decimalToHexadecimal(decimalNumber)
  % Función que convierte un número decimal a hexadecimal, incluyendo la parte fraccionaria

  if decimalNumber < 0
    error('El número debe ser positivo');
  end

  % Separar la parte entera y la parte fraccionaria del número decimal
  integerPart = floor(decimalNumber);
  fractionalPart = decimalNumber - integerPart;

  % Convertir la parte entera a hexadecimal
  hexIntegerPart = dec2hex(integerPart);

  % Convertir la parte fraccionaria a hexadecimal
  hexFractionalPart = '';
  maxPrecision = 16; % número máximo de dígitos hexadecimales después del punto decimal

  while fractionalPart > 0 && length(hexFractionalPart) < maxPrecision
    fractionalPart = fractionalPart * 16;
    hexDigit = floor(fractionalPart);
    hexFractionalPart = [hexFractionalPart, dec2hex(hexDigit)];
    fractionalPart = fractionalPart - hexDigit;
  end

  if isempty(hexFractionalPart)
    hexString = hexIntegerPart;
  else
    hexString = [hexIntegerPart, '.', hexFractionalPart];
  end
end
decimalToHexadecimal(56.8);
