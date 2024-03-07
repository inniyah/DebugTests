// compile with -finstrument-functions and link with -ldl -rdynamic
// gcc -o instrument src/instrument.c -finstrument-functions -ldl -rdynamic

// See: https://github.com/bartman/snippets/tree/master/gcc-instrument-functions
// See: https://balau82.wordpress.com/2010/10/06/trace-and-profile-function-calls-with-gcc/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static FILE *fp_trace;

void __attribute__ ((constructor)) trace_begin(void) {
    fp_trace = fopen("trace.out", "w");
}

__attribute__((no_instrument_function))
void __cyg_profile_func_enter (void * func,  void * caller) {
    if(fp_trace != NULL) {
        fprintf(fp_trace, "e %p %p %lu\n", func, caller, time(NULL) );
    }
}

__attribute__((no_instrument_function))
void __cyg_profile_func_exit  (void * func,  void * caller) {
    if(fp_trace != NULL) {
        fprintf(fp_trace, "x %p %p %lu\n", func, caller, time(NULL));
    }
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
