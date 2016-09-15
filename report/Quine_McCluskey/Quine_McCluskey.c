#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h> // ���ڻ�

void setLname(struct leng *length, int xyz[3], int index); // table�� ���κκ� ������ ���� �迭�� �̸� ����.
void setNumXYZ(struct ePI *PI, struct tp *temp, int number, int n, int index); // ���ڸ� 2��ȭ �Ͽ� ���� �� ���յ� ���� 2��ȭ ����
int searchA(struct ePI **PI, int depth, int n, int arrnum); // ���� ù��° ���� ã�´�.
int searchAB(struct ePI **PI, int num1, int n, int arrnum); // ���� �μ��� ��ġ�� ����Ų��
int comPI(struct ePI **PI1, struct ePI **PI2, int n); // �μ��� bin�� ���Ͽ� �ϳ��� �ٸ��ٸ� ��ġ�� ��ȯ�Ѵ�.
int comCheck(struct ePI **dn, struct tp *temp, int *sample, int n); // ����� ���ڵ��� �̹� �迭�� �ִ��� ���ؼ� ���ٸ� ����, ������ ���������ʴ´�. hash���� ������ ������������ ��
void printPI(struct ePI **dn, int *nnn, int n);
void printTable(struct wid *width, struct leng *length, int **table, int *prtable, int c, int colorLine); // table ������ �Բ� ���
void cyclicTable(struct wid *width, struct leng *length, int *wlTemp, int **table, int *prtable, int c, int tc, int *cyclic); // cyclictable ������ �� ��� ����
void dupTable(struct wid *width, struct leng *length, int **table, int *prtable, int c, int max, int imax, int cpi, char *cyclic); // �������� �� �϶� �������
void printCM(struct tp *temp, int c);
struct tp
{
	int d; // depth (0~2), -�� ����
	int num[4]; // d��ġ���� ���ڰ� �����.
	int xyz[3];
};

struct ePI
{
	int number[4]; // �ش��ϴ� ���ڰ� ����Ǵ°� tp�� num�� ����
	int num1; // 1�� ����
	int xyz[3]; // xyz�� �ش��ϴ� ��
	int ischeck; // V Ȯ��
};

struct wid
{
	int num;
	int count;
};

struct leng
{
	int ischeck;
	int count;
	char name[7];
};

int tbin[3];
int nnn[3] = { 0, 0, 0 }; // �� �ܰ��� �迭�� ���ڸ� �����ϱ� ����
int aindex = -1;
int bindex = -1;


