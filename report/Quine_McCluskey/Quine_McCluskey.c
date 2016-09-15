#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h> // 글자색

void setLname(struct leng *length, int xyz[3], int index); // table의 세로부분 정보를 가진 배열에 이름 저장.
void setNumXYZ(struct ePI *PI, struct tp *temp, int number, int n, int index); // 숫자를 2진화 하여 저장 및 결합된 숫자 2진화 저장
int searchA(struct ePI **PI, int depth, int n, int arrnum); // 비교할 첫번째 수를 찾는다.
int searchAB(struct ePI **PI, int num1, int n, int arrnum); // 비교할 두수의 위치를 가리킨다
int comPI(struct ePI **PI1, struct ePI **PI2, int n); // 두수의 bin을 비교하여 하나만 다르다면 위치를 반환한다.
int comCheck(struct ePI **dn, struct tp *temp, int *sample, int n); // 저장될 숫자들이 이미 배열에 있는지 비교해서 없다면 저장, 있으면 저장하지않는다. hash값을 각수의 제곱의합으로 함
void printPI(struct ePI **dn, int *nnn, int n);
void printTable(struct wid *width, struct leng *length, int **table, int *prtable, int c, int colorLine); // table 정보와 함께 출력
void cyclicTable(struct wid *width, struct leng *length, int *wlTemp, int **table, int *prtable, int c, int tc, int *cyclic); // cyclictable 계산과정 및 결과 저장
void dupTable(struct wid *width, struct leng *length, int **table, int *prtable, int c, int max, int imax, int cpi, char *cyclic); // 선택적인 해 일때 결과저장
void printCM(struct tp *temp, int c);
struct tp
{
	int d; // depth (0~2), -의 개수
	int num[4]; // d위치까지 숫자가 저장됨.
	int xyz[3];
};

struct ePI
{
	int number[4]; // 해당하는 숫자가 저장되는곳 tp의 num과 같음
	int num1; // 1의 개수
	int xyz[3]; // xyz에 해당하는 수
	int ischeck; // V 확인
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
int nnn[3] = { 0, 0, 0 }; // 각 단계의 배열의 숫자를 저장하기 위함
int aindex = -1;
int bindex = -1;


/* temp에 d[0] 고정해야함 입력받을때*/
int main()
{
	struct tp temp[12]; // -의 개수가 1일때의 만들어질수 있는 임시 PI의 최대개수만큼 배열 생성
	struct ePI *dn[3]; // -의 개수 = i일때, dn[i]에는 -의 개수가 i개일때, nnn[i]개수 만큼 PI를 표현하는 ePI가 저장되어있다,
	struct wid width[8]; // table에서 가로 정보
	struct leng *length; // table에서 세로 정보
	int **table; // table을 2차원 동적배열을 만들기위해 사용
	int prtable[8]; // table 출력을 효율적으로 하기위함
	int sample[4]; // 숫자 [0,1,2,3]같은걸 저장할때 옮기기위해 잠시 사용되는 임시배열
	int i,j,k,l = 0;
	int c = 0; // 처음엔 입력받은 수 개수 check, 이후엔 dn의 ischeck된것의 개수를 셈
	int cpi, ep = 0; // 비교한 pi의 위치를 반환하는거, 이후에는 ep와 함께 pi개수 저장하는 변수
	int n, nn = 0; // PI 추출 시행횟수, 나중엔 cyclic 체크할때 사용(nn은 dupTable 체크할때 사용)
	int a = 0; // table에서 사용하는 행이동변수
	int tc = 0; // ischeck가 1일때 숫자를 셈
	int cycR = 0; // 중복해를 받고나서 원래대로 table을 돌리려고 사용하는 변수
	int wlTemp[8];
	int max, imax = 0;
	char cyclic[20] = "";

	SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 15); // 글씨색 흰색으로 지정
	for (i = 0; i < 12; i++)
	{
		temp[i].d = -1;
	}

	i = 0;

