format ELF64
public _start
section '.data' writable
	a	dd	0x00
	b	dd	0x00
	c	dd	0x00
	s	dd	0x00
	d	dd	0x00
section '.text' executable
_start:
jmp	something
	push	4
	push	3
	pop	rax
	pop	rbx
	add	rax,	rbx
	push	rax
	push	5
	push	3
	push	2
	pop	rax
	pop	rbx
	imul	rax,	rbx
	push	rax
	push	1
	pop	rax
	pop	rbx
	add	rax,	rbx
	push	rax
	pop	rax
	pop	rbx
	sub	rax,	rbx
	push	rax
	pop	rax
	neg	rax
	push	rax
	pop	rax
	pop	rbx
	imul	rax,	rbx
	push	rax
	push	20
	push	10
	pop	rax
	neg	rax
	push	rax
	pop	rax
	pop	rbx
	imul	rax,	rbx
	push	rax
	pop	rax
	pop	rbx
	sub	rax,	rbx
	push	rax
	pop	rax
	mov	[a],	eax
jmp	dadada
	push	200
	pop	rax
	mov	[b],	eax
	mov	eax,	[a]
	push	rax
	pop	rax
	mov	[c],	eax
something:
	push	3
	push	2
	push	2
	pop	rax
	pop	rbx
	imul	rax,	rbx
	push	rax
	push	2
	pop	rax
	pop	rbx
	add	rax,	rbx
	push	rax
	pop	rax
	pop	rbx
	sub	rax,	rbx
	push	rax
	pop	rax
	mov	[a],	eax
dadada:
	call	exit
section '.exit' executable
exit:
	mov	rax,	1
	mov	rbx,	0
	int	0x80
