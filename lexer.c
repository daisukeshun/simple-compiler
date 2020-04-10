#include "small_lib.h"

unsigned int check(char * word);
unsigned long strip(char * str);

unsigned long strip(char * str)
{
	unsigned long i = 0;

	char * curtok = strtok(str, " ");
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

	unsigned int code = 0; 
	unsigned int i;
	for(i = 0; i < strlen(word); i++)
	{
		if(word[i] >= 'A' && word[i] <= 'z')
		{
			if(code == 2){
				code = 20;
				break;
			}
			code = 1;
			fprintf(output, "%c", word[i]);
		}
		else if(word[i] >= '0' && word[i] <= '9')
		{
			if(code == 1){
				code = 20;
				break;
			}
			code = 2;
			fprintf(output, "%c", word[i]);
		}
		else 
		{
			if(code == 1 || code == 2){
				if(word[i] == '\n'){
					continue;
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
				fprintf(output, "\t\t%d\n", code);
			}
			switch (word[i])
			{
				case '=':
					code = 30;
					break;
				case ';':
					code = 10;
				break;
				case ',':
					code = 11;
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
			if(word[i] != '\n'){
				fprintf(output, "%c", word[i]);
			}
		}
		if(code >= 30 && code < 40)
		{
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
	if(mystrcmp(word, ":="))
	{
		code = 30;
	}

	if(!(code >= 30 && code < 40))
	{
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
		readln(&str, fp);
		if(!strlen(str))
			break;

		line++;

		FILE * output = fopen("output.out", "a");
		fprintf(output, "\n::%lu\n", line);
		fclose(output);

		strip(str);
	} while (strlen(str) != 0);

	fclose(fp);
END:
	return 0;
}

