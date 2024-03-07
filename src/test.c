#include <stdio.h>

struct foo {
    int a;
    struct foo * next;
};

int fib(int a, struct foo *b) {
    if (a <= 1) return 1;
    printf("%d\n", a);
    return fib(a-1, 0)+fib(a-2, 0);
}

int main(int argc, char **argv) {
    struct foo b = {23, 0};
    return fib(5, &b);
}
