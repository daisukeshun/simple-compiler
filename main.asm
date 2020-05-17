format ELF64
public _start
section '.data' writable
	a	dd	0x00
	b	dd	0x00
	c	dd	0x00
	d	dd	0x00
section '.text' executable
_start:
	push	11
	push	10
	pop	rax
	neg	rax
	push	rax
	push	3
	pop	rax
	pop	rbx
	idiv	rbx
	push	rax
	pop	rax
	pop	rbx
	imul	rax,	rbx
	push	rax
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
	call	exit
section '.exit' executable
exit:
	mov	rax,	1
	mov	rbx,	0
	int	0x80