/* temp�� d[0] �����ؾ��� �Է¹�����*/
int main()
{
	struct tp temp[12]; // -�� ������ 1�϶��� ��������� �ִ� �ӽ� PI�� �ִ밳����ŭ �迭 ����
	struct ePI *dn[3]; // -�� ���� = i�϶�, dn[i]���� -�� ������ i���϶�, nnn[i]���� ��ŭ PI�� ǥ���ϴ� ePI�� ����Ǿ��ִ�,
	struct wid width[8]; // table���� ���� ����
	struct leng *length; // table���� ���� ����
	int **table; // table�� 2���� �����迭�� ��������� ���
	int prtable[8]; // table ����� ȿ�������� �ϱ�����
	int sample[4]; // ���� [0,1,2,3]������ �����Ҷ� �ű������ ��� ���Ǵ� �ӽù迭
	int i,j,k,l = 0;
	int c = 0; // ó���� �Է¹��� �� ���� check, ���Ŀ� dn�� ischeck�Ȱ��� ������ ��
	int cpi, ep = 0; // ���� pi�� ��ġ�� ��ȯ�ϴ°�, ���Ŀ��� ep�� �Բ� pi���� �����ϴ� ����
	int n, nn = 0; // PI ���� ����Ƚ��, ���߿� cyclic üũ�Ҷ� ���(nn�� dupTable üũ�Ҷ� ���)
	int a = 0; // table���� ����ϴ� ���̵�����
	int tc = 0; // ischeck�� 1�϶� ���ڸ� ��
	int cycR = 0; // �ߺ��ظ� �ް��� ������� table�� �������� ����ϴ� ����
	int wlTemp[8];
	int max, imax = 0;
	char cyclic[20] = "";

	SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 15); // �۾��� ������� ����
	for (i = 0; i < 12; i++)
	{
		temp[i].d = -1;
	}

	i = 0;

	printf("F=��(");
	while (1)
	{
		c = getch();
		if (c == ')')
		{
			putch(c);
			break;
		}
		if ('0' <= c &&  c <= '7')
		{
			putch(c);
			temp[i].num[0] = c - 48; // ascii �ڵ带 digitȭ��
			temp[i].d = 0;
			i++;
		}
		else if (c == ',') putch(c);
	}
	printf("\n");

	printf("ī�����\n");
	printCM(temp, i);

	nnn[0] = i;
	dn[0] = (struct ePI *)malloc(sizeof(struct ePI) * (nnn[0] + 1)); // �迭 ����

	for (i = 0; i < nnn[0]; i++) // 2��ȭ �ϸ鼭 num1�� ����
	{
		setNumXYZ(&dn[0][i], temp, temp[i].num[0], 0, -1);
		dn[0][i].number[0] = temp[i].num[0];
	}

	for (i = 0; i < nnn[0]; i++) // ischeck 1�� �ʱ�ȭ.
	{
		dn[0][i].ischeck = 1;
	}
	
	printPI(dn, nnn, 0);
	//(searchAB������ ��ġ) �� �����ϸ� �ݺ����� {
	for (n = 0; n < 2; n++) // PI�� ����Ƚ�� 0�϶� -�ϳ� ��������� 1�϶� -- ��������� , ---����������� ����Է¹޾ƾ��ϴϱ� 1������ �ݺ�
	{
		for (i = 0; i < 3; i++) // 1�� ������ ���� �ݺ�Ƚ��
		{
			if (searchA(dn, i, n, nnn[n]) == -1) continue; // firstA ã��
			while (searchAB(dn, i, n, nnn[n]) != -1) // �̸� �̿��ؼ� ��ã�������� �ݺ�
			{
				if (bindex == -1) continue; // -1�̸� ���������� �����ܰ�� �Ѿ
				// A�� ù��° ��ġ ��ȯ, dp�� �´� �����迭 ����
				//printf("%d��° PI, %d��° PI ��\n", aindex, bindex); �� �׽�Ʈ
				// �񱳽����� �������̸� �ӽù迭�� dp�� i+1�� PI ����
				// �����̶�� comPI���� �ٸ����� ��ȯ���ٰ��̰� ������ġ�� aindex, bindex�� �̿��ؼ� ���ڸ� �����Ѵ�.
				// aindex ���� comPI�� ��ȯ�� ���� ��ġ�� -1�� �ٲ۴�.
				cpi = comPI(dn, dn, n);

				if (cpi != 999) // ���⿡ �ִ� 1��
				{
					// ������ 1�� �ǰԲ� �� 2���迭�� �޾ƿ�
					
					temp[nnn[n + 1]].d = n + 1;	

					if (comCheck(dn, temp, sample, n))
					{
						setNumXYZ(&dn, temp, temp[nnn[n + 1]].num[0], n, cpi);
						nnn[n + 1]++;
						
						printf("%d��°�װ� %d��°�� �񱳼���, �ٸ���ġ ", aindex+1, bindex+1, cpi);
						switch (cpi)
						{
						case 0: printf("x\n"); break;
						case 1: printf("y\n"); break;
						case 2: printf("z\n"); break;
						default: printf("line 149 ����");
						}
					}

				}

			}
		}
		// ������ ������ �ӽù迭 dp[i+1]���ٰ� �����迭�� ������ �Է�
		aindex = -1;
		bindex = -1;


		// ���⼱ aindex �ʱ�ȭ bindex �ʱ�ȭ �ؾ��ҵ�
		dn[n+1] = (struct ePI *)malloc(sizeof(struct ePI) * (nnn[n+1]));

		// �Ѱ��ܡ� number, xyz, num1����(������), ischeck �ʱ�ȭ
		for (i = 0; i < nnn[n + 1]; i++)
		{
			k = 0;
			for (j = 0; j < (n + 1) * 2; j++)
			{
				dn[n + 1][i].number[j] = temp[i].num[j];
			}
			for (j = 0; j < 3; j++)
			{
				dn[n + 1][i].xyz[j] = temp[i].xyz[j];
				if (temp[i].xyz[j] == 1) k++;
			}
			dn[n + 1][i].num1 = k;
			dn[n + 1][i].ischeck = 1;
		}
		printPI(dn, nnn, n+1);

	} // ��� pi ���� 2��(--0,-0-,0--)���� ��

	printf("\n�ĺ��� �ĺ����� (�ĺ����� �ƴѰ� : V)\n");
	for (k = 0; k < 3; k++)
	{

		for (i = 0; i < nnn[k]; i++)
		{
			if (dn[k][i].ischeck != 1)
			{
				printf("< ");
				for (l = 0; l < 0.5*k*k + 0.5*k + 1; l++)
				{
					printf("%d ", dn[k][i].number[l]);
				}
				printf("> : ", i);
				for (j = 0; j < 3; j++)
				{
					if (dn[k][i].xyz[j] == -1) printf("- ");
					else printf("%d ", dn[k][i].xyz[j]);
				}
				if (dn[k][i].ischeck != 1) printf(" V");
			}
			else // �ĺ����� ��������� 
			{
				SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 14);
				printf("< ");
				for (l = 0; l < 0.5*k*k + 0.5*k + 1; l++)
				{
					printf("%d ", dn[k][i].number[l]);
				}
				printf("> : ", i);
				for (j = 0; j < 3; j++)
				{
					if (dn[k][i].xyz[j] == -1) printf("- ");
					else printf("%d ", dn[k][i].xyz[j]);
				}
				SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 15);
			}

			//printf("num1 : %d / check : %d, ", dn[k][i].num1, dn[k][i].ischeck);
			printf("\n");
		}
		printf("\n");
	}

	c = 0; // c�� �����迭���鶧 �̿�

	for (i = 0; i < 3; i++)
	{
		for (j = 0; j < nnn[i]; j++)
		{
			if (dn[i][j].ischeck == 1)
				c++;
		}
	}
	//// *** ���⼭ c�� 1�̶�� �ٷ� ����ϰ� ����

	// ischeck�� ���� ���� ���� cpi (��Ȱ��)
	cpi = 0;
	// ���μ��� �Ӹ��� ����
	length = (struct leng *)malloc(sizeof(struct leng)*c); // ����
	for (i = 0; i < 8; i++)
	{
		width[i].count = 0;
		width[i].num = i;
	}

	for (i = 0; i < c; i++) // ���̸Ӹ�������
	{
		length[i].ischeck = 0;
		length[i].count = 0;
	}

	// ���̺� ����
	table = (int *)malloc(sizeof(int) * c);
	for (i = 0; i < c; i++)
	{
		table[i] = (int *)malloc(sizeof(int) * 8);
		for (j = 0; j < 8; j++)
		{
			table[i][j] = 0;
		}
	}

	// ���̺� check�� ���� ����
	for (i = 0; i < 3; i++)
	{
		for (j = 0; j < nnn[i]; j++)
		{
			if (dn[i][j].ischeck == 1)
			{
				for (k = 0; k < 0.5*i*i+0.5*i+1; k++)
				{
					table[a][dn[i][j].number[k]] = 1;
					length[a].count++;
					width[dn[i][j].number[k]].count++;
				}
				setLname(length, dn[i][j].xyz, a);
				a++;
			}
		}
	}

	// ��� ȿ�������� �ҷ��� �ʱ�ȭ
	for (i = 0; i < 8; i++)
	{
		if (width[i].count == 0)
			prtable[i] = 0;
		else
			prtable[i] = 1;
	}

	printf("�ĺ��� ���̺�\n");
	printTable(width, length, table, prtable, c, -1);

	a = 0;
	for (i = 0; i < 8; i++)
	{
		if (width[i].count == 1)
		{
			wlTemp[a++] = i;
			tc++;
		}
	}

	// cyclic üũ�κ�
	// if(��� width�� count�� 2�̻��̸� cyclic�̴�) ó������� 2�̻��� ������ ���� ù��° ��(0)�� �������� �ٸ��� �Ͽ� ����Ѵ�.
	n = 0;
	for (i = 0; i < 8; i++)
	{
		if (prtable[i] == 1)
		{
			if (width[i].count < 2)
			{
				n++; // �ϳ��� ������ n�� ������Ű�� Ż��
				break;
			}
		}
	}
	if (nnn[0] == 8) n++; // ������� �޾Ƶ� �Ѿ��
	if (n == 0) // cyclic�� ����̴�. �ӽù迭�� ���� �Ѱܾ��Ѵ�.
	{
		struct wid Cwidth[8]; // table���� ���� ����
		struct leng *Clength; // table���� ���� ����
		int CwlTemp[8];
		int **Ctable; // table�� 2���� �����迭�� ��������� ���
		
		Clength = (struct leng *)malloc(sizeof(struct leng)*c); // ����
		// ���̺� ����
		Ctable = (int *)malloc(sizeof(int) * c);
		for (i = 0; i < c; i++)
		{
			Ctable[i] = (int *)malloc(sizeof(int) * 8);
			for (j = 0; j < 8; j++)
			{
				Ctable[i][j] = table[i][j];
			}
			Clength[i].count = length[i].count;
			Clength[i].ischeck = length[i].ischeck;
			strcpy(Clength[i].name,length[i].name);
		}

		//table �� ������ ����
		for (i = 0; i < 8; i++)
		{
			Cwidth[i].count = width[i].count;
			Cwidth[i].num = width[i].num;
			CwlTemp[i] = wlTemp[i];
		}
		cyclicTable(Cwidth, Clength, CwlTemp, Ctable, prtable, c, tc, cyclic);
	}
	
	printf("\nPI ���ð��� �Դϴ�\n");
	// �۾��Ѵ�

	// �࿡�� �ϳ�¥�� �ɷ���
	for (i = 0; i < c; i++)
	{
		for (j = 0; j < tc; j++)
		{
			if (table[i][wlTemp[j]] == 1) // �ϳ�¥���� �ִ� ���� ã������
			{
				length[i].ischeck = 1;
				cpi++;
				ep++;
				printTable(width, length, table, prtable, c, i);
				for (k = 0; k < 8; k++) // ���࿡ �ִ� ��� 1�� ���ο��� 0���� �Ұ��Ѵ�.
				{
					if (table[i][k] == 1)
					{
						for (l = 0; l < c; l++)
						{
							if (table[l][k] == 1)
							{
								width[k].count--;
								length[l].count--;
							}
							table[l][k] = 0;
	}}}}}}
	printf("EPI�� %d�� �Դϴ�.\n\n",ep);

	max = length[0].count;
	for (i = 0; i < c; i++)
	{
		if (length[i].count > max)
		{
			max = length[i].count;
			imax = i;
		}
	}

	// ū�ݺ��� ����
	while (max != 0) // ���ο��� count�� ��ū�� 0�̸� �� �ߴ� �Ҹ�
	{
		// �� ���� ����Ұ��̹Ƿ� �� ���� 1�� �ʱ�ȭ
		for (i = 0; i < 8; i++)
		{
			if (width[i].count >= 2)
			{
				nn++;
			}
		}
		if (nn == 1)
		{
			struct wid Cwidth[8]; // table���� ���� ����
			struct leng *Clength; // table���� ���� ����
			int **Ctable; // table�� 2���� �����迭�� ��������� ���
			int Cmax = max;
			int Cimax = imax;
			Clength = (struct leng *)malloc(sizeof(struct leng)*c); // ����
			// ���̺� ����
			Ctable = (int *)malloc(sizeof(int) * c);
			for (i = 0; i < c; i++)
			{
				Ctable[i] = (int *)malloc(sizeof(int) * 8);
				for (j = 0; j < 8; j++)
				{
					Ctable[i][j] = table[i][j];
				}
				Clength[i].count = length[i].count;
				Clength[i].ischeck = length[i].ischeck;
				strcpy(Clength[i].name, length[i].name);
			}

			//table �� ������ ����
			for (i = 0; i < 8; i++)
			{
				Cwidth[i].count = width[i].count;
				Cwidth[i].num = width[i].num;
			}
			// 2��° �� ǥ�� check ���� = 1��
			dupTable(Cwidth, Clength, Ctable, prtable, c, max, imax, cpi, cyclic);
		}

		length[imax].ischeck = 1;
		cpi++;
		for (j = 0; j < 8; j++)
		{
			//table[imax][j]�� 1�ΰ� ��� 0���� �ٲ۴�
			if (table[imax][j] == 1)
			{
				for (l = 0; l < c; l++)
				{
					if (table[l][j] == 1)
					{
						width[j].count--;
						length[l].count--;
					}
					table[l][j] = 0;
				}
			}
		}
		max = length[0].count;
		for (i = 0; i < c; i++)
		{
			if (length[i].count > max)
			{
				max = length[i].count;
				imax = i;
			}
		}
		printTable(width, length, table, prtable, c, imax);
	}
	ep = cpi;
	printf("\nF = ");
	for (i = 0; i < c; i++)
	{
		if (length[i].ischeck == 1)
		{
			printf("%s", length[i].name);
			if (cpi-- > 1) printf("+");
		}
	}
	printf("�Դϴ�. \n����Ϸ�\n\n");
	//ū�ݺ��� ����

	printf("\nF = ");
	for (i = 0; i < c; i++)
	{
		if (length[i].ischeck == 1)
		{
			printf("%s",length[i].name);
			if (ep-- > 1) printf("+");
		}
	}
	if(nnn[0] == 8) printf(" �Ǵ� y+y' �Ǵ� z+z' �̹Ƿ� 1�Դϴ�.");
	else if (n == 0 || nn == 1) printf(" �Ǵ� %s", cyclic); // n==0�̸� cyclic, nn==1�̸� ����
	printf("\n");
}



