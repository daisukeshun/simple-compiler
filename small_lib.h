#ifndef SMALL_LIB
#define SMALL_LIB

#include <string.h>
#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>

#define nl printf("\n")
int readln(char ** str, FILE * f);
int mystrcmp(const char * str1, const char * str2);

int mystrcmp(const char * str1, const char * str2)
{
	unsigned int i;
	for(i = 0; i < strlen(str2); i++){
		if(str1[i] != str2[i])
		{
			return 0;
		}
	}
	return 1;
}

int readln(char ** str, FILE * f)
{
	if(*str != NULL){
		free(*str);
	}
	*str = NULL;
	unsigned int i = 1;
	char c = 0;
	int pos = ftell(f);
	while(c != '\n' && c != EOF){
		c = fgetc(f);
		i++;
	}
	fseek(f, pos, SEEK_SET);
	*str = (char*)calloc(i, sizeof(char));
	fgets(*str, i, f);
	if(*str == 0)
	{
		i = 0;
	}
	return i;
}

int len(int * line)
{
	return *line;
}

void pLine(int * list)
{
	int i;
	for(i = 0; i < list[0]; i++)
	{
		printf("%d ", list[i+1]);
	}
	nl;
}
#endif
