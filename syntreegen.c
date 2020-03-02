#include "small_lib.h"
#include <limits.h>
int main(int argc, char ** argv)
{
	if(argc < 2)
		goto END;

	char * str = NULL;
	FILE * fp = fopen(argv[1], "r");
	char * word = calloc(INT_MAX, sizeof(char));
	unsigned long line = 0;

	int ** lineOfCode = calloc(1, sizeof(int *));
	*lineOfCode = calloc(1, sizeof(int));
	unsigned long id = 0;
	unsigned long codeCounter = 0;

	do
	{
		readln(&str, fp);
		if(str[1] == ':'){
			id++;
			lineOfCode = realloc(lineOfCode, sizeof(int*) * id);
			sscanf(str,"::%lu\n", &line);
			codeCounter = 0;
		}
		else if (str[0] != '\n' && str[0] != ' ' && str[0] != 0)
		{
			codeCounter++;
			lineOfCode[id - 1] = realloc(lineOfCode[id - 1], sizeof(int) * (codeCounter + 1));
			lineOfCode[id - 1][0] = codeCounter;

			sscanf(str,"%s\t\t%d\n", word, &lineOfCode[id - 1][codeCounter]);
		}
	} while (strlen(str) != 0);


	char basicStructure[3] = { 0 };

	int i, j;
	for(i = 0; i < (int)id; i++)
	{
		for(j = 0; j < lineOfCode[i][0]; j++){
			printf("%d ", lineOfCode[i][j + 1]);
			switch(lineOfCode[i][j + 1])
			{
				case 30:
					{
						if(lineOfCode[i][j] == 1)
						{
							printf(" (variable) ");
						} else 
						{
							printf(" (error) ");
						}
						switch (lineOfCode[i][j + 2])
						{
							case 1:
								printf(" (variable) ");
								break;
							case 2:
								printf(" (const) ");
								break;
						} 
					}
					break;
				case 3:
					nl;
					basicStructure[0] = 1;
					break;
				case 4:
					basicStructure[1] = 1;
					break;
				case 5:
					basicStructure[2] = 1;
					break;
			}
		}
		nl;
	}

	fclose(fp);
END:
	return 0;
}