void printCM(struct tp *temp, int c)
{
	int i;
	int CM[8] = {0};
	for(i=0;i<c;i++)
	{
		CM[temp[i].num[0]] = 1;
	}
	
	printf("\nx��yz\t00\t01\t11\t10\n");
	printf("0\t%d\t%d\t%d\t%d\n",CM[0],CM[1],CM[3],CM[2]);
	printf("1\t%d\t%d\t%d\t%d\n",CM[4],CM[5],CM[7],CM[6]);
}


void printPI(struct ePI **dn, int *nnn, int n)
{
	int i,j,l;
	printf("\n-�� ������ %d���� TABLE\n", n);
	for (i = 0; i < nnn[n]; i++)
	{
		printf("< ");
		for (l = 0; l < 0.5*n*n + 0.5*n + 1; l++)
		{
			printf("%d ", dn[n][i].number[l]);
		}
		printf("> : ", i);
		for (j = 0; j < 3; j++)
		{
			if (dn[n][i].xyz[j] == -1) printf("- ");
			else printf("%d ", dn[n][i].xyz[j]);
		}
		if (dn[n][i].ischeck != 1) printf(" V");
		//printf("num1 : %d / check : %d, ", dn[k][i].num1, dn[k][i].ischeck);
		printf("\n");
	}
	printf("\n�׷찣 ���� ����\n");
}




