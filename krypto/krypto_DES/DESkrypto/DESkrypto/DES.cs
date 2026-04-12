using System;
using System.Collections.Generic;
using System.Text;

namespace DESkrypto
{
    class DES
    {
        /*Przygotowanie głównego klucza, zmniejsza rozmiar z 64 bitów na 56
         * (odrzuca najmniej ważny bit - bity parzystości) i miesza pozostałe bity, wynik będzie dalej
         używany do generowania 16 podkluczy*/
        private byte[] roundkey = new byte[]{
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4};

        /*Określa o ile pozycji będzie rotacja w każdej z 16 rund, po rundkey
         56bity/2 i obie połówki przesuwane w lewo o określoną liczbę miejsc*/
        private byte[] rotation = new byte[]
            {1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};

        /*Kompresujemy do 48 bitów, pomijając część bitów*/
        private byte[] compression_pbox = new byte[]{
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32};

        /*szyfrując bity tekstu jawnego, permutujemy je na odpowiednie miejsca
         nie ma to żadnego celu kryptograficznego, zabieg historyczny*/
        private byte[] IP = new byte[]{
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7};

        /*Blok ma 64 bity, z czego mieszana jest połowa, klucz ma 48 bitów i 
         żeby zrobić operację XOR potrzebujemy tyle samo bitów więc rozszerzamy z
        32 bitów na 48 na otrzymanych bitach dokonuje się operację XOR odpowiadającym
        bitom podklucza*/
        private byte[] expansion_permutation = new byte[]{
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1};

        /*Otrzymane bity dzielimy na 8 grup po 6 bitów, na wyjściu 4 bity, całość 32 bity*/
        private byte[][] SBox = new byte[][] {
        new byte[] {
            14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
            0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
            4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
            15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 },
        new byte[] {
            15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
            3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
            0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
            13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 },
        new byte[] {
            10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
            13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
            13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
            1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 },
        new byte[] {
            7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
            13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
            10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
            3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14 },
        new byte[] {
            2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
            14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
            4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
            11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 },
        new byte[] {
            12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
            10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
            9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
            4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13 },
        new byte[] {
            4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
            13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
            1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
            6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12 },
        new byte[] {
            13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
            1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
            7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
            2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11 }
    };

        /*Jest używana 16 razy – wewnątrz każdej pojedynczej rundy szyfrowania
         Otrzymuje 32 bity wychodzące z S-Boxów i po prostu zamienia je miejscami. 
        Dzięki temu, w kolejnej rundzie te przemieszane bity trafią do zupełnie innych
        S-Boxów, co zapewnia tzw. efekt lawinowy*/
        private byte[] pbox_permutation = new byte[]{
        16, 7, 20, 21,
        29, 12, 28, 17,
        1, 15, 23, 26,
        5, 18, 31, 10,
        2, 8, 24, 14,
        32, 27, 3, 9,
        19, 13, 30, 6,
        22, 11, 4, 25};

        /*Ostatnia permutacja, odwrotna do IP, jest stosowana do uzyskania ostatecznego szyfrogramu z otrzymanych bitów po 16 rundach*/
        private byte[] IP_reverse = new byte[]{
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25};

        private byte[] ByteToBit(byte[] input)
        {
            byte[] output = new byte[input.Length * 8]; //Wiadomość --> UTF8 - od 0 do 255, czyli 8 bitów na znak
            for (int i = 0; i < input.Length; i++)
            {
                int number = input[i]; //int bo dzielenie
                for (int j = 7; j >= 0; j--)
                {
                    output[i * 8 + j] = (byte)(number % 2);
                    number = number / 2;
                }
            }
            return output;
        }

        //Zamieniamy bity z powrotem na bajty, dzieląc je na grupy po 8, obliczając wartość po zaszyfrowaniu
        private byte[] BitsToBytes(byte[] input)
        {
            byte[] output = new byte[input.Length / 8];
            for (int i = 0; i < output.Length; i++)
            {
                int number = 0;
                for (int j = 0; j < 8; j++)
                {
                    number = (number << 1) + input[i * 8 + j];
                }
                output[i] = (byte)number;
            }
            return output;
        }

