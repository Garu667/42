NAME			= push_swap
BONUS_NAME		= checker

OBJDIR			= objs

CC				= gcc
CFLAGS			= -Wall -Werror -Wextra -MMD -MP

ALGO_SRCS		= algo_utils.c				\
				chunk_sort.c				\
				radix_sort.c				\
				selection_sort.c			\
				tiny_sort.c

BENCHMARK_SRCS	= benchmark.c				\
				benchmark_utils.c

OP_SRCS			= push_op.c					\
				reverse_op.c				\
				rotate_op.c					\
				swap_op.c

PARSING_SRCS	= check_flags.c				\
				index.c						\
				parsing.c					\
				split.c						\
				utils.c						\
				utils_str.c

MANDATORY_SRCS	= main_push_swap.c			\
				$(ALGO_SRCS)				\
				$(BENCHMARK_SRCS)			\
				$(OP_SRCS)					\
				$(PARSING_SRCS)

BONUS_SRCS		= main_checker.c			\
				gnl.c						\
				gnl_utils.c					\
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