void printTable(struct wid *width, struct leng *length, int **table, int *prtable, int c, int colorLine)
{
	int i,j;
	printf("(TABLE)\t");
	for (i = 0; i < 8; i++)
	{
		if (prtable[i] == 1) printf("%d ", width[i].num, width[i].count);
	}
	printf("\n");
	for (i = 0; i < c; i++)
	{
		if (i == colorLine)
		{
			SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 2); // 1�� �Ķ�, 4�� ����, 0�� ����!
			printf("%s\t", length[i].name);
			if (length[i].ischeck == 1) printf("\b\bV ");
			//printf("%s%d%d\t", length[i].name, length[i].count, length[i].ischeck); // count��ȭ, ischeck ��ȭ Ȯ��
			for (j = 0; j < 8; j++)
			{
				if (prtable[j] == 1) printf("%d ", table[i][j]);
			}
			SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 15); // 15�� ���� ���
		}
		else
		{
			printf("%s\t", length[i].name);
			if (length[i].ischeck == 1) printf("\b\bV ");
			//printf("%s%d%d\t", length[i].name, length[i].count, length[i].ischeck); // count��ȭ, ischeck ��ȭ Ȯ��
			for (j = 0; j < 8; j++)
			{
				if (prtable[j] == 1) printf("%d ", table[i][j]);
			}
		}
		printf("\n");
	}
	printf("\n");
}

