// compile with -finstrument-functions and link with -ldl -rdynamic
// gcc -o instrument src/instrument.c -finstrument-functions -ldl -rdynamic

// See: https://github.com/bartman/snippets/tree/master/gcc-instrument-functions

#include <stdio.h>
#include <stdlib.h>

__attribute__((no_instrument_function))
void __cyg_profile_func_enter (void *this_fn, void *call_site) {
    printf(">>\n");
}
__attribute__((no_instrument_function))
void __cyg_profile_func_exit  (void *this_fn, void *call_site) {
    printf("<<\n");
}

void bar(void) {
    printf("bar\n");
}

void foo(void) {
    printf("foo\n");
}

int main(int argc, char **argv) {
    foo();
    bar();
    return 0;
}