	printf("F=∑(");
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
			temp[i].num[0] = c - 48; // ascii 코드를 digit화함
			temp[i].d = 0;
			i++;
		}
		else if (c == ',') putch(c);
	}
	printf("\n");

	printf("카르노맵\n");
	printCM(temp, i);

	nnn[0] = i;
	dn[0] = (struct ePI *)malloc(sizeof(struct ePI) * (nnn[0] + 1)); // 배열 생성

	for (i = 0; i < nnn[0]; i++) // 2진화 하면서 num1에 넣음
	{
		setNumXYZ(&dn[0][i], temp, temp[i].num[0], 0, -1);
		dn[0][i].number[0] = temp[i].num[0];
	}

	for (i = 0; i < nnn[0]; i++) // ischeck 1로 초기화.
	{
		dn[0][i].ischeck = 1;
	}
	
	printPI(dn, nnn, 0);
	//(searchAB에서의 서치) 가 실패하면 반복종료 {
	for (n = 0; n < 2; n++) // PI의 연산횟수 0일때 -하나 만들어지고 1일때 -- 만들어지고 , ---만들어질려면 모두입력받아야하니까 1까지만 반복
	{
		for (i = 0; i < 3; i++) // 1의 개수에 따른 반복횟수
		{
			if (searchA(dn, i, n, nnn[n]) == -1) continue; // firstA 찾고
			while (searchAB(dn, i, n, nnn[n]) != -1) // 이를 이용해서 못찾을때까지 반복
			{
				if (bindex == -1) continue; // -1이면 비교하지말고 다음단계로 넘어감
				// A의 첫번째 위치 반환, dp에 맞는 동적배열 개수
				//printf("%d번째 PI, %d번째 PI 비교\n", aindex, bindex); 비교 테스트
				// 비교시행후 성공값이면 임시배열에 dp가 i+1인 PI 생성
				// 성공이라면 comPI에서 다른값을 반환해줄것이고 현재위치의 aindex, bindex를 이용해서 숫자를 저장한다.
				// aindex 에서 comPI가 반환한 값의 위치를 -1로 바꾼다.
				cpi = comPI(dn, dn, n);

				if (cpi != 999) // 여기에 있는 1은
				{
					// 위에서 1이 되게끔 한 2진배열을 받아옴
					
					temp[nnn[n + 1]].d = n + 1;	

					if (comCheck(dn, temp, sample, n))
					{
						setNumXYZ(&dn, temp, temp[nnn[n + 1]].num[0], n, cpi);
						nnn[n + 1]++;
						
						printf("%d번째항과 %d번째항 비교성공, 다른위치 ", aindex+1, bindex+1, cpi);
						switch (cpi)
						{
						case 0: printf("x\n"); break;
						case 1: printf("y\n"); break;
						case 2: printf("z\n"); break;
						default: printf("line 149 에러");
						}
					}

				}

			}
		}
		// 위에서 생성한 임시배열 dp[i+1]에다가 동적배열로 생성후 입력
		aindex = -1;
		bindex = -1;


		// 여기선 aindex 초기화 bindex 초기화 해야할듯
		dn[n+1] = (struct ePI *)malloc(sizeof(struct ePI) * (nnn[n+1]));

		// 넘겨줌★ number, xyz, num1개수(세야함), ischeck 초기화
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

	} // 모든 pi 연산 2차(--0,-0-,0--)까지 끝

	printf("\n후보항 식별과정 (후보항이 아닌것 : V)\n");
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
			else // 후보항은 노란색으로 
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

	c = 0; // c를 동적배열만들때 이용

	for (i = 0; i < 3; i++)
	{
		for (j = 0; j < nnn[i]; j++)
		{
			if (dn[i][j].ischeck == 1)
				c++;
		}
	}
	//// *** 여기서 c가 1이라면 바로 출력하고 종료

	// ischeck의 개수 세는 변수 cpi (재활용)
	cpi = 0;
	// 가로세로 머릿말 세팅
	length = (struct leng *)malloc(sizeof(struct leng)*c); // 선언
	for (i = 0; i < 8; i++)
	{
		width[i].count = 0;
		width[i].num = i;
	}

	for (i = 0; i < c; i++) // 높이머릿말지정
	{
		length[i].ischeck = 0;
		length[i].count = 0;
	}

	// 테이블 생성
	table = (int *)malloc(sizeof(int) * c);
	for (i = 0; i < c; i++)
	{
		table[i] = (int *)malloc(sizeof(int) * 8);
		for (j = 0; j < 8; j++)
		{
			table[i][j] = 0;
		}
	}

	// 테이블에 check된 수들 넣음
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

	// 출력 효율적으로 할려고 초기화
	for (i = 0; i < 8; i++)
	{
		if (width[i].count == 0)
			prtable[i] = 0;
		else
			prtable[i] = 1;
	}

	printf("식별전 테이블\n");
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

	// cyclic 체크부분
	// if(모든 width의 count가 2이상이면 cyclic이다) 처리방법은 2이상인 숫자의 가장 첫번째 수(0)을 시작점을 다르게 하여 출력한다.
	n = 0;
	for (i = 0; i < 8; i++)
	{
		if (prtable[i] == 1)
		{
			if (width[i].count < 2)
			{
				n++; // 하나라도 있으면 n을 증가시키고 탈출
				break;
			}
		}
	}
	if (nnn[0] == 8) n++; // 모든항을 받아도 넘어간다
	if (n == 0) // cyclic인 경우이다. 임시배열을 만들어서 넘겨야한다.
	{
		struct wid Cwidth[8]; // table에서 가로 정보
		struct leng *Clength; // table에서 세로 정보
		int CwlTemp[8];
		int **Ctable; // table을 2차원 동적배열을 만들기위해 사용
		
		Clength = (struct leng *)malloc(sizeof(struct leng)*c); // 선언
		// 테이블 생성
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

		//table 및 정보들 복사
		for (i = 0; i < 8; i++)
		{
			Cwidth[i].count = width[i].count;
			Cwidth[i].num = width[i].num;
			CwlTemp[i] = wlTemp[i];
		}
		cyclicTable(Cwidth, Clength, CwlTemp, Ctable, prtable, c, tc, cyclic);
	}
	
	printf("\nPI 선택과정 입니다\n");
	// 작업한다

	// 행에서 하나짜리 걸러냄
	for (i = 0; i < c; i++)
	{
		for (j = 0; j < tc; j++)
		{
			if (table[i][wlTemp[j]] == 1) // 하나짜리가 있는 행을 찾았으면
			{
				length[i].ischeck = 1;
				cpi++;
				ep++;
				printTable(width, length, table, prtable, c, i);
				for (k = 0; k < 8; k++) // 그행에 있는 모든 1의 세로열을 0으로 소거한다.
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
	printf("EPI는 %d개 입니다.\n\n",ep);

	max = length[0].count;
	for (i = 0; i < c; i++)
	{
		if (length[i].count > max)
		{
			max = length[i].count;
			imax = i;
		}
	}

	// 큰반복문 시작
	while (max != 0) // 세로에서 count중 젤큰게 0이면 다 했단 소리
	{
		// 이 행을 사용할것이므로 이 행은 1로 초기화
		for (i = 0; i < 8; i++)
		{
			if (width[i].count >= 2)
			{
				nn++;
			}
		}
		if (nn == 1)
		{
			struct wid Cwidth[8]; // table에서 가로 정보
			struct leng *Clength; // table에서 세로 정보
			int **Ctable; // table을 2차원 동적배열을 만들기위해 사용
			int Cmax = max;
			int Cimax = imax;
			Clength = (struct leng *)malloc(sizeof(struct leng)*c); // 선언
			// 테이블 생성
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

			//table 및 정보들 복사
			for (i = 0; i < 8; i++)
			{
				Cwidth[i].count = width[i].count;
				Cwidth[i].num = width[i].num;
			}
			// 2번째 해 표시 check 변수 = 1함
			dupTable(Cwidth, Clength, Ctable, prtable, c, max, imax, cpi, cyclic);
		}

		length[imax].ischeck = 1;
		cpi++;
		for (j = 0; j < 8; j++)
		{
			//table[imax][j]가 1인건 모두 0으로 바꾼다
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
	printf("입니다. \n시행완료\n\n");
	//큰반복문 닫음

	printf("\nF = ");
	for (i = 0; i < c; i++)
	{
		if (length[i].ischeck == 1)
		{
			printf("%s",length[i].name);
			if (ep-- > 1) printf("+");
		}
	}
	if(nnn[0] == 8) printf(" 또는 y+y' 또는 z+z' 이므로 1입니다.");
	else if (n == 0 || nn == 1) printf(" 또는 %s", cyclic); // n==0이면 cyclic, nn==1이면 다항
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
	
	printf("\nx＼yz\t00\t01\t11\t10\n");
	printf("0\t%d\t%d\t%d\t%d\n",CM[0],CM[1],CM[3],CM[2]);
	printf("1\t%d\t%d\t%d\t%d\n",CM[4],CM[5],CM[7],CM[6]);
}


void printPI(struct ePI **dn, int *nnn, int n)
{
	int i,j,l;
	printf("\n-의 개수가 %d개인 TABLE\n", n);
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
	printf("\n그룹간 결합 과정\n");
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
			SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 2); // 1는 파랑, 4는 빨강, 0은 검정!
			printf("%s\t", length[i].name);
			if (length[i].ischeck == 1) printf("\b\bV ");
			//printf("%s%d%d\t", length[i].name, length[i].count, length[i].ischeck); // count변화, ischeck 변화 확인
			for (j = 0; j < 8; j++)
			{
				if (prtable[j] == 1) printf("%d ", table[i][j]);
			}
			SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 15); // 15는 진한 흰색
		}
		else
		{
			printf("%s\t", length[i].name);
			if (length[i].ischeck == 1) printf("\b\bV ");
			//printf("%s%d%d\t", length[i].name, length[i].count, length[i].ischeck); // count변화, ischeck 변화 확인
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

void setNumXYZ(struct ePI *PI, struct tp *temp, int number, int n, int index) // PI의 xyz에 2진수를 넣고 1의개수도 넣음
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
	else // dn에서 n-1일때의 xyz도 받아와서 index에 저장되어있는 수만 -1로 바꿔준다.
	{
		tbin[index] = -1;
		for (i = 0; i < 3; i++)
		{
			temp[nnn[n + 1]].xyz[i] = tbin[i];
		}
	}
}

int searchA(struct ePI **PI, int num1, int n, int arrnum) // A의 첫번째 위치 반환, dp에 맞는 동적배열 개수
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
	return -1; // 첫번째 A를 실패하면 다음 num1로 넘어가서 검색해야함
}

int searchAB(struct ePI **PI, int num1, int n, int arrnum) // n은 PI[0~2] 의 숫자임
{ // num1 을 찾아서 위치를 잡는다. depth, n(0~3) 입력받음, arrnum만큼 찾아야함 // 비교해야할 두 대상의 좌표를 잡아준다
	int i;
	for (i = bindex + 1; i < arrnum; i++)
	{
		if (PI[n][i].num1 == num1 + 1)
		{
			bindex = i;
			return i; //b 위치 반환
		}
	}

	bindex = -1; // b에서 못찾았으면 b를 -1로 초기화해준다

	// a 위치
	for (i = aindex + 1; i < arrnum; i++)
	{
		if (PI[n][i].num1 == num1)
		{
			aindex = i;
			return i;
		}
	}
	return -1; // a,b 둘다 같은 숫자가 없다면 0반환
}

int comPI(struct ePI **PI1, struct ePI **PI2, int n) // PI를 비교하고 1개만 다르다면 위치 index 반환, 아니면 999
{
	int i;
	int index;
	int c = 0; // 1개인가 아닌가 check 하는 변수
	for (i = 0; i < 3; i++)
	{
		if (PI1[n][aindex].xyz[i] != PI2[n][bindex].xyz[i])
		{
			index = i;
			c++;
		}
	}

	// ischeck에 v 확인해야함. V사용해야한다면 1, 아니면 0
	// - 사용됌
	if (c == 1) // 다른게 한개라면 그 위치 반환
	{
		PI1[n][aindex].ischeck = 0;
		PI2[n][bindex].ischeck = 0;
		//printf("다른 위치 : %d, ischeck : 0으로 초기화\n", index, aindex, bindex);
		for (i = 0; i < 3; i++)
		{
			tbin[i] = PI1[n][aindex].xyz[i];
		}
		return index;
	}
	// - 사용안됌, 1로 초기화 해두었으므로 사용된것만 0으로 변경
	else
		return 999;
}

int comCheck(struct ePI **dn, struct tp *temp, int *sample, int n) // exist check(임시배열포인터, temp배열 포인터, n(이 0일때 2개 비교, n이 1일때 2개비교));
{
	int i,k;
	int sumS = 0;
	int sumT = 0;
	
	for (i = 0, k = 0; i < (n + 1); i++,k++) // abindex가 가리키는 숫자들 다 sample에 넣음 정렬해야함
	{
		sample[i + k] = dn[n][aindex].number[k];
		sample[i + 1 + k] = dn[n][bindex].number[k];
	}
	for (i = 0; i < (n + 1) * 2 - 1; i++) // 버블정렬
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
			temp[0].num[i] = sample[i];// 바로 temp에 넣음
		}

		return 1; // 비어있거나 같은게 없다면 1 반환.
	}

	// nnn[n+1]이 0보다 크다면 PI가 있는지 없는지 비교하고 넣음. (비교 방법은 각수의 제곱값의 합을 해쉬값으로 정함)
	
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

		if (sumT == sumS) return 0; // 같은수가 하나라도 있으면 거른다.
	}

	// 같은수가 없다면 temp에 저장
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
	printf("숫자가 존재하는 모든 열의 count가 2 이상이므로 Cyclic 입니다.\n");
	printf("PI 선택 과정입니다.\n");
	for (i = 0; i < 8; i++)
	{
		if (width[i].count == 1)
		{
			wlTemp[a++] = i;
			tc++;
		}
	}

	// 행에서 하나짜리 걸러냄
	for (i = 0; i < c; i++)
	{
		for (j = 0; j < tc; j++)
		{
			if (table[i][wlTemp[j]] == 1) // 하나짜리가 있는 행을 찾았으면
			{
				length[i].ischeck = 1;
				cpi++;
				ep++;
				for (k = 0; k < 8; k++) // 그행에 있는 모든 1의 세로열을 0으로 소거한다.
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
	printf("EPI는 %d개 입니다.\n\n",ep);


	// 비교숫자를 +1칸으로 지정해서 비교시작*
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
	// 큰반복문 필요함
	while (max != 0)
	{
		// 이 행을 사용할것이므로 이 행은 1로 초기화
		length[imax].ischeck = 1;
		cpi++;
		for (j = 0; j < 8; j++)
		{
			//table[imax][j]가 1인건 모두 0으로 바꾼다
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
	printf("Cyclic 시행완료\n");
	//큰반복문 닫음

	for (i = 0; i < c; i++)
	{
		if (length[i].ischeck == 1)
		{
			strcat(cyclic, length[i].name);
			if (cpi-- > 1) strcat(cyclic, "+");
		}
	}
	printf("F = %s를 결과값에 저장하였습니다.\n", cyclic);
}

void dupTable(struct wid *width, struct leng *length, int **table, int *prtable, int c, int max, int imax, int cpi, char *cyclic)
{
	int i, j, k, l;
	printf("여기서 해를 선택할 수 있습니다.\n");
	printTable(width, length, table, prtable, c, -1);
	// width count가 2이상이 하나만 있을때
	// 배열 복사해서 출력

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
		//table[imax][j]가 1인건 모두 0으로 바꾼다
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

	printf("선택항 시행완료\n");
	//큰반복문 닫음
	printf("F = %s를 결과값에 저장하였습니다.\n\n다른경우\n", cyclic);
}