#include <stdio.h>
#define CODE "#include <stdio.h>%1$c#define CODE %3$c%4$s%3$c%1$c#define FT()int main(void){ FILE *f = fopen(%3$cGrace_kid.c%3$c, %3$cw%3$c); if (f == NULL) return (1); fprintf(f, CODE, 10, 9, 34, CODE); fclose(f);}%1$c%1$c/*%1$c	Comment%1$c*/%1$c%1$cFT();%1$c"
#define FT()int main(void){ FILE *f = fopen("Grace_kid.c", "w"); if (f == NULL) return (1); fprintf(f, CODE, 10, 9, 34, CODE); fclose(f);}

/*
	Comment
*/

FT();
