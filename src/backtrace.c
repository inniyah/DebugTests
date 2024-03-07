// compile with -g -rdynamic compiler option to load the symbols
// gcc -o backtrace src/backtrace.c -g -rdynamic

#include <stdio.h>
#include <execinfo.h>
#include <stdlib.h>

void handler(char *caller) {
    void *array[10];
    size_t size;
    printf("Stack Trace Start for %s\n",caller);
    size = backtrace(array, 10);
    backtrace_symbols_fd(array, size, 2);
    printf("Stack Trace End\n");
}

void car() {
    handler("car()");
    printf("Continue Execution\n");
}
void baz() {car(); }

void bar() { baz(); }
void foo() { bar(); }


int main(int argc, char **argv) {
    foo();
}