void setLname(struct leng *length, int xyz[3], int index)
{
	strcpy(length[index].name, "");

	switch (xyz[0])
	{
	case 0: strcat(length[index].name, "x'"); break;
	case 1: strcat(length[index].name, "x"); break;
	default: break;
	}

	switch (xyz[1])
	{
	case 0: strcat(length[index].name, "y'"); break;
	case 1: strcat(length[index].name, "y"); break;
	default: break;
	}

	switch (xyz[2])
	{
	case 0: strcat(length[index].name, "z'"); break;
	case 1: strcat(length[index].name, "z"); break;
	default: break;
	}
}

void setNumXYZ(struct ePI *PI, struct tp *temp, int number, int n, int index) // PI�� xyz�� 2������ �ְ� 1�ǰ����� ����
{
	int i;

	if (index == -1)
	{
		PI->num1 = 0;
		for (i = 2; i >= 0; i--)
		{
			PI->xyz[i] = number % 2;
			if (PI->xyz[i] == 1) PI->num1++;
			number = number / 2;
		}
	}
	else // dn���� n-1�϶��� xyz�� �޾ƿͼ� index�� ����Ǿ��ִ� ���� -1�� �ٲ��ش�.
	{
		tbin[index] = -1;
		for (i = 0; i < 3; i++)
		{
			temp[nnn[n + 1]].xyz[i] = tbin[i];
		}
	}
}

