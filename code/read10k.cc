#include <cstring>
#include <algorithm>

using namespace std;

int read10k(char* buffer);

const int TEN_K = 10 * 1024;

void copy(char*& src, int srcLen, char*& dst, int dstLen) {
  int s = min(srcLen, dstLen);
  if (s > 0) {
    memcpy(dst, src, s);
    src += s;
    dst += s;
  }
}

int read(char* buf, int size) {
  static char intBuf[TEN_K], *src = intBuf, *srcEnd = intBuf;
  char *dst = buf, *dstEnd = dst + size;

  copy(src, srcEnd - src, dst, dstEnd - dst);
  bool eof = false;
  while (dstEnd - dst >= TEN_K && !eof) {
    int r = read10k(dst);
    dst += r;
    eof = r < TEN_K;
  }
  if (dstEnd > dst && !eof) {
    srcEnd = intBuf + read10k(src = intBuf);
    copy(src, srcEnd - src, dst, dstEnd - dst);
  }
  return dst - buf;
}
