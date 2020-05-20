#include <stdio.h>
#include <string.h>

char get_code(char c)
{
	char code = 0;


	( c >= 40)	?	code = 10: 0;	// (
	( c >= 41)	?	code = 11: 0;	// (
	( c == 42)	?	code = 23: 0;	// *
	( c == 43)	?	code = 21: 0;	// +
	( c == 44)	?	code = 20: 0;	//,
	( c == 45)	?	code = 21: 0;	// -
	( c == 47)	?	code = 23: 0;	// /
	( c >= 48 && c <= 57)	?	code = 3: 0;	// 0 - 9
	( c == 58 )	?	code = 5: 0;	// :
	( c == 59 )	?	code = 6: 0;	// ;
	( c == 61 )	?	code = 7: 0;	// =
	( c >= 65 && c <= 90 )	?	code = 8: 0;	// A - Z
	( c >= 97 && c <= 122 )	?	code = 8: 0;	// a - z

	return code;
}

char mstrncmp(char *s1, const char * s2, const size_t n)
{
	char ret = 1;
	(strlen(s1) < n) ? ret = 0 : strlen(s2) < n ? ret = 0 : 0;
	size_t i = 0;
	for (i = 0; i < n; i++)
	{
		if (s1[i] != s2[i]){
			ret = 0;
			break;
		}
	}

	return ret;
}

char is_keyword(char * s)
{
	return	mstrncmp(s, "Begin", 5) +
			mstrncmp(s, "End", 3) + 
			mstrncmp(s, "Var" , 3);
}

int main(int argc, char ** argv)
{
	if(argc < 2)
		goto END;

	FILE *fp = fopen(argv[1], "r");
	unsigned long line = 0;

	FILE * output = fopen("output.out", "w");

	char c = 0;
	char prev_code = 0;

	char word[100000] = { 0 };
	int counter = 0;
	do 
	{
		prev_code = get_code(c);
		c = fgetc(fp);
		if (prev_code != get_code(c) || 
			prev_code == 10 || 
			prev_code == 11 || 
			prev_code == 21 || 
			prev_code == 23 || 
			prev_code == 20 || 
			prev_code == 5 || 
			prev_code == 6 || 
			prev_code == 7) 
		{
			if (prev_code){
				if (is_keyword(word))
				{
					fprintf(output, "\tKeyword");
				}
				else
				{
					fprintf(output, "\t%d", prev_code);
				}
				fprintf(output, "\t%ld\n", line);
				memset((void*)word, 0, 100000);
				counter = 0;
			}
		}
		if (c != '\n' && c != ' ' && c != '\t' && c != EOF)
		{
			word[counter] = c;
			counter++;
			fprintf(output, "%c", c);
		}
		else if (c == '\n')
		{
			line++;
		}

			
	} while (c != EOF);

	fclose(output);
	fclose(fp);
END:
	return 0;
}