int searchA(struct ePI **PI, int num1, int n, int arrnum) // A�� ù��° ��ġ ��ȯ, dp�� �´� �����迭 ����
{
	int i;
	for (i = 0; i < arrnum; i++)
	{
		if (PI[n][i].num1 == num1)
		{
			aindex = i;
			return i;
		}
	}
	return -1; // ù��° A�� �����ϸ� ���� num1�� �Ѿ�� �˻��ؾ���
}

int searchAB(struct ePI **PI, int num1, int n, int arrnum) // n�� PI[0~2] �� ������
{ // num1 �� ã�Ƽ� ��ġ�� ��´�. depth, n(0~3) �Է¹���, arrnum��ŭ ã�ƾ��� // ���ؾ��� �� ����� ��ǥ�� ����ش�
	int i;
	for (i = bindex + 1; i < arrnum; i++)
	{
		if (PI[n][i].num1 == num1 + 1)
		{
			bindex = i;
			return i; //b ��ġ ��ȯ
		}
	}

	bindex = -1; // b���� ��ã������ b�� -1�� �ʱ�ȭ���ش�

	// a ��ġ
	for (i = aindex + 1; i < arrnum; i++)
	{
		if (PI[n][i].num1 == num1)
		{
			aindex = i;
			return i;
		}
	}
	return -1; // a,b �Ѵ� ���� ���ڰ� ���ٸ� 0��ȯ
}

