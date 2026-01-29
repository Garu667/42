#include <stdio.h>

/*
	Outside Comment
*/

char	*ft_getcode(void)
{
	return ("#include <stdio.h>%2$c%2$c/*%2$c	Outside Comment%2$c*/%2$c%2$cchar	*ft_getcode(void)%2$c{%2$c%1$creturn (%3$c%4$s%3$c);%2$c}%2$c%2$cint	main(void)%2$c{%2$c%1$c/*%2$c%1$c%1$cInside Comment%2$c%1$c*/%2$c%1$cchar	*str = ft_getcode();%2$c%1$cprintf(str, 9, 10, 34, str);%2$c}%2$c");
}

int	main(void)
{
	/*
		Inside Comment
	*/
	char	*str = ft_getcode();
	printf(str, 9, 10, 34, str);
}
