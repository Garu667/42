int	rra(t_stack *a, bool write_switch)
{
	t_node	*pre_last;
	t_node	*last;

	if (!a || !a->head || !a->head->next)
		return (0);
	pre_last = a->head;
	while (pre_last->next->next)
		pre_last = pre_last->next;
	last = pre_last->next;
	pre_last->next = NULL;
	last->next = a->head;
	a->head = last;
	if (write_switch)
		write(1, "rra\n", 4);
	return (1);
}

int	rrb(t_stack *b, bool write_switch)
{
	t_node	*pre_last;
	t_node	*last;

	if (!b || !b->head || !b->head->next)
		return (0);
	pre_last = b->head;
	while (pre_last->next->next)
		pre_last = pre_last->next;
	last = pre_last->next;
	pre_last->next = NULL;
	last->next = b->head;
	b->head = last;
	if (write_switch)
		write(1, "rrb\n", 4);
	return (1);
}

int	rrr(t_stack *a, t_stack *b, bool write_switch)
{
	if (!a || !a->head || !a->head->next
		|| !b || !b->head || !b->head->next)
		return (0);
	rra(a, false);
	rrb(b, false);
	if (write_switch)
		write(1, "rrr\n", 4);
	return (1);
}
