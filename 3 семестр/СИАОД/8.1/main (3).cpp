#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <algorithm>
#include <fstream>

using namespace std;

// Структура для хранения символа и его частоты
struct Symbol {
    char ch;
    int freq;
    string code;
};

// Сравнение для сортировки по частоте
bool compareFreq(const Symbol &a, const Symbol &b) {
    return a.freq > b.freq;
}

// Функция рекурсивного кодирования
void shannonFanoCoding(vector<Symbol>& symbols, int start, int end) {
    if (start >= end)
        return;

    // Находим середину для разделения на 2 группы
    int total_freq = 0;
    for (int i = start; i <= end; ++i)
        total_freq += symbols[i].freq;

    int half_freq = 0;
    int mid = start;
    for (int i = start; i <= end; ++i) {
        half_freq += symbols[i].freq;
        if (half_freq >= total_freq / 2) {
            mid = i;
            break;
        }
    }

    // Присваиваем код "0" левой части и "1" правой части
    for (int i = start; i <= mid; ++i)
        symbols[i].code += "0";
    for (int i = mid + 1; i <= end; ++i)
        symbols[i].code += "1";

    // Рекурсивно кодируем обе части
    shannonFanoCoding(symbols, start, mid);
    shannonFanoCoding(symbols, mid + 1, end);
}

// Функция для сжатия текста
string compress(const string& text, map<char, string>& encodingTable) {
    string compressed = "";
    for (char ch : text) {
        compressed += encodingTable[ch];
    }
    return compressed;
}

// Функция для декодирования сжатого текста
string decompress(const string& compressed, const map<string, char>& decodingTable) {
    string decoded = "";
    string buffer = "";
    for (char bit : compressed) {
        buffer += bit;
        if (decodingTable.find(buffer) != decodingTable.end()) {
            decoded += decodingTable.at(buffer);
            buffer = "";
        }
    }
    return decoded;
}

// Функция для вычисления процента сжатия
double compressionRate(const string& original, const string& compressed) {
    return 100.0 * (1.0 - (double(compressed.size()) / (original.size() * 8)));
}

int main() {
    // Открытие исходного текстового файла
    ifstream inputFile("input.txt");
    string text((istreambuf_iterator<char>(inputFile)), istreambuf_iterator<char>());
    inputFile.close();

    // Подсчёт частоты символов
    map<char, int> freqMap;
    for (char ch : text) {
        freqMap[ch]++;
    }

    // Заполнение вектора символов
    vector<Symbol> symbols;
    for (auto& pair : freqMap) {
        symbols.push_back({pair.first, pair.second, ""});
    }

    // Сортировка символов по частоте
    sort(symbols.begin(), symbols.end(), compareFreq);

    // Выполнение кодирования Шеннона-Фано
    shannonFanoCoding(symbols, 0, symbols.size() - 1);

    // Построение таблиц кодирования и декодирования
    map<char, string> encodingTable;
    map<string, char> decodingTable;
    for (Symbol& sym : symbols) {
        encodingTable[sym.ch] = sym.code;
        decodingTable[sym.code] = sym.ch;
        cout << "Символ: " << sym.ch 
             << " встречается " << sym.freq << " раз, закодировано как " 
             << sym.code << ", количество битов: " << sym.code.length() << endl;
    }

    // Сжатие текста
    string compressedText = compress(text, encodingTable);
    ofstream compressedFile("compressed.txt");
    compressedFile << compressedText;
    compressedFile.close();

    // Декодирование сжатого текста
    string decompressedText = decompress(compressedText, decodingTable);
    ofstream outputFile("decompressed.txt");
    outputFile << decompressedText;
    outputFile.close();

    // Вычисление процента сжатия
    double compressionPercentage = compressionRate(text, compressedText);
    cout << "Процент сжатия: " << compressionPercentage << "%" << endl;
    cout << "ы я т к м л ш з р п ё н е б й В у " << endl;

    return 0;
}
