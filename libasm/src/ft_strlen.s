section .text
	global ft_strlen

ft_strlen:
	xor rax, rax	; Met la len a 0

.loop:
	cmp byte [rdi + rax], 0	; if (str[rax] == '\0')
	je	.end				; if (...) return (rax)
	inc rax			;rax++
	jmp	.loop

.end:
	ret				; return (rax)
