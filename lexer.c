#include <stdio.h>

char get_flag(char c)
{
	char flag = 0;

	( c >= 40)	? flag = 1: 0;	// (
	( c >= 42)	? flag = 2: 0;	// * + - /
	( c == 44 ) ? flag = 7: 0;	//,
	( c == 46 ) ? flag = 8: 0;	//.
	( c >= 48 ) ? flag = 3: 0;	// 0 - 9
	( c == 58 ) ? flag = 5: 0;	// :
	( c == 59 ) ? flag = 6: 0;	// ;
	( c >= 60 ) ? flag = 7: 0;	// > = <
	( c >= 65 ) ? flag = 8: 0;	// A - z
	( c > 122 ) ? flag = 9: 0;

	return flag;
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

	do 
	{
		prev_flag = get_flag(c);
		c = fgetc(fp);
		if (prev_flag != get_flag(c) || prev_flag == 1 || prev_flag == 2 || prev_flag == 6 || prev_flag == 7) 
		{
			if (prev_flag){
				fprintf(output, "\t%d\t%ld", prev_flag, line);
				fprintf(output, "\n");
			}
		}
		if (c != '\n' && c != ' ' && c != EOF)
		{
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

