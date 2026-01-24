NAME			= push_swap
BONUS_NAME		= checker

OBJDIR			= objs

CC				= gcc
CFLAGS			= -Wall -Werror -Wextra -MMD -MP

ALGO_SRCS		= algorithms/algo_utils.c	\
				algorithms/chunk_sort.c		\
				algorithms/index.c			\
				algorithms/radix_sort.c		\
				algorithms/selection_sort.c	\
				algorithms/tiny_sort.c

BENCHMARK_SRCS	= benchmark/benchmark.c		\
				benchmark/benchmark_utils.c

OP_SRCS			= operations/push_op.c		\
				operations/reverse_op.c		\
				operations/rotate_op.c		\
				operations/swap_op.c

PARSING_SRCS	= parsing/check.c			\
				parsing/parsing.c			\
				parsing/split.c				\
				parsing/utils.c				\
				parsing/utils2.c

MANDATORY_SRCS	= main_push_swap.c			\
				$(ALGO_SRCS)				\
				$(BENCHMARK_SRCS)			\
				$(OP_SRCS)					\
				$(PARSING_SRCS)

BONUS_SRCS		= bonus/main_checker.c		\
				bonus/gnl.c					\
				bonus/gnl_utils.c			\
				$(OP_SRCS)					\
				$(PARSING_SRCS)


MANDATORY_OBJS	= $(MANDATORY_SRCS:%.c=$(OBJDIR)/%.o)

BONUS_OBJS		= $(BONUS_SRCS:%.c=$(OBJDIR)/%.o)

DEPFILES		= $(MANDATORY_OBJS:.o=.d) $(BONUS_OBJS:.o=.d)

all: $(NAME)

$(NAME): $(MANDATORY_OBJS)
	$(CC) $(CFLAGS) $(MANDATORY_OBJS) -o $(NAME) 

bonus: $(BONUS_NAME)

$(BONUS_NAME): $(BONUS_OBJS)
	$(CC) $(CFLAGS) $(BONUS_OBJS) -o $(BONUS_NAME)

$(OBJDIR)/%.o: %.c
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(OBJDIR)
	rm -f $(DEPFILES)

fclean: clean
	rm -f $(NAME) $(BONUS_NAME)

re: fclean all

-include $(DEPFILES)

.PHONY: all clean fclean re bonus
