#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <string.h>

#define nl printf("\n")

typedef struct {
	unsigned int code[30];
	char ** word;
} Codes;

int readln(char ** str, FILE * f);
int mystrcmp(const char * str1, const char * str2);
unsigned int check(char * word);
unsigned int check(char * word);
unsigned long strip(char * str);

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
	return i;
}

unsigned long strip(char * str)
{
	char * curtok = strtok(str, " ");
	unsigned long i = 0;
	while(curtok != NULL)
	{
		check(curtok);
		curtok = strtok(NULL, " ");
		i++;
	} 
	return i;
}

unsigned int check(char * word)
{
	FILE * output = fopen("output.out", "a");

	unsigned int code;
	unsigned int i;
	char f = 0;
	for(i = 0; i < strlen(word); i++)
	{
		f = 0;
		if(word[i] >= 'A' && word[i] <= 'z')
		{
			if(code == 2){
				code = 20;
				break;
			}
			code = 1;
			fprintf(output, "%c", word[i]);
			printf("%c", word[i]);
		}
		else if(word[i] >= '0' && word[i] <= '9')
		{
			if(code == 1){
				code = 20;
				break;
			}
			code = 2;
			fprintf(output, "%c", word[i]);
			printf("%c", word[i]);
		}
		else {
			if(code == 1 || code == 2){
				if(word[i] == '\n'){
					continue;
				}
				fprintf(stdout, "\t\t%d\n", code);
				fprintf(output, "\t\t%d\n", code);
				f = 1;
			}
			switch (word[i])
			{
				case ';':
					code = 10;
				break;
				case ',':
					code = 11;
				break;
				case '=':
					code = 30;
				break;
				case '+':
					code = 31;
				break;
				case '-':
					code = 32;
				break;
				case '*':
					code = 33;
				break;
				case '/':
					code = 34;
				break;
				case '(':
					code = 35;
				break;
				case ')':
					code = 36;
				break;
			}
			if(word[i] != '\n')
				fprintf(output, "%c", word[i]);
				printf("%c", word[i]);
		}
		if(code >= 30 && code < 40)
		{
			fprintf(stdout, "\t\t%d\n", code);
			fprintf(output, "\t\t%d\n", code);
		}
	}
	if(mystrcmp(word, "Var")){
		code = 3;
	}
	if(mystrcmp(word, "Begin")){
		code = 4;
	}
	if(mystrcmp(word, "End")){
		code = 5;
	}

	if(!(code >= 30 && code < 40))
	{
		fprintf(stdout, "\t\t%d\n", code);
		fprintf(output, "\t\t%d\n", code);
	}

	fclose(output);
	return code;
}

int main(int argc, char ** argv)
{
	if(argc < 2)
		goto END;
	FILE *fp = fopen(argv[1], "r");
	char * str = NULL;
	unsigned long line = 0;

	FILE * output = fopen("output.out", "w");
	fclose(output);
	do
	{
		nl;
		line++;
		readln(&str, fp);
		strip(str);
	} while (strlen(str) != 0);

	fclose(fp);
END:
	return 0;
}

