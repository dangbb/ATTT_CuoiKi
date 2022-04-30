#include <bits/stdc++.h>
#define maxn 100005

using namespace std;

class Shift
{
    public:
        int key;

        string encode(string s)
        {
            string news = "";

            for (auto c: s)
            {
                news += char((int(c - 'A') + 26 + key) % 26 + int('A'));
            }

            return news;
        };

        string decode(string s)
        {
            string news = "";

            for (auto c: s)
            {
                news += char((int(c - 'A') + 26 - key) % 26 + int('A'));
            }

            return news;
        };

        static void analysis(string s)
        {
            for (int i=0;i<=25;i++)
            {
                string news = "";

                for (auto c: s)
                {
                    news += char((int(c - 'A') + 26 - i) % 26 + int('A'));
                }

                cout << "Check key " << i << endl;
                cout << news << endl;
            }
        };
};

int main()
{
    freopen("a.inp","r",stdin);

    string str;

    Shift cipher = Shift();
    cin >> cipher.key;
    cin >> str;

    cout << cipher.encode(str) << endl;
    string ciphertext = cipher.encode(str);

    cout << cipher.decode(ciphertext) << endl;
    Shift::analysis(ciphertext);
}
