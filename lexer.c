#include <stdio.h>
#include <string.h>

char get_flag(char c)
{
	char flag = 0;


	( c >= 40)	? flag = 10: 0;	// (
	( c >= 41)	? flag = 11: 0;	// (
	( c == 42)	? flag = 23: 0;	// *
	( c == 43)	? flag = 21: 0;	// +
	( c == 44)	? flag = 20: 0;	//,
	( c == 45)	? flag = 21: 0;	// -
	( c == 47)	? flag = 23: 0;	// /
	( c >= 48 && c <= 57) ? flag = 3: 0;	// 0 - 9
	( c == 58 ) ? flag = 5: 0;	// :
	( c == 59 ) ? flag = 6: 0;	// ;
	( c == 61 ) ? flag = 7: 0;	// =
	( c >= 65 && c <= 90 ) ? flag = 8: 0;	// A - Z
	( c >= 97 && c <= 122 ) ? flag = 8: 0;	// a - z

	return flag;
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
	char prev_flag = 0;

	char word[100000] = { 0 };
	int counter = 0;
	do 
	{
		prev_flag = get_flag(c);
		c = fgetc(fp);
		if (prev_flag != get_flag(c) || 
			prev_flag == 10 || 
			prev_flag == 11 || 
			prev_flag == 21 || 
			prev_flag == 23 || 
			prev_flag == 20 || 
			prev_flag == 5 || 
			prev_flag == 6 || 
			prev_flag == 7) 
		{
			if (prev_flag){
				if (is_keyword(word))
				{
					fprintf(output, "\tKeyword\t%ld", line);
				}
				else
				{
					fprintf(output, "\t%d\t%ld", prev_flag, line);
				}
				fprintf(output, "\n");
				memset((void*)word, 0, 100000);
				counter = 0;
			}
		}
		if (c != '\n' && c != ' ' && c != EOF)
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

