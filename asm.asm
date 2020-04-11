section .data
	a:	dd 0x00
	b:	dd 0x00
	c:	dd 0x00
section .bss
section .text
	global _start
_start:
	push ebp
	mov ebp, esp
	mov	eax, 5
	mov	eax, 2
	mul	ebx
	push	eax
	mov	eax, -2
	mov	eax, 3
	mul	ebx
	push	eax
	pop	eax
	pop	ebx
	add	eax, ebx
	push	eax
	mov	eax, -3
	mov	eax, 7
	div	ebx
	push	eax
	mov	eax, 4
	pop	ebx
	mul	ebx
	push	eax
	pop	eax
	pop	ebx
	add	eax, ebx
	push	eax
	mov	eax, 1
	pop	ebx
	add	eax, ebx
	push	eax
	mov	eax, [a]
	pop	ebx
	mov	[eax], ebx
	mov	eax, 10
	mov	eax, 3
	mul	ebx
	push	eax
	mov	eax, 1
	pop	ebx
	add	eax, ebx
	push	eax
	mov	eax, [a]
	pop	ebx
	sub	eax, ebx
	push	eax
	mov	eax, [b]
	pop	ebx
	mov	[eax], ebx
	mov	eax, 0
	pop	ebp
	ret
