#include <iostream>
#include <cstring>
#include <vector>

using namespace std;

    char *strStr(char *haystack, char *needle) {
        if (!haystack || !needle) {
            return NULL;
        }
        int k = strlen(needle);
        if (!k) {
            return haystack;
        }
        
        vector<int> K(k);
        K[0] = -1;
        for (int i = 1; i < k; ++i) {
            int j;
            for (j = K[i - 1]; j + 1 >= 0 && needle[j + 1] != needle[i]; j = j > 0 ? K[j] : -2);
            K[i] = j + 1;
        }
        for (auto t: K) {
          cout << t << " ";
        }
        cout << endl;
        int j = 0;
        for (char *s = haystack; *s; ++s) {
            while (*s != needle[j]) {
                if (j > 0)
                    j = K[j - 1] + 1;
                else
                    break;
            }
            if (j >= 0 && *s == needle[j]) {
                if (++j == k) {
                    return s - k + 1;
                }
            } else {
              j = 0;
            }
        }
        return NULL;
    }

int main() {
  char *s = strStr("mississippi", "issi");
  if (!s) {
    cout << "NULL" << endl;
  } else {
    cout << s << endl;
  }
  return 0;
}
