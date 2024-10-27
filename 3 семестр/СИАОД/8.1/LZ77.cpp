#include <iostream>
#include <string>
#include <string_view>
#include <forward_list>
#include <algorithm>

using namespace std;

struct CodeNode
{
    unsigned char beg;
    unsigned char len;
    char ch;
};

bool push_shift(string& s, char c, size_t len)  // возвращает true, если первый символ был удален
{
    if (s.size() < len) { s.push_back(c); return false; }
    move(next(s.begin()), s.end(), s.begin());
    s.back() = c; return true;
}

forward_list<CodeNode> LZ77(string_view s, size_t win_len = 255)
{
    forward_list<CodeNode> res; auto it = res.before_begin();
    string win, buf; win.reserve(win_len); buf.reserve(win_len);
    CodeNode next; size_t saved_win_len = 0;
    for (char c : s) {
        buf.push_back(c);
        size_t pos;
        next.ch = c;

        if ((pos = win.rfind(buf)) != string::npos) {
            next.beg = saved_win_len - pos; next.len = buf.size();
            if (push_shift(win, c, win_len)) saved_win_len--;  // сдвиг
        } else {
            it = res.insert_after(it, next); buf.resize(0);
            next.beg = 0; next.len = 0;
            push_shift(win, c, win_len);
            saved_win_len = win.size();
        }
    }
    if (next.len != 0) { next.len--; res.insert_after(it, next); }
    return res;
}

size_t LZ77length(const forward_list<CodeNode>& code) { // получение длины исходной строки
    size_t len = 0;
    for (const CodeNode& cn : code) len += cn.len + 1;
    return len;
}

size_t LZ77size(const forward_list<CodeNode>& code) {  // размер закодированных данных
    return sizeof(CodeNode) * distance(code.begin(), code.end());
}

string LZ77decode(const forward_list<CodeNode>& code)
{
    string res;
    res.reserve(LZ77length(code)); // не может быть
    for (CodeNode cn : code) {
        for (size_t i = res.size() - cn.beg, e = i + cn.len; i != e; ++i)
            res += res[i];
        res += cn.ch;
    }
    return res;
}

ostream& operator<<(ostream& os, CodeNode cn) {
    return os << '<' << int(cn.beg) << ',' << int(cn.len) << ',' << cn.ch << '>';
}

int main()
{
    // Ввод строки с клавиатуры
    cout << "Введите строку из символов '0' и '1': ";
    string s;
    getline(cin, s);

    // Сжатие строки
    auto code = LZ77(s, 10);

    // Подсчет количества LZ-кодов
    size_t code_count = distance(code.begin(), code.end());

    // Вывод кодов
    cout << "Сгенерированные LZ-коды:\n";
    for (CodeNode cn : code) cout << cn << ' ';
    cout << endl;

    // Вывод декодированной строки и исходной строки для сравнения
    cout << "\nДекодированная строка: " << LZ77decode(code) << '\n';
    cout << "Исходная строка: " << s << '\n';

    // Вычисление и вывод процента сжатия
    size_t original_size = s.size();
    size_t compressed_size = LZ77size(code);
    double compression_ratio = (1 - double(compressed_size) / original_size) * 100.0;

    cout << "\nРазмер исходной строки: " << original_size << " байт\n";
    cout << "Размер сжатой строки: " << compressed_size << " байт\n";
    cout << "Процент сжатия: " << compression_ratio << "%\n";
    cout << "Общее количество сгенерированных LZ-кодов: " << code_count << "\n";

    return 0;
}
