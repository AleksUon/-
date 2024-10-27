#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <string>
#include <cmath>

using namespace std;

// Узел дерева Хаффмана
struct Node {
    char ch;
    int freq;
    Node* left;
    Node* right;

    // Конструктор для листовых узлов
    Node(char c, int f) : ch(c), freq(f), left(nullptr), right(nullptr) {}

    // Конструктор для внутренних узлов
    Node(char c, int f, Node* l, Node* r) : ch(c), freq(f), left(l), right(r) {}
};

// Компаратор для приоритетной очереди
struct Compare {
    bool operator()(Node* l, Node* r) {
        return l->freq > r->freq;
    }
};

// Построение кодов Хаффмана
void buildHuffmanCodes(Node* root, unordered_map<char, string>& huffmanCode, string str) {
    if (!root) return;

    // Если это лист
    if (!root->left && !root->right) {
        huffmanCode[root->ch] = str;
    }

    buildHuffmanCodes(root->left, huffmanCode, str + "0");
    buildHuffmanCodes(root->right, huffmanCode, str + "1");
}

// Удаление дерева Хаффмана
void deleteTree(Node* root) {
    if (!root) return;
    deleteTree(root->left);
    deleteTree(root->right);
    delete root;
}

// Кодирование строки
void huffmanCoding(const string& text) {
    // Подсчет частот символов
    unordered_map<char, int> freq;
    for (char ch : text) {
        freq[ch]++;
    }

    // Подсчет вероятностей символов
    int totalCharacters = text.length();
    unordered_map<char, double> probabilities;
    for (auto pair : freq) {
        probabilities[pair.first] = (double)pair.second / totalCharacters;
    }

    // Вывод таблицы частот и вероятностей
    cout << "Частота и вероятность встречаемости символов:\n";
    for (auto pair : freq) {
        cout << pair.first << ": частота = " << pair.second << ", вероятность = " << probabilities[pair.first] << "\n";
    }

    // Построение дерева
    priority_queue<Node*, vector<Node*>, Compare> pq;

    for (auto pair : freq) {
        pq.push(new Node(pair.first, pair.second));
    }

    while (pq.size() != 1) {
        Node* left = pq.top(); pq.pop();
        Node* right = pq.top(); pq.pop();

        int sum = left->freq + right->freq;
        pq.push(new Node('\0', sum, left, right));
    }

    Node* root = pq.top();

    // Построение кодов
    unordered_map<char, string> huffmanCode;
    buildHuffmanCodes(root, huffmanCode, "");

    // Вывод кодов
    cout << "\nКоды Хаффмана для символов:\n";
    for (auto pair : huffmanCode) {
        cout << pair.first << ": " << pair.second << "\n";
    }

    // Кодирование строки
    string encodedString = "";
    for (char ch : text) {
        encodedString += huffmanCode[ch];
    }

    cout << "\nЗакодированная строка: " << encodedString << "\n";

    // Расчет коэффициентов сжатия
    int originalSize = text.length() * 8; // исходная строка в битах (8 бит на символ в ASCII)
    int compressedSize = encodedString.length(); // сжатая строка в битах
    double compressionRatioASCII = (double)compressedSize / originalSize;

    int uniformCodeSize = ceil(log2(freq.size())); // биты на символ для равномерного кода
    int totalUniformSize = uniformCodeSize * text.length(); // исходный размер в равномерном коде
    double compressionRatioUniform = (double)compressedSize / totalUniformSize;

    cout << "\nИсходный размер (ASCII): " << originalSize << " бит\n";
    cout << "Сжатый размер: " << compressedSize << " бит\n";
    cout << "Коэффициент сжатия относительно ASCII: " << compressionRatioASCII * 100 << "%\n";

    cout << "\nРазмер равномерного кода: " << totalUniformSize << " бит\n";
    cout << "Коэффициент сжатия относительно равномерного кода: " << compressionRatioUniform * 100 << "%\n";

    // Расчет средней длины кода
    double averageLength = 0;
    for (auto pair : probabilities) {
        averageLength += pair.second * huffmanCode[pair.first].length();
    }
    cout << "\nСредняя длина кода: " << averageLength << "\n";

    // Расчет дисперсии длины кода
    double variance = 0;
    for (auto pair : probabilities) {
        double diff = huffmanCode[pair.first].length() - averageLength;
        variance += pair.second * diff * diff;
    }
    cout << "Дисперсия длины кода: " << variance << "\n";

    // Освобождение памяти
    deleteTree(root);
}

int main() {
    // Чтение строки из файла
    ifstream inputFile("input.txt");
    if (!inputFile.is_open()) {
        cerr << "Не удалось открыть файл!" << endl;
        return 1;
    }

    string text;
    getline(inputFile, text); // Чтение строки из файла
    inputFile.close();

    cout << "Исходный текст: " << text << endl;
    huffmanCoding(text);
    return 0;
}
