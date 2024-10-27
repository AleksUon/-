#include <iostream>
#include <string>
#include <vector>
#include <map>

using namespace std;

// Структура для хранения кодов
struct Code {
    int index;
    char symbol;
};

// Функция для сжатия строки с помощью алгоритма LZ78
vector<Code> LZ78Compress(const string &input) {
    map<string, int> dictionary; // Словарь
    vector<Code> codes; // Вектор для хранения кодов
    string current; // Текущая последовательность

    for (char ch : input) {
        current += ch; // Добавляем символ к текущей последовательности

        // Проверяем, существует ли текущая последовательность в словаре
        if (dictionary.find(current) == dictionary.end()) {
            // Находим индекс предыдущего элемента
            int index = (current.size() > 1) ? dictionary[current.substr(0, current.size() - 1)] : 0;

            // Добавляем код в вектор
            codes.push_back({index, ch});

            // Добавляем текущую последовательность в словарь
            dictionary[current] = dictionary.size() + 1; // Индексация с 1

            // Вывод информации о словаре и считываемом содержимом
            cout << "Словарь: ";
            for (const auto &entry : dictionary) {
                cout << entry.first << " = " << entry.second << " ";
            }
            cout << "\nСчитываемое содержимое: " << current << endl;

            // Вывод кода
            cout << "Код: <" << index << ", '" << ch << "'>" << endl << endl;

            current.clear(); // Очищаем текущую последовательность
        }
    }

    // Обработка оставшейся текущей последовательности, если она есть
    if (!current.empty()) {
        int index = dictionary[current.substr(0, current.size() - 1)];
        codes.push_back({index, current.back()});

        // Вывод информации о словаре и считываемом содержимом
        cout << "Словарь: ";
        for (const auto &entry : dictionary) {
            cout << entry.first << " = " << entry.second << " ";
        }
        cout << "\nСчитываемое содержимое: " << current << endl;

        // Вывод кода
        cout << "Код: <" << index << ", '" << current.back() << "'>" << endl << endl;
    }

    return codes;
}

// Функция для вывода результата сжатия
void printCompressionResult(const vector<Code> &codes) {
    cout << "\nНе Сжатый результат: ";
    for (const auto &code : codes) {
        cout << "(" << code.index << ", '" << code.symbol << "') ";
    }
    cout << endl;
}

// Функция для расчета процента сжатия
void printCompressionPercentage(const string &input, const vector<Code> &codes) {
    int originalSize = input.size(); // Размер исходной строки
    int compressedSize = codes.size(); // Количество кодов после сжатия

    double compressionPercentage = (1.0 - static_cast<double>(compressedSize) / originalSize) * 100;

    cout << "Оригинальный размер: " << originalSize << endl;
    cout << "Сжатый размер: " << compressedSize << endl;
    cout << "Процент сжатия: " << compressionPercentage << "%" << endl;
}

int main() {
    string input = "bigbonebigborebigbo";
    vector<Code> compressedCodes = LZ78Compress(input);

    // Выводим результат сжатия
    printCompressionResult(compressedCodes);
    printCompressionPercentage(input, compressedCodes);

    return 0;
}