        private byte[] XOR(byte[] a, byte[] b) //0 jeśli bity są takie same, 1 jeśli różne
        {
            byte[] wynik = new byte[a.Length];

            for (int i = 0; i < wynik.Length; i++)
            {
                if (a[i] == b[i])
                {
                    wynik[i] = 0;
                }
                else
                {
                    wynik[i] = 1;
                }
            }
            return wynik;
        }
        //git
        private byte[] Permutate(byte[] input, byte[] table) //Zamienia bity według określonego wzoru w tabeli
        {
            byte[] output = new byte[table.Length];
            for (int i = 0; i < table.Length; i++)
            {
                output[i] = input[table[i] - 1];
            }
            return output;

        }
        //git
        // Przesuwa bity w lewo o określoną liczbę miejsc, używane do generowania podkluczy
        private byte[] LeftShift(byte[] input, byte shifts)
        {
            byte[] output = new byte[input.Length];
            for (int i = 0; i < input.Length; i++)
            {
                byte newIndex = (byte)((i + shifts) % input.Length);
                output[i] = input[newIndex];
            }
            return output;
        }

        //Wykorzystywany przy generowaniu podkluczy oraz po 16 rundach szyfrowania, łączy dwie połowy bitów w jedną całość
        private byte[] ConnectTables(byte[] left, byte[] right)
        {
            byte[] output = new byte[left.Length + right.Length];
            for (int i = 0; i < left.Length; i++)
            {
                output[i] = left[i];
            }
            for (int i = 0; i < right.Length; i++)
            {
                output[left.Length + i] = right[i];
            }
            return output;
        }

        //Dzieli blok na dwa fragmenty, używane przy rundach oraz generowaniu podkluczy
        //zwraca tablicę z dwoma elementami, gdzie każdy element to jedna połowa bitów
        // byte[][] polowki = DivideFragments(blok);
        // byte[] lewa = polowki[0];
        // byte[] prawa = polowki[1];
        private byte[][] DivideFragments(byte[] input)
        {
            int fragmentSize = input.Length / 2;
            byte[] left = new byte[fragmentSize];
            byte[] right = new byte[fragmentSize];

            for (int i = 0; i < fragmentSize; i++)
            {
                left[i] = input[i];
                right[i] = input[i + fragmentSize];
            }
            return new byte[][] { left, right };
        }

        private byte[][] Generate16Keys(byte[] mainKey64bits)
        {
            byte[][] subkeys = new byte[16][];
            byte[] key56bits = Permutate(mainKey64bits, roundkey); //Zmniejszamy rozmiar klucza z 64 bitów do 56

            byte[][] halves = DivideFragments(key56bits); //Dzielimy klucz na dwie połowy
            byte[] left = halves[0];
            byte[] right = halves[1];
            for (int i = 0; i < 16; i++)
            {
                left = LeftShift(left, rotation[i]); //Rotacja w lewo o określoną liczbę miejsc
                right = LeftShift(right, rotation[i]); //To samo dla prawej połowy
                byte[] combinedKey = ConnectTables(left, right); //Łączymy obie połowy
                subkeys[i] = Permutate(combinedKey, compression_pbox); //Kompresujemy do 48 bitów, pomijając część bitów
            }
            return subkeys;
        }

        // Zamienia dowolną tablicę bitów na jedną liczbę dziesiętną, używana do obliczania wiersza i kolumny w S-Boxach
        private int BitToInt(byte[] input)
        {
            int result = 0;
            for (int i = 0; i < input.Length; i++)
            {
                result = (result << 1) + input[i];
            }
            return result;
        }

        // Zamienia liczbę z S-Boxa (0-15) na tablicę dokładnie 4 bitów, używana do zamiany wyniku z S-Boxów na bity, które będą dalej permutowane
        private byte[] IntToBit(int integerNum)
        {
            byte[] bity = new byte[4];
            for (int i = 3; i >= 0; i--) // po Sbox mamy 4 bity, więc iterujemy od 3 do 0
            {
                bity[i] = (byte)(integerNum % 2);
                integerNum /= 2;
            }
            return bity;
        }

