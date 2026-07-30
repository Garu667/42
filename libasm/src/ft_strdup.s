section .text
	extern	malloc
	extern	ft_strlen
	extern	ft_strcpy
	global	ft_strdup

ft_strdup:
	push	rbp
	mov		rbp, rsp
	push	rbx			; Save le registre
	mov		rbx, rdi	; Save src dans le registre
	sub		rsp, 8		; Aligner la stack (16 bytes)

	call	ft_strlen	; rdi contient src
	inc		rax			; rax contient le nbr de bytes a malloc

	mov		rdi, rax
	call	malloc

	call	malloc
	test	rax, rax	; Si NULL goto .end
	jz		.end
;char *ft_strcpy(char *dst, char *src);
;					   ↑ rdi	  ↑ rsi
	mov		rdi, rax	; le pointer qu'on a malloc
	mov		rsi, rbx	; la string donné en argument de ft_strdup
	push	rax
	call	ft_strcpy
	pop		rax			; récupere rax

.end:
	add		rsp, 8
	pop		rbx
	pop		rbp
	ret				; rax contient le pointer ou NULL