int comPI(struct ePI **PI1, struct ePI **PI2, int n) // PI�� ���ϰ� 1���� �ٸ��ٸ� ��ġ index ��ȯ, �ƴϸ� 999
{
	int i;
	int index;
	int c = 0; // 1���ΰ� �ƴѰ� check �ϴ� ����
	for (i = 0; i < 3; i++)
	{
		if (PI1[n][aindex].xyz[i] != PI2[n][bindex].xyz[i])
		{
			index = i;
			c++;
		}
	}

	// ischeck�� v Ȯ���ؾ���. V����ؾ��Ѵٸ� 1, �ƴϸ� 0
	// - ����
	if (c == 1) // �ٸ��� �Ѱ���� �� ��ġ ��ȯ
	{
		PI1[n][aindex].ischeck = 0;
		PI2[n][bindex].ischeck = 0;
		//printf("�ٸ� ��ġ : %d, ischeck : 0���� �ʱ�ȭ\n", index, aindex, bindex);
		for (i = 0; i < 3; i++)
		{
			tbin[i] = PI1[n][aindex].xyz[i];
		}
		return index;
	}
	// - ���ȉ�, 1�� �ʱ�ȭ �صξ����Ƿ� ���Ȱ͸� 0���� ����
	else
		return 999;
}

int comCheck(struct ePI **dn, struct tp *temp, int *sample, int n) // exist check(�ӽù迭������, temp�迭 ������, n(�� 0�϶� 2�� ��, n�� 1�϶� 2����));
{
	int i,k;
	int sumS = 0;
	int sumT = 0;
	
	for (i = 0, k = 0; i < (n + 1); i++,k++) // abindex�� ����Ű�� ���ڵ� �� sample�� ���� �����ؾ���
	{
		sample[i + k] = dn[n][aindex].number[k];
		sample[i + 1 + k] = dn[n][bindex].number[k];
	}
	for (i = 0; i < (n + 1) * 2 - 1; i++) // ��������
	{
		for (k = (n + 1) * 2 - 1; k > 0; k--)
		{
			if (sample[k] < sample[k - 1])
			{
				sample[k - 1] = sample[k - 1] + sample[k];
				sample[k] = sample[k - 1] - sample[k];
				sample[k - 1] = sample[k - 1] - sample[k];
			}
		}
	}

	if (nnn[n + 1] == 0)
	{
		for (i = 0; i < (n + 1) * 2; i++)
		{
			temp[0].num[i] = sample[i];// �ٷ� temp�� ����
		}

		return 1; // ����ְų� ������ ���ٸ� 1 ��ȯ.
	}

	// nnn[n+1]�� 0���� ũ�ٸ� PI�� �ִ��� ������ ���ϰ� ����. (�� ����� ������ �������� ���� �ؽ������� ����)
	
	for (k = 0; k < (n + 1) * 2; k++)
	{
		sumS += sample[k] * sample[k];
	}

	for (i = 0; i < nnn[n + 1]; i++) // 
	{
		sumT = 0;
		for (k = 0; k < (n + 1) * 2; k++)
		{
			sumT += (temp[i].num[k]) * (temp[i].num[k]);
		}

		if (sumT == sumS) return 0; // �������� �ϳ��� ������ �Ÿ���.
	}

	// �������� ���ٸ� temp�� ����
	for (i = 0; i < (n + 1) * 2; i++)
	{
		temp[nnn[n + 1]].num[i] = sample[i];
	}
	return 1;
}