        //Funkcja działa wewnątrz każdej z 16 rund szyfrowania, otrzymuje 32 bity i 48 bitów podklucza,
        ///wykonuje operację XOR, dzieli wynik na 8 grup po 6 bitów, zamienia je na 4 bity za pomocą S- Boxów
        ///a następnie permutuje otrzymane 32 bity
        private byte[] FunctionInRounds(byte[] right32bit, byte[] roundKey48bit)
        {
            byte[] expandedRight = Permutate(right32bit, expansion_permutation); //Rozszerzamy z 32 bitów na 48
            byte[] afterXOR = XOR(expandedRight, roundKey48bit); //Operacja XOR z podkluczem
            byte[] output = new byte[32];
            for (int i = 0; i < 8; i++)
            {
                byte[] sixBits = new byte[6];
                for (int j = 0; j < 6; j++)
                {
                    sixBits[j] = afterXOR[i * 6 + j];
                }
                int row = BitToInt(new byte[] { sixBits[0], sixBits[5] });
                int col = BitToInt(new byte[] { sixBits[1], sixBits[2], sixBits[3], sixBits[4] });
                int sBoxValue = SBox[i][row * 16 + col];
                byte[] fourBits = IntToBit(sBoxValue);
                for (int j = 0; j < 4; j++)
                {
                    output[i * 4 + j] = fourBits[j];
                }
            }
            return Permutate(output, pbox_permutation);
        }

        private byte[] ProcessBlock(byte[] block64bit, byte[][] subkeys, bool encrypt)
        {
            byte[] bits = Permutate(block64bit, IP);

            byte[][] halves = DivideFragments(bits);
            byte[] left = halves[0];
            byte[] right = halves[1];

            for (int i = 0; i < 16; i++)
            {
                byte[] tempRight = right;

                byte[] currentKey = encrypt ? subkeys[i] : subkeys[15 - i];

                right = XOR(left, FunctionInRounds(right, currentKey));

                left = tempRight;
            }
            byte[] combined = ConnectTables(right, left);

            return Permutate(combined, IP_reverse);
        }

        public byte[] Encrypt(byte[] data, byte[] key)
        {
            byte[][] subkeys = Generate16Keys(ByteToBit(key));

            // Obliczamy padding zgodnie z PKCS7
            // Jeśli data.Length = 8, to 8 - (8 % 8) = 8 (dodajemy cały blok)
            // Jeśli data.Length = 7, to 8 - (7 % 8) = 1 (dodajemy jeden bajt o wartości 1)
            int paddingLength = 8 - (data.Length % 8);
            byte[] paddedData = new byte[data.Length + paddingLength];
            Array.Copy(data, paddedData, data.Length);

            // Wypełniamy końcówkę wartością paddingu
            for (int i = data.Length; i < paddedData.Length; i++)
            {
                paddedData[i] = (byte)paddingLength;
            }

            byte[] result = new byte[paddedData.Length];

            //Szyfrowanie
            for (int i = 0; i < paddedData.Length; i += 8)
            {
                byte[] block = new byte[8];
                Array.Copy(paddedData, i, block, 0, 8);

                // Konwersja na bity -> Szyfrowanie -> Konwersja na bajty
                byte[] encryptedBlockBits = ProcessBlock(ByteToBit(block), subkeys, true);
                byte[] encryptedBlockBytes = BitsToBytes(encryptedBlockBits);

                Array.Copy(encryptedBlockBytes, 0, result, i, 8);
            }

            return result;
        }

        public byte[] Decrypt(byte[] encryptedData, byte[] key)
        {
            byte[][] subkeys = Generate16Keys(ByteToBit(key));
            byte[] resultWithPadding = new byte[encryptedData.Length];

            for (int i = 0; i < encryptedData.Length; i += 8)
            {
                byte[] block = new byte[8];
                Array.Copy(encryptedData, i, block, 0, 8);

                byte[] decryptedBlockBits = ProcessBlock(ByteToBit(block), subkeys, false);
                byte[] decryptedBlockBytes = BitsToBytes(decryptedBlockBits);

                Array.Copy(decryptedBlockBytes, 0, resultWithPadding, i, 8);
            }

            int paddingLength = resultWithPadding[resultWithPadding.Length - 1];
            if (paddingLength < 1 || paddingLength > 8) return resultWithPadding;

            byte[] finalResult = new byte[resultWithPadding.Length - paddingLength];
            Array.Copy(resultWithPadding, finalResult, finalResult.Length);

            return finalResult;
        }
    }
}
