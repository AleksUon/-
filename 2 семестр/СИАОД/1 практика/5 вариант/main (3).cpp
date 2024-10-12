#include <iostream>

using namespace std;

#define M 4
#define N 4 

void spiral(int matrix[M][N])
{
    int t = 0, b = M - 1, l = 0, r = N - 1, p = 0;
    
    while (t <= b && l <= r)
    {
        for (int i = l; i <= r; i++)
        {
            p++;
            cout << matrix [t][i] << " ";
        }
        t++;
        p++;
        
        for (int i = t; i <= b; i++)
        {
           p++;
           cout << matrix [i][r] << " "; 
        }
        r--;
        p++;
        
        if (t <= b)
        {
            for (int i = r; i >= l; i--)
            {
                p++;
                cout << matrix[b][i] << " ";
            }
            b--;
            p++;
        }
        p++;
        
        if (l <= r)
        {
            for (int i = b; i >= t; i--)
            {
                p++;
                cout << matrix[i][l] << " ";
            }
            l++;
            p++;
        }
        p++;
    }
    p++;
    cout <<"Операций: " << p << endl;
}

int main()
{
    setlocale(LC_ALL, "RUS");
    int matrix[M][N] = { {8, 6, 3, 1},
                         {48, -5, 7, 3},
                         {9, 1, 2, 63},
                         {13, 21, 72, 12} };
                         
    cout << "Обход матрицы по спирали (по часовой стрелке): " << endl;
    spiral(matrix);
    
    return 0;
}