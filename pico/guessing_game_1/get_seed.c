#include <stdio.h>
#include <stdlib.h>

#define BUFSIZE 100

long increment(long in) {
	return in + 1;
}

long get_random() {
	return rand() % BUFSIZE;
}

int do_stuff() {
	long ans = get_random();
	ans = increment(ans);
    return ans;
}

int main(int argc, char *argv[])
{
  printf("sayi: %d\n", do_stuff());
  printf("sayi: %d\n", do_stuff());
  printf("sayi: %d\n", do_stuff());
  printf("sayi: %d\n", do_stuff());
  printf("sayi: %d\n", do_stuff());
  return 0;
}
