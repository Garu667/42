section .text
	global ft_strcmp

ft_strcmp:
	xor	rax, rax	; Valeur de ret = 0
	xor	rbx, rbx	; i = 0

.loop:
	cmp	byte [rsi + rbx], 0			; if (s1[i] == '\0')
	je	.end
	mov	cl, [rdi + rbx]
	mov	dl, [rsi + rbx]
	cmp	byte dl, cl	; if (s1[i] != s2[i])
	jne	.end
	inc	rbx			; i++
	jmp	.loop

.end:
	movzx	rax, cl
	movzx	rdx, dl
	sub	rax, rdx
	ret				; return (rax)
