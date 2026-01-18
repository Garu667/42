NAME = push_swap.a

SRCS = algo_utils.c			\
	benchmark.c				\
	check.c 				\
	chunk_sort.c 			\
	chunk_utils.c 			\
	ft_op.c 				\
	ft_split.c 				\
	index.c 				\
	parsing.c 				\
	push_operations.c 		\
	radix_sort.c 			\
	reverse_operations.c 	\
	rotate_operations.c 	\
	selection_sort.c 		\
	swap_operations.c 		\
	tiny_sort.c				\
	utils.c 				\
	utils2.c 				\

OBJDIR = Objets
OBJS = ${SRCS:%.c=${OBJDIR}/%.o}
DEPS = ${OBJS:.o=.d}

CC = gcc
CFLAGS = -Wall -Werror -Wextra -MMD -MP


all: ${NAME}

${NAME}: ${OBJS}
	ar rcs ${NAME} ${OBJS}

${OBJDIR}/%.o: %.c | ${OBJDIR}
	${CC} ${CFLAGS} -c $< -o $@

${OBJDIR}:
	mkdir -p ${OBJDIR}


clean:
	rm -rf ${OBJDIR}

fclean: clean
	rm -f ${NAME}

re: fclean all


-include ${DEPS}

.PHONY: all clean fclean re