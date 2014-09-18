#include <string>
#include <iostream>
#include <stdexcept>
#include <cctype>

using namespace std;

string exp;
int p;
int indent;

double value() {
  int op = p;
  cout << string(indent++, ' ') << "value at " << p << endl;
  while (p < exp.size() && isspace(exp[p])) p++;
  double v = 0, e = 0;
  bool d = false;
  while (p < exp.size()) {
    char c = exp[p++];
    if (c == '.') {
      if (e) {
        throw runtime_error("second . in number");
      }
      e = .1;
    } else if (isdigit(c)) {
      d = true;
      if (e == 0) {
        v = v * 10 + (c - '0');
      } else {
        v += e * (c - '0');
        e /= 10;
      }
    } else {
      --p;
      break;
    }
  }
  if (!d) {
    throw runtime_error("expect number");
  }
  cout << string(--indent, ' ') << "value at " << op << " to " << p << ": " << v << endl;
  return v;
}

double expr();

double factor() {
  int op = p;
  cout << string(indent++, ' ') << "factor at " << p << endl;
  while (p < exp.size()) {
    char c = exp[p++];
    if (!isspace(c)) {
      if (isdigit(c) || c == '.' || c =='-') {
        if (c == '-') {
          double r = -value();
          cout << string(--indent, ' ') << "factor at " << op << " to " << p << ": " << r << endl;
          return r;
        } else {
          --p;
          double r = value();
          cout << string(--indent, ' ') << "factor at " << op << " to " << p << ": " << r << endl;
          return r;
        }
      } else if (c == '(') {
        double e = expr();
        while (p < exp.size()) {
          char c = exp[p++];
          if (!isspace(c)) {
            if (c == ')') {
              cout << string(--indent, ' ') << "factor at " << op << " to " << p << ": " << e << endl;
              return e;
            } else {
              throw runtime_error("expect )");
            }
          }
        }
        throw runtime_error("expect ), got eof");
      }
      throw runtime_error("expect number or (");
    }
  }
  throw runtime_error("expect number or (");
}

double term() {
  int op = p;
  cout << string(indent++, ' ') << "term at " << p << endl;
  double f = factor();
  while (p < exp.size()) {
    char c = exp[p++];
    if (!isspace(c)) {
      if (c == '*') {
        f *= factor();
      } else if (c == '/') {
        f /= factor();
      } else {
        --p;
        break;
      }
    }
  }
  cout << string(--indent, ' ') << "term at " << op << " to " << p <<": " << f << endl;
  return f;
}

double expr() {
  int op = p;
  cout << string(indent++, ' ') << "expr at " << p << endl;
  double t = term();
  while (p < exp.size()) {
    char c = exp[p++];
    if (!isspace(c)) {
      if (c == '+') {
        t += term();
      } else if (c == '-') {
        t -= term();
      } else {
        --p;
        break;
      }
    }
  }
  cout << string(--indent, ' ') << "expr at " << op << " to " << p << ": " << t << endl;
  return t;
}

int main(int argc, char **argv) {
  if (1 < argc) {
    exp = argv[1];
  } else {
    getline(cin, exp);
  }
  try {
    cout << expr() << endl;
  } catch(runtime_error& e) {
    cerr << "Line:" << exp << endl;
    cerr << "Error:" << e.what() << " at:" << p - 1 << endl;
  }

  return 0;
}
