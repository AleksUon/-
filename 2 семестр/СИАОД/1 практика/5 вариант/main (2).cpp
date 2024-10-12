#include <iostream>
#include <random>

using namespace std;

void delOtherMethod(int array[], int& n, int key)
{
    int j = 0;
    int count = 0;
    for (int i = 0; i < n; i++)
    {
        array[j] = array[i];
            
        if (array[i] != key)
        {
            j++;
            count++;
        }
    }
    
    n = j;
    count++;
    cout << "Операций: " << count << endl;
}


/*Главная функция программы*/
int main()
{
    setlocale(LC_ALL, "RUS");
    int n = 100; //размер
    int key = 0; //что убрать
    cout << "Введите число, которое нужно удалить: ";
    cin >> key;

    cout << "Исходный массив: ";
    int* array = new int[n]; // Массив
    mt19937 gen(random_device{}());
    uniform_int_distribution<int> dist(1, 10);
    for (int j = 0; j < n; j++)
    {
        array[j] = dist(gen); // Заполнение массива случайными значениями от 1 до 10
        cout << array[j] << " ";
    }

    cout << endl;
    delFirstMethod(array, n, key);

    cout << "Изменённый массив: ";
    for (int i = 0; i < n; i++)
    {
        cout << array[i] << " ";
    }
    cout << endl;
    //размер конечного массива
    cout << "n = " << n << endl;

    return 0;
}