void cyclicTable(struct wid *width, struct leng *length, int *wlTemp, int **table, int *prtable, int c, int tc, int *cyclic)
{
	int a, i, j, k, l, max, imax, cpi,ep;
	a = 0;
	cpi = 0;
	ep = 0;
	printf("���ڰ� �����ϴ� ��� ���� count�� 2 �̻��̹Ƿ� Cyclic �Դϴ�.\n");
	printf("PI ���� �����Դϴ�.\n");
	for (i = 0; i < 8; i++)
	{
		if (width[i].count == 1)
		{
			wlTemp[a++] = i;
			tc++;
		}
	}

	// �࿡�� �ϳ�¥�� �ɷ���
	for (i = 0; i < c; i++)
	{
		for (j = 0; j < tc; j++)
		{
			if (table[i][wlTemp[j]] == 1) // �ϳ�¥���� �ִ� ���� ã������
			{
				length[i].ischeck = 1;
				cpi++;
				ep++;
				for (k = 0; k < 8; k++) // ���࿡ �ִ� ��� 1�� ���ο��� 0���� �Ұ��Ѵ�.
				{
					if (table[i][k] == 1)
					{
						for (l = 0; l < c; l++)
						{
							if (table[l][k] == 1)
							{
								width[k].count--;
							}
							table[l][k] = 0;
	}}}}}}
	printf("EPI�� %d�� �Դϴ�.\n\n",ep);


	// �񱳼��ڸ� +1ĭ���� �����ؼ� �񱳽���*
	max = length[1].count;
	imax = 1;
	for (i = 0; i < c; i++)
	{
		if (length[i].count > max)
		{
			max = length[i].count;
			imax = i;
		}
	}
	printTable(width, length, table, prtable, c, imax);
	// ū�ݺ��� �ʿ���
	while (max != 0)
	{
		// �� ���� ����Ұ��̹Ƿ� �� ���� 1�� �ʱ�ȭ
		length[imax].ischeck = 1;
		cpi++;
		for (j = 0; j < 8; j++)
		{
			//table[imax][j]�� 1�ΰ� ��� 0���� �ٲ۴�
			if (table[imax][j] == 1)
			{
				for (l = 0; l < c; l++)
				{
					if (table[l][j] == 1)
					{
						width[j].count--;
						length[l].count--;
					}
					table[l][j] = 0;
				}
			}
		}
		max = length[0].count;
		for (i = 0; i < c; i++)
		{
			if (length[i].count > max)
			{
				max = length[i].count;
				imax = i;
			}
		}
		printTable(width, length, table, prtable, c, imax);
	}
	printf("Cyclic ����Ϸ�\n");
	//ū�ݺ��� ����

	for (i = 0; i < c; i++)
	{
		if (length[i].ischeck == 1)
		{
			strcat(cyclic, length[i].name);
			if (cpi-- > 1) strcat(cyclic, "+");
		}
	}
	printf("F = %s�� ������� �����Ͽ����ϴ�.\n", cyclic);
}

void dupTable(struct wid *width, struct leng *length, int **table, int *prtable, int c, int max, int imax, int cpi, char *cyclic)
{
	int i, j, k, l;
	printf("���⼭ �ظ� ������ �� �ֽ��ϴ�.\n");
	printTable(width, length, table, prtable, c, -1);
	// width count�� 2�̻��� �ϳ��� ������
	// �迭 �����ؼ� ���

	max = length[0].count;
	for (i = 0; i < c; i++)
	{
		if (length[i].count >= max)
		{
			max = length[i].count;
			imax = i;
		}
	}
	length[imax].ischeck = 1;
	cpi++;
	printTable(width, length, table, prtable, c, imax);
	for (j = 0; j < 8; j++)
	{
		//table[imax][j]�� 1�ΰ� ��� 0���� �ٲ۴�
		if (table[imax][j] == 1)
		{
			for (l = 0; l < c; l++)
			{
				if (table[l][j] == 1)
				{
					width[j].count--;
					length[l].count--;
				}
				table[l][j] = 0;
			}
		}
	}
	printTable(width, length, table, prtable, c, imax);

	for (i = 0; i < c; i++)
	{
		if (length[i].ischeck == 1)
		{
			strcat(cyclic, length[i].name);
			if (cpi-- > 1) strcat(cyclic, "+");
		}
	}

	printf("������ ����Ϸ�\n");
	//ū�ݺ��� ����
	printf("F = %s�� ������� �����Ͽ����ϴ�.\n\n�ٸ����\n", cyclic);
}