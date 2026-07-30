section .text
	global ft_strcpy

ft_strcpy:
	xor	rax, rax	; Met la len a 0

.loop:
	cmp	byte [rsi + rax], 0			; if (src[i] == '\0')
	je	.end						; if (...) return (rax)
	mov	cl, [rsi + rax]
	mov	[rdi + rax], cl				; dst[i] = src[i]
	inc	rax			; rax++
	jmp	.loop

.end:
	mov	byte [rdi + rax], 0
	mov	rax, rdi
	ret				; return (rax)
