#include <stdio.h>
#include <stdlib.h>

extern size_t	ft_strlen(const char *str);
extern char		*ft_strcpy(char *dst, char *src);
extern int		ft_strcmp(char *s1, char *s2);
extern char		*ft_strdup(const char *s1);

int	main(int ac, char **av)
{
	(void)ac;
	(void)av;
	/*			ft_strlen			*/
	printf("ft_strlen(\"Salut\"):\t%ld\n", ft_strlen("Salut"));

	/*			ft_strcpy			*/
	char	dst[] = "dest_string";
	char	src[] = "src__string";
	printf("ft_strcpy(dst, src):\t%s\n", ft_strcpy(dst, src));

	/*			ft_strcmp			*/
	char	s1[] = "aab";
	char	s2[] = "aaa";
	printf("ft_strcmp(%s, %s):\t%d\n", s1, s2, ft_strcmp(s1, s2));

	/*			ft_strdup			*/
	char	dup[] = "duplicate";
	printf("%s\n", ft_strdup(dup));
}
