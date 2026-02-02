NAME			= push_swap
BONUS_NAME		= checker

OBJDIR			= objs

CC				= cc
CFLAGS			= -Wall -Werror -Wextra -MMD -MP

SRCS			= selection_sort.c	\
				algo_utils.c		\
				chunk_sort.c		\
				radix_sort.c		\
				tiny_sort.c

SRCS			+= check_flags.c	\
				utils_str.c			\
				parsing.c			\
				index.c				\
				split.c				\
				utils.c

SRCS			+= benchmark.c		\
				benchmark_utils.c

OP_SRCS			= reverse_op.c		\
				rotate_op.c			\
				push_op.c			\
				swap_op.c

MANDATORY_SRCS	= main_push_swap.c	\
				$(OP_SRCS)			\
				$(SRCS)

BONUS_SRCS		= main_checker.c	\
				utils_str.c			\
				algo_utils.c		\
				parsing.c			\
				split.c				\
				utils.c				\
				gnl.c				\
				gnl_utils.c			\
				$(OP_SRCS)			\


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
