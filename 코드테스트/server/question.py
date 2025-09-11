class Questions:
    que =[
     
####################################################################
#print
#"""----------------- 01  -----------------"""
        {
        'section':"출력문",
        'ques':[
                '1. print를 사용하세요', 
        ],
        'hint':[
                "print('안녕하세요')",
        ],
        'bonus':30,
        'input':[],
        'answ_in':None,
        'answ':['hello'], 
        'nused':[],
        'must':['print'],
        'correct':[
                "print('hello')",
        ]
        },
        
#"""----------------- 02  -----------------"""
        {
        'section':"출력문",
        'ques':[ 
                '1. print를 사용하세요',  
        ],
        'hint':[
                "print('안녕하세요')",
        ],
        'bonus':30,
        'input':[],  
        'answ_in':None,
        'answ':['import random'],
        'nused':[],
        'must':['print'],
        'correct':[
                "print('import random')",
        ]
        },
        
#"""----------------- 03  -----------------"""
        {
        'section':"출력문",
        'ques':[  
                '1. print를 사용하세요',  
        ],
        'hint':[
                "print('안녕하세요')",
        ],
        'bonus':30,
        'input':[],  
        'answ_in':None,
        'answ':['com = random.randint(0,100)'],
        'nused':[],
        'must':['print'],
        'correct':[
                "print('com = random.randint(0,100)')",
        ]
        },
        
#"""----------------- 04  -----------------"""
        {
        'section':"출력문",
        'ques':[
                '1. print를 사용하세요',  
        ],
        'hint':[
                "print('안녕하세요')",
        ],
        'bonus':30,
        'input':[],  
        'answ_in':None,
        'answ':['import pygame'],
        'nused':[],
        'must':['print'],
        'correct':[
                "print('import pygame')",
        ]
        },
        
#"""----------------- 05  -----------------"""
        {
        'section':"출력문",
        'ques':[ 
                '1. print를 사용하세요',
        ],
        'hint':[
                "print('안녕하세요')",
        ],
        'bonus':30,
        'input':[],  
        'answ_in':None,
        'answ':['pygame.init()'],
        'nused':[],
        'must':['print'],
        'correct':[
                "print('pygame.init()')",
        ]
        },
        
#"""----------------- 06  -----------------"""
        {
        'section':"출력문",
        'ques':[
                '1. print를 사용하세요',
        ],
        'hint':[
                "print('안녕하세요')",
        ],
        'bonus':30,
        'input':[],  
        'answ_in':None,
        'answ':['while True:'],
        'nused':[],
        'must':['print'],
        'correct':[
                "print('while True:')",
        ]
        },
        
#"""----------------- 07  -----------------"""
        {
        'section':"출력문",
        'ques':[  
                '1. print를 사용하세요',
        ],
        'hint':[
                "print('안녕하세요')",
        ],
        'bonus':30,
        'input':[],  
        'answ_in':None,
        'answ':['if a > b:'],
        'nused':[],
        'must':['print'],
        'correct':[
                "print('if a > b:')",
        ]
        },
        
#"""----------------- 08  -----------------"""
        {
        'section':"출력문",
        'ques':[  
                '1. print를 사용하세요',
        ],
        'hint':[
                "print('안녕하세요')",
        ],
        'bonus':30,
        'input':[],  
        'answ_in':None,
        'answ':['for i in range(5):'],
        'nused':[],
        'must':['print'],
        'correct':[
                "print('for i in range(5):')",
        ]
        },
        
#"""----------------- 09  -----------------"""
        {
        'section':"출력문",
        'ques':[ 
                '1. print를 사용하세요',
        ],
        'hint':[
                "print('안녕하세요')",
        ],
        'bonus':30,
        'input':[],  
        'answ_in':None,
        'answ':['class Game:'],
        'nused':[],
        'must':['print'],
        'correct':[
                "print('class Game:')",
        ]
        },
        
#"""----------------- 10  -----------------"""
        {
        'section':"출력문",
        'ques':[
                '1. print를 사용하세요',
        ],
        'hint':[
                "print('안녕하세요')",
        ],
        'bonus':30,
        'input':[],  
        'answ_in':None,
        'answ':['def __init__(self):'],
        'nused':[],
        'must':['print'],
        'correct':[
                "print('def __init__(self):')",
        ]
        },
####################################################################
#변수          

#"""----------------- 11  -----------------"""
        {
        'section':"변수",
        'ques':[
                '1. a 변수를 선언하고',
                '\t5을 넣고',
                '\ta의 값을 출력하세요',
                '2. print를 사용하세요',
        ],
        'hint':[
                "a = 10",
                "print(a)",
        ],
        'bonus':40,
        'input':[],    
        'answ_in':None, 
        'answ':[5],
        'nused':[],
        'must':[['print(a)',"print(f\'{a}\')",'print(f\"{a}\")'],'a'],
        'correct':[
                "a = 5",
                "print(a)",
        ]
        },
#"""----------------- 12  -----------------"""
        {
        'section':"변수",
        'ques':[
                '1. a 변수를 선언하고',
                '\thello 문자열을 넣고',
                '\ta의 값을 출력하세요',
                '2. print를 사용하세요',
        ],
        'hint':[
                "print(a)",
        ],
        'bonus':40,
        'input':[],    
        'answ_in':None, 
        'answ':['hello'],
        'nused':[],
        'must':[['print(a)',"print(f\'{a}\')",'print(f\"{a}\")'],'a'],
        'correct':[
                "a = 'hello'",
                "print(a)",
        ]
        },
#"""----------------- 13  -----------------"""
        {
        'section':"변수",
        'ques':[
                '1. a 변수를 선언하고',
                '\tTrue 를 넣고',
                '\ta의 값을 출력하세요',
                '\tTrue는 문자열이 아닙니다.',
                '2. print를 사용하세요',
        ],
        'hint':[
                "print(a)",
        ],
        'bonus':40,
        'input':[],    
        'answ_in':None, 
        'answ':[True],
        'nused':['\'True\'','\"True\"'],
        'must':[['print(a)',"print(f\'{a}\')",'print(f\"{a}\")'],'a'],
        'correct':[
                "a = True",
                "print(a)",
        ]
        },
#"""----------------- 14  -----------------"""
        {
        'section':"변수",
        'ques':[
                '1. a 변수를 선언하고',
                '\t8/4의 값을 넣고',
                '\ta의 값을 출력하세요',
                '2. print를 사용하세요',
        ],
        'hint':[
                "print(a)",
        ],
        'bonus':40,
        'input':[],    
        'answ_in':None, 
        'answ':[2.0],
        'nused':['2.0'],
        'must':[['print(a)',"print(f\'{a}\')",'print(f\"{a}\")'],'a','/','8','4'],
        'correct':[
                "a = 8/4",
                "print(a)",
        ]
        },
#"""----------------- 15  -----------------"""
        {
        'section':"변수",
        'ques':[
                '1. a 변수를 선언하고',
                '\t8+4의 값을 넣고',
                '\ta의 값을 출력하세요',
                '2. print를 사용하세요',
        ],
        'hint':[
                "print(a)",
        ],
        'bonus':40,
        'input':[],    
        'answ_in':None, 
        'answ':[12],
        'nused':['12'],
        'must':[['print(a)',"print(f\'{a}\')",'print(f\"{a}\")'],'a','+','8','4'],
        'correct':[
                "a = 8+4",
                "print(a)",
        ]
        },
#"""----------------- 16  -----------------"""
        {
        'section':"변수",
        'ques':[
                '1. a 변수를 선언하고',
                '\t8-2의 값을 넣고',
                '\ta의 값을 출력하세요',
                '2. print를 사용하세요',
        ],
        'hint':[
                "print(a)",
        ],
        'bonus':40,
        'input':[],    
        'answ_in':None, 
        'answ':[6],
        'nused':['6'],
        'must':[['print(a)',"print(f\'{a}\')",'print(f\"{a}\")'],'a','-','8','2'],
        'correct':[
                "a = 8-2",
                "print(a)",
        ]
        },
#"""----------------- 17  -----------------"""
        {
        'section':"변수",
        'ques':[
                '1. a 변수를 선언하고',
                '\t8*2의 값을 넣고',
                '\ta의 값을 출력하세요',
                '2. print를 사용하세요',
        ],
        'hint':[
                "print(a)",
        ],
        'bonus':40,
        'input':[],    
        'answ_in':None, 
        'answ':[16],
        'nused':['16'],
        'must':[['print(a)',"print(f\'{a}\')",'print(f\"{a}\")'],'a','*','8','2'],
        'correct':[
                "a = 8*2",
                "print(a)",
        ]
        },
#"""----------------- 18  -----------------"""
        {
        'section':"변수",
        'ques':[
                '1. a 변수를 선언하고',
                '\t10을 a에 넣고',
                '\t5를 증가하고',
                '\ta의 값을 출력하세요',
                '2. print를 사용하세요',
                '3. += 을 사용하세요',
        ],
        'hint':[
                "a += 1",
                "print(a)",
        ],
        'bonus':40,
        'input':[],    
        'answ_in':None, 
        'answ':[15],
        'nused':['15'],
        'must':[['print(a)',"print(f\'{a}\')",'print(f\"{a}\")'],'a','+=','10','5'],
        'correct':[
                "a = 10",
                "a += 5",
                "print(a)",
        ]
        },
#"""----------------- 19  -----------------"""
        {
        'section':"변수",
        'ques':[
                '1. a 변수를 선언하고',
                '\t10을 넣고',
                '\ta를 아래와 같이 출력하세요.',
                '2. print를 사용하세요',
                "\tf'a = {}' 를 사용하세요.",
        ],
        'hint':[
                "a = 10",
                "print(f'a{a}')",
        ],
        'bonus':40,
        'input':[],    
        'answ_in':None, 
        'answ':['a = 10'],
        'nused':[],
        'must':['print','f','{a'],
        'correct':[
                "a = 10",
                "print(f'a = {a}')",
        ]
        },

#"""----------------- 20  -----------------"""
        {
        'section':"변수",
        'ques':[
                '1. 변수 a와 b를 선언하고',
                '    아래와 같이 출력하세요.',
                '2. print를 사용하세요',
        ],
        'hint':[
                "f'a = {}' 를 사용하세요.",
        ],
        'bonus':40,
        'input':[],     
                'answ_in':None,
                'answ':[
                "a = 3, b = 5",
        ],
        'nused':[],
        'must':['print','f','{a','{b'],
        'correct':[
                "a = 3",
                "b = 5",
                "print(f'a={a},b={b}')",
        ]
        },
####################################################################
#연산
#"""----------------- 21  -----------------"""
        {
        'section':"연산",
        'ques':[
                '1. print와 +를 사용하세요',
                '2. 변수 a b c를 모두 사용하세요',  
        ],
        'hint':[
                "a = 1",
                "b = 1",                   
                "c = a + b",
                "print(c)",
        ],
        'bonus':40,
        'input':[],  
        'answ_in':None,
        'answ':[6],
        'nused':[],
        'must':['print','+','a','b','c'],
        'correct':[
                "a =3",
                "b =3",
                "c=a+b",
                "print(c)",
        ]
        },

#"""----------------- 22  -----------------"""
        {
        'section':"연산",
        'ques':[
                '1. print와 -를 사용하세요',
                '2. 변수 a b c를 모두 사용하세요',
        ],
        'hint':[
        ],
        'bonus':40,
        'input':[],  
        'answ_in':None,
        'answ':[8],
        'nused':[],
        'must':['print','-','a','b','c'],
        'correct':[
                "a = 12",
                "b = 4",
                "c = a -b",
                "print(c)",
        ]
        },

#"""----------------- 23  -----------------"""
        {
        'section':"연산",
        'ques':[
                '1. print와 *를 사용하세요',
                '2. 변수 a b c를 모두 사용하세요',
        ],
        'hint':[
        ],
        'bonus':40,
        'input':[],  
        'answ_in':None,
        'answ':[16],
        'nused':[],
        'must':['print','*','a','b','c'],
        'correct':[
                "a = 4",
                "b = 4",
                "c = a * b",
                "print(c)",
        ]
        },

#"""----------------- 24  -----------------"""
        {
        'section':"연산",
        'ques':[
                '1. print와 /를 사용하세요',
                '2. 변수 a b c를 모두 사용하세요',
        ],
        'hint':[
        ],

        'bonus':40,
        'input':[],  
        'answ_in':None,
        'answ':[4.0],
        'nused':[],
        'must':['print','/','a','b','c'],
        'correct':[
                "a = 8",
                "b = 2",
                "c = a/b",
                "print(c)",
        ]
        },

####################################################################   
#input
#"""----------------- 25  -----------------"""
        {
        'section':"입력",
        'ques':[
                '1. print를 사용하세요',
                '2. input을 사용해서 이름을 입력 받습니다.',
                "3. f' {}' 를 사용하세요.",
        ],
        'hint':[
                'name = input("이름 : ")',
                'print(name)',
        ],
        'bonus':40,

        'input':[['철수'],['영희']],     
        'answ_in':[              
                ['이름 : 철수'],
                ['이름 : 영희'],
        ],
        'answ':['안녕하세요, 철수님!','안녕하세요, 영희님!'],
        'nused':[],
        'must':['print','f','{'],
        'correct':[
                "name = input('이름 : ')",
                "print(f'안녕하세요, {name}님!')",
        ]
        },

#"""----------------- 26  -----------------"""
        {
        'section':"입력",
        'ques':[
                '1. print를 사용하세요',
                '2. input을 사용해서 나이를 입력 받습니다.',
                "3. f' {}' 를 사용하세요.",
        ],
        'hint':[
                'age = input("나이 : ")',
                'print(age)',
        ],
        'bonus':40,

        'input':[['12'],['20']],     
        'answ_in':[              
                ['나이 : 12'],
                ['나이 : 20'],
        ],
        'answ':['나이는 12세입니다.','나이는 20세입니다.'],
        'nused':[],
        'must':['print','f','{'],
        'correct':[
                "age = input('나이 : ')",
                "print(f'나이는 {age}세입니다.')",
        ]
        },

#"""----------------- 27  -----------------"""
        {
        'section':"입력",
        'ques':[
                '1. input을 사용해서 a와 b를 입력 받습니다.',
                '2. 입력된 값의 합을 구해서 출력하세요.',
                "3. f' {}' 를 사용하세요.",
        ],
        'hint':[
                'a = input("첫번째:")',
                'b = input("두번째:")',
                'a = int(a)',
                'b = int(b)',
        ],
        'bonus':40,
        'input':[['3','4'],['5','3']],   
        'answ_in':[              
                ['첫번째 : 3','두번째 : 4'],
                ['첫번째 : 4','두번째 : 4'],
        ],
        'answ':['두수의 합은 7입니다.','두수의 합은 8입니다.'],
        'nused':[],
        'must':['print','f','{','int'],
        'correct':[
                "a = input('첫번째:')",
                "b = input('두번째:')",
                "a = int(a)",
                "b = int(b)",
                "c = a + b",
                "print(f'두수의 합은 {c}입니다.')",
        ]
        },

#"""----------------- 28  -----------------"""
        {
        'section':"입력",
        'ques':[
                '1. input을 사용해서 a와 b를 입력 받습니다.',
                '2. 입력된 값의 차을 구해서 출력하세요.',
                "3. f' {}' 를 사용하세요.", 
        ],
        'hint':[
                'a = input("첫번째:")',
                'b = input("두번째:")',
        ],
        'bonus':40,

        'input':[['3','4'],['5','7']],  
        'answ_in':[              
                ['첫번째 : 3','두번째 : 4'],
                ['첫번째 : 5','두번째 : 7'],
        ], 
        'answ':['결과: 3 - 4 = -1','결과: 5 - 7 = -2'],
        'nused':[],
        'must':['print','f','{','int'],
        'correct':[
                "a = input('첫번째:')",
                "b = input('두번째:')",
                "a = int(a)",
                "b = int(b)",
                "c = a - b",
                "print(f'결과: {a} - {b} = {c}')",
        ]
        },

#"""----------------- 29  -----------------"""
        {
        'section':"입력",
        'ques':[
                '1. input을 사용해서 a와 b를 입력 받습니다.',
                '2. 입력된 값의 차을 구해서 출력하세요.',
                "3. f' {}' 를 사용하세요.",
        ],
        'hint':[
                'a = input("첫번째:")',
                'b = input("두번째:")',
        ],
        'bonus':40,

        'input':[['3','4'],['5','7']],   
        'answ_in':[              
                ['첫번째 : 3','두번째 : 4'],
                ['첫번째 : 5','두번째 : 7'],
        ], 
        'answ':['결과: 3 * 4 = 12','결과: 5 * 7 = 35'],
        'nused':[],
        'must':['print','f','{', 'int'],
        'correct':[
                "a = input('첫번째:')",
                "b = input('두번째:')",
                "a = int(a)",
                "b = int(b)",
                "c = a * b",
                "print(f'결과: {a} * {b} = {c}')",
        ]
        },

#"""----------------- 30  -----------------"""
        {
        'section':"입력",
        'ques':[
                '1. input을 사용해서 입력받은 문자열을 s에 저장하세요.',
                '2. 입력된 문자열의 길이를 구해서 출력하세요.',
                "3. f' {}' 를 사용하세요.",
        ],
        'hint':[
                's = input("문자열 입력:")',
                'len 함수를 사용하면 문자열의 길이를 구할 수 있습니다.',
        ],
        'bonus':40,

        'input':[['hello'],['codingnow']],      
        'answ_in':[              
                ['문자열 입력 :hello'],
                ['문자열 입력 :codingnow'],
        ], 
        'answ':['문자열 길이 = 5','문자열 길이 = 9'],
        'nused':[],
        'must':['print','f','{', 'len'],
        'correct':[
                "s = input('문자열 입력:')",
                "print(f'문자열 길이 = {len(s)}')",
        ]
        },
####################################################################   
#조건문   

#"""----------------- 31  -----------------"""
        {
        'section':"조건문",
        'ques':[
                '1. a 변수에 3을 넣고',
                '2. b 변수에 4을 넣고',
                "3. 어느 변수가 큰지 출력하세요",
                '4. if를 사용하세요', 
                
        ],
        'hint':[
                'a = 3',    
                'b = 1',
                'if a == b:',
                '\tprint("같다")',
                'else:',
                '\tprint("다르다")',
        ],
        'bonus':40,
        'input':[],   
        'answ_in':None, 
        'answ':['b가크다'],
        'nused':[],
        'must':['print','a=3','b=4','if',['else','elif'],'a가크다'],
        'correct':[
                "a = 3",
                "b = 4",
                "if a > b:",
                "\tprint('a가크다')",
                "else:",
                "\tprint('b가크다')",
        ]
        },

#"""----------------- 32  -----------------"""
        {
        'section':"조건문",
        'ques':[
                '1. a 변수에 4을 넣고',
                '2. b 변수에 3을 넣고',
                "3. 어느 변수가 큰지 출력하세요",
                '4. if를 사용하세요', 
                
        ],
        'hint':[
                'a = 3',    
                'b = 1',
                'if a == b:',
                '\tprint("같다")',
        ],
        'bonus':40,
        'input':[],   
        'answ_in':None, 
        'answ':['a가크거나 같다'],
        'nused':[],
        'must':['print','a=4','b=3','if','>='],
        'correct':[
                "a = 4",
                "b = 3",
                "if a >= b:",
                "\tprint('a가크거나 같다')",
        ]
        },
#"""----------------- 33  -----------------"""
        {
        'section':"조건문",
        'ques':[
                '1. input을 사용해서 입력받은 숫자가',
                '\t60이상이면 PASS, 아니면 FAIL을 출력하세요.',
                '2. if를 사용하세요', 
                '3. 잘못된 조건식을 고쳐야해요',
        ],
        'hint':[
                'score = int(input("입력:"))',    
                'if score > 60:',
                '\tprint("??")',
                'else:',
                '\tprint("??")',
        ],
        'bonus':40,
        'input':[['85'],['60'],['59']],   
        'answ_in':[              
                ['입력 : 85'],
                ['입력 : 60'],
                ['입력 : 59'],
        ], 
        'answ':['PASS', 'PASS', 'FAIL'],
        'nused':[],
        'must':['print','input','if','else'],
        'correct':[
                "score = int(input('입력:'))",
                "if score >= 60:",
                "\tprint('PASS')",
                "else:",
                "\tprint('FAIL')",
        ]
        },

#"""----------------- 34  -----------------"""
        {
        'section':"조건문",
        'ques':[
                '1. input을 사용해서 입력받은 숫자가',
                '\t20세 이상이면 성인, 아니면 미성년자를 출력하세요.',
                '2. if를 사용하세요', 
                '3. 잘못된 조건식을 고쳐야해요',
        ],
        'hint':[
                "age = int(input('입력:'))",    
                'if age < 20:',
                '\tprint("성인")',
                'else:',
                '\tprint("미성년자")',
        ],
        'bonus':40,

        'input':[['17'],['20'],['21']],  
        'answ_in':[              
                ['입력 : 17'],
                ['입력 : 20'],
                ['입력 : 21'],
        ], 
        'answ':['미성년자', '성인', '성인'],
        'nused':[],
        'must':['print','input','if','else'],
        'correct':[
                "age = int(input('입력:'))",
                "if age >= 20:",
                "\tprint('성인')",
                "else:",
                "\tprint('미성년자')",
        ]
        },

#"""----------------- 35  -----------------"""
        {
        'section':"조건문",
        'ques':[
                '1. 점수를 입력받아 등급을 출력하는 프로그램',
                '\t90 이상: A',
                '\t80 이상: B',
                '\t70 이상: C',
                '\t60 이상: D',
                '\t그 외: F',
        ],
        'hint':[
                "#elif는 조건 우선순위가 있습니다.",
                "",
                "score = int(input('입력 : '))",    
                "if score > 50:",
                "\tprint('aaa')",
                "elif score > 40:",
                "\tprint('bbb')",
                "else:",
                "\tprint('ccc')",
        ],
        'bonus':40,

        'input':[['78'],['90'],['71'],['60'],['50']],  
        'answ_in':[              
                ['입력 : 78'],
                ['입력 : 90'],
                ['입력 : 71'],
                ['입력 : 60'],
                ['입력 : 50'],
        ], 
        'answ':['C','A','C','D','F'],
        'nused':[],
        'must':['print','input','if','else'],
        'correct':[
                "score = int(input('입력 : '))",
                "if score >= 90:",
                "\tprint('A')",
                "elif score >= 80:",
                "\tprint('B')",
                "elif score >= 70:",
                "\tprint('C')",
                "elif score >= 60:",
                "\tprint('D')",
                "else:",
                "\tprint('F')",
        ]
        },

#"""----------------- 36  -----------------"""
        {
        'section':"조건문",
        'ques':[
                '1. 두 개의 숫자를 입력받아 더 큰 수를 출력하는 프로그램',
        ],
        'hint':[
                "a = int(input('입력1 :'))",    
                "b = int(input('입력2 :'))",
        ],
        'bonus':40,

        'input':[['10','15'],['90','80']],
        'answ_in':[              
                ['입력1 :10','입력2 :14'],
                ['입력1 :90','입력2 :80'],
        ], 
        'answ':['큰수 : 15','큰수 : 90'],
        'nused':[],
        'must':['print','input','if'],
        'correct':[
                "a = int(input('입력1 :'))",
                "b = int(input('입력2 :'))",
                "if a > b:",
                "\tprint(f'큰수 : {a}')",
                "else:",
                "\tprint(f'큰수 : {b}')",
        ]
        },

#"""----------------- 37  -----------------"""
        {
        'section':"조건문",
        'ques':[
                '1. input을 사용해서 입력받은 숫자가 짝수인지 홀수인지 판단하세요.',
                '2. if를 사용하세요',
        ],
        'hint':[
                '#% 연산자를 사용하면 나머지를 구할 수 있습니다.',    
                'n = int(input("정수입력 : "))',    
                'a = n % 2',
                'print(a)',
        ],
        'bonus':40,

        'input':[[7],[2]],  
        'answ_in':[              
                ['정수입력 : 7'],
                ['정수입력 : 2'],
        ], 
        'answ':['홀수', '짝수'],
        'nused':[],
        'must':['print','input','if','%'],
        'correct':[
                "n = int(input('정수입력 : '))",
                "a = n % 2",
                "if a == 0:",
                "\tprint('짝수')",
                "else:",
                "\tprint('홀수')",
        ]
        },

#"""----------------- 38  -----------------"""
        {
        'section':"조건문",
        'ques':[
                '1. 성별(남 또는 여)을 입력받아 남자 또는 여자로 출력하는 프로그램',
        ],
        'hint':[
                "gender = input('입력 :')",    
        ],
        'bonus':40,

        'input':[['남'],['여']],  
        'answ_in':[              
                ['입력 :남'],
                ['입력 :여'],
        ], 
        'answ':['남자','여자'],
        'nused':[],
        'must':['print','input','if'],
        'correct':[
                "gender = input('입력 :')",
                "if gender == '남':",
                "\tprint('남자')",
                "else:",
                "\tprint('여자')",
        ]
        },


#"""----------------- 39  -----------------"""
        {
        'section':"조건문",
        'ques':[
                '1. 세 개의 숫자를 입력받아 가장 큰 수를 출력하는 프로그램',
                '\t힌트 조건식을 완료해 보세요',
        ],
        'hint':[
                "a = int(input('입력1 :'))",    
                "b = int(input('입력2 :'))",   
                "c = int(input('입력3 :'))",  

                "if a > b and a > c:",  
                "\tprint('a가 제일크다')",  
                "elif b > a and b > c:",  
                "\tprint('b가 제일크다')",  
        ],
        'bonus':40,

        'input':[['10','15','20'],['90','80','70'],['5','3','4']],  
        'answ_in':[              
                ['입력1 : 10','입력2 : 15','입력3 : 20'], 
                ['입력1 : 90','입력2 : 80','입력3 : 70'], 
                ['입력1 : 5','입력2 : 3','입력3 : 4'], 
        ], 
        'answ':['20', '90', '5'],
        'nused':[],
        'must':['print','input','if', 'and'],
        'correct':[
                "a = int(input('입력1 :'))",
                "b = int(input('입력2 :'))",
                "c = int(input('입력3 :'))",
                "if a > b and a > c:",
                "\tprint(a)",
                "elif b > a and b > c:",
                "\tprint(b)",
                "elif c > a and c > b:",
                "\tprint(c)",
        ]
        },

#"""----------------- 40  -----------------"""
        {
        'section':"조건문",
        'ques':[
                '1. 월(숫자)을 입력받아 계절을 출력하는 프로그램',
                '\t3~5월: 봄',
                '\t6~8월: 여름',
                '\t9~11월: 가을',
                '\t12, 1, 2월: 겨울',
        ],
        'hint':[
                "month = int(input('입력 : '))",    
                "if 3 <= month and month <= 5:",   
                "\tprint('봄')",  
        ],
        'bonus':40,

        'input':[['1'],['9'],['6'],['12']],  
        'answ_in':[              
                ['1'], 
                ['9'], 
                ['6'], 
                ['12'], 
        ], 
        'answ':['겨울', '가을', '여름', '겨울'],
        'nused':[],
        'must':['print','input','if', 'and'],
        'correct':[
                "month = int(input('입력 : '))",
                "if 3 <= month and month <= 5:",
                "\tprint('봄')",
                "elif 6 <= month and month <= 8:",
                "\tprint('여름')",
                "elif 9 <= month and month <= 11:",
                "\tprint('가을')",
                "else:",
                "\tprint('겨울')",
        ]
        },
####################################################################   
#반복문     
#"""----------------- 41  -----------------"""
        {
        'section':"반복문",
        'ques':[
                '1. for를 사용하세요',
                '2. range를 사용하세요',    
        ],
        'hint':[
                '#range(중지):',    
                'for i in range(10):',
                '\tprint(i)', 
        ],
        'bonus':40,

        'input':[],  
        'answ_in':None,
        'answ':[0,1,2,3,4],
        'nused':[],
        'must':['print','for','range'],
        'correct':[
                "for i in range(5):",
                "\tprint(i)",
        ]
        },
#"""----------------- 42  -----------------"""
        {
        'section':"반복문",
        'ques':[
                '1. for를 사용하세요',
                '2. range를 사용하세요',    
        ],
        'hint':[
                '#range(시작, 중지):',  
                'for i in range(10):',
                '\tprint(i)', 
        ],
        'bonus':40,

        'input':[],  
        'answ_in':None,
        'answ':[1,2,3,4,5],
        'nused':[],
        'must':['print','for','range'],
        'correct':[
                "for i in range(1,10):",
                "\tprint(i)",
        ]
        },

#"""----------------- 43  -----------------"""
        {
        'section':"반복문",
        'ques':[
                '1. for를 사용하세요',
                '2. range를 사용하세요',
                '3. 2 씩 증가한 값을 출력',
        ],
        'hint':[
                'range(시작, 중지, 증가):',   
        ],
        'bonus':40,

        'input':[],  
        'answ_in':None,
        'answ':[2,4,6,8],
        'nused':[],
        'must':['print','for'],
        'correct':[
                "for i in range(2,10,2):",
                "\tprint(i)",
        ]
        },

#"""----------------- 44  -----------------"""
        {
        'section':"반복문",
        'ques':[
                '1. for를 사용하세요',
                '2. range를 사용하세요',  
        ],
        'hint':[
                'range(시작, 중지, 증가):',   
        ],
        'bonus':40,

        'input':[],  
        'answ_in':None,
        'answ':[5,4,3,2,1],
        'nused':[],
        'must':['print','for'],
        'correct':[
                "for i in range(5,0,-1):",
                "\tprint(i)",
        ]
        },


#"""----------------- 45  -----------------"""
        {
        'section':"반복문",
        'ques':[
                '1. 반복 문자열을 5번 출력',
                '2. for를 사용하세요',
        ],
        'hint':[
                'for i in range(5):',   
                "\tprint(i)",
        ],
        'bonus':40,

        'input':[],  
        'answ_in':None,
        'answ':['반복','반복','반복','반복','반복'],
        'nused':[],
        'must':['print','for'],
        'correct':[
                "for i in range(5):",
                "\tprint('반복')",
        ]
        },

#"""----------------- 46  -----------------"""
        {
        'section':"반복문",
        'ques':[
                '1. 반복 문자열을 3번 출력',
                '2. 3번 이후는 숫자 출력',
                '3. for를 사용하세요',
        ],
        'hint':[
                'for i in range(5):',   
                "\tprint(i)",
        ],
        'bonus':40,

        'input':[],  
        'answ_in':None,
        'answ':['반복','반복','반복',3,4],
        'nused':[],
        'must':['print(i)',["print('반복')",'print("반복")'],'for','if','else'],
        'correct':[
                "for i in range(5):",
                "\tif i < 3:",
                "\t\tprint('반복')",
                "\telse:",
                "\t\tprint(i)",
        ]
        },


#"""----------------- 47  -----------------"""
        {
        'section':"반복문",
        'ques':[
                '1. 2를 4번 더한 값을 구하세요.',
                '\t 2 + 2 + 2 + 2',
                '2. for를 사용하세요',
                '3. total 변수를 사용하여 값을 구하세요',
        ],
        'hint':[
                "#1을 6번 더한 값 출력",
                'total = 0',   
                'for i in range(6):',
                '\ttotal += 1',    
                'print(total)', 
        ],
        'bonus':40,

        'input':[],  
        'answ_in':None,
        'answ':[8],
        'nused':['8'],
        'must':['print','for','+=','total'],
        'correct':[
                "total = 0",
                "for i in range(4):",
                "\ttotal += 2",
                "print(total)",
        ]
        },
        
#"""----------------- 48  -----------------"""
        {
        'section':"반복문",
        'ques':[
                '1. 1부터 5까지의 모든 수의 합을 구하세요',
                '2. for를 사용하세요',
                '3. total 변수를 사용하여 값을 구하세요',
        ],
        'hint':[
                'total = 0',   
                'for i in range(1, 3):',
                '\ttotal += 1',    
                'print(total)', 
        ],
        'bonus':40,

        'input':[],  
        'answ_in':None,
        'answ':[15],
        'nused':['15'],
        'must':['print(total)','for','+=','total'],
        'correct':[
                "total = 0",
                "for i in range(1, 6):",
                "\ttotal += i",
                "print(total)",
        ]
        },

#"""----------------- 49  -----------------"""
        {
        'section':"반복문",
        'ques':[
                '1. for를 사용하세요',
                '2. range를 사용하세요',
                "3. f'{}' 를 사용하세요.",
        ],
        'hint':[
                'for i in range(5):',
                '\tprint(i)',    
        ],
        'bonus':40,

        'input':[],  
        'answ_in':None,
        'answ':['1x2=2','2x2=4','3x2=6','4x2=8','5x2=10','6x2=12','7x2=14','8x2=16','9x2=18'],
        'nused':[],
        'must':['print','for','f','{'],
        'correct':[
                "for i in range(1,10):",
                "\tprint(f'{i}x2={i*2}')",
        ]
        },


#"""----------------- 50  -----------------"""
        {
        'section':"반복문",
        'ques':[
                '1. input을 사용하세요',
                '2. for를 사용하세요',
                "3. f'{}' 를 사용하세요.",
        ],
        'hint':[
                'dan = int(input("출력할 구구단 단수를 입력하세요: "))',    
                'for i in range(5):',
                '\tprint(i)', 
        ],
        'bonus':40,

        'input':[['7'],['6']],  
        'answ_in':[
                ['출력할 구구단 단수를 입력하세요: 7'],
                ['출력할 구구단 단수를 입력하세요: 6'],
        ],
        'answ':[
                [
                '7 x 1 = 7',
                '7 x 2 = 14',
                '7 x 3 = 21',
                '7 x 4 = 28',
                '7 x 5 = 35',
                '7 x 6 = 42',
                '7 x 7 = 49',
                '7 x 8 = 56',
                '7 x 9 = 63'
                ],
                [
                '6 x 1 = 6',
                '6 x 2 = 12',
                '6 x 3 = 18',
                '6 x 4 = 24',
                '6 x 5 = 30',
                '6 x 6 = 36',
                '6 x 7 = 42',
                '6 x 8 = 48',
                '6 x 9 = 54'
                ],
        ],
        'nused':[],
        'must':['print','for','f','{'],
        'correct':[
                "dan = int(input('출력할 구구단 단수를 입력하세요: '))",
                "for i in range(1,10):",
                "\tprint(f'{dan}x{i}={dan*i}')",
        ]
        },
        
####################################################################   
#리스트

#"""----------------- 51  -----------------"""

        {
        'section':"리스트",
        'ques':[
                '문제 : 리스트 [블로그:31번]', 
                '사과, 바나나, 오렌지가 저장된 리스트를 생성하고 출력하는 프로그램',
        ],
        'hint':[
                "#리스트는 ['사과', '바나나', '오렌지'] ",
                "lst = ['a','b']",   
                'print(lst)',  
        ],
        'bonus':40,

        'answ_in':None,
        'input':[],  
        'answ':["['사과', '바나나', '오렌지']"],
        'nused':[],
        'must':['print'],
        'correct':[
                "lst = ['사과', '바나나', '오렌지'] ",
                "print(lst)",
        ]
        },

#"""----------------- 52  -----------------"""

        {
        'section':"리스트",
        'ques':[
                '리스트에 새로운 요소를 추가한 후 결과를 출력하는 프로그램',
                'append( )를 사용하세요.',
        ],
        'hint':[
                "lst = ['사과', '바나나', '오렌지']",   
                'print(lst)',   
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["['사과', '바나나', '오렌지', '포도']"],
        'nused':[],
        'must':['print','append'],
        'correct':[
                "lst = ['사과', '바나나', '오렌지']",
                "lst.append('포도')",
                "print(lst)",
        ]
        },


#"""----------------- 53  -----------------"""
        {
        'section':"리스트",
        'ques':[ 
                '리스트에서 특정 요소를 제거한 후 결과를 출력하는 프로그램',
                '바나나를 모두 삭제하세요.',
                'remove( )를 사용하세요.',
        ],
        'hint':[  
                "lst = ['사과', '바나나', '오렌지', '바나나']",   
                'print(lst)',  
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["['사과', '오렌지']"],
        'nused':[],
        'must':['print','remove'],
        'correct':[
                "lst = ['사과', '바나나', '오렌지', '바나나']",
                "lst.remove('바나나')",
                "lst.remove('바나나')",
                "print(lst)",
        ]
        },


#"""----------------- 54  -----------------"""
        {
        'section':"리스트",
        'ques':[
                '리스트의 길이(요소 개수)를 출력하는 프로그램',
                'len(lst)를 사용하세요.',
        ],
        'hint':[
                "lst = ['사과', '오렌지', '바나나']",   
                'print(lst)', 
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["리스트의 길이 : 3"],
        'nused':[],
        'must':['print','len'],
        'correct':[
                "lst = ['사과', '오렌지', '바나나']",
                "print(f'리스트의 길이 : {len(lst)}')",
        ]
        },

#"""----------------- 55  -----------------"""
        {
        'section':"리스트",
        'ques':[
                '리스트의 두 번째 요소를 출력하는 프로그램',
                '인덱싱으로 lst[0]을 사용합니다.',
        ],
        'hint':[
                "lst = ['사과', '오렌지', '포도']",   
                'print(lst)',  
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["오렌지"],
        'nused':[],
        'must':['print','[1]'],
        'correct':[
                "lst = ['사과', '오렌지', '포도']",
                "print(lst[1])",
        ]
        },

#"""----------------- 56  -----------------"""
        {
        'section':"리스트",
        'ques':[
                '리스트의 모든 요소를 순회하면서 출력하는 프로그램',
                'for x in lst:',
                '\tprint(x)',
                '형태로 작성합니다.',
        ],
        'hint':[
                "lst = ['사과', '오렌지', '포도']",   
                'print(lst)',    
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["사과","오렌지","포도"],
        'nused':[],
        'must':['print','for'],
        'correct':[
                "lst = ['사과', '오렌지', '포도']",
                "for x in lst:",
                "\tprint(x)",
        ]
        },

#"""----------------- 57  -----------------"""
        {
        'section':"리스트",
        'ques':[
                '리스트의 모든 숫자를 더한 합계를 출력하는 프로그램',
                'sum(lst) 함수를 사용',

        ],
        'hint':[
        "nums = [1, 2, 3, 4, 5]",   
        'print(nums)',   
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["15"],
        'nused':[],
        'must':['print','sum'],
        'correct':[
                "nums = [1, 2, 3, 4, 5]",
                "print(sum(nums))",
        ]
        },

#"""----------------- 58  -----------------"""
        {
        'section':"리스트",
        'ques':[
                '리스트의 최댓값과 최솟값을 구하여 출력하는 프로그램',
                'max(lst), min(lst) 함수를 사용',
        ],
        'hint':[
        "nums = [10, 3, 7, 1, 5]",   
        'print(nums)',   
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["10","1"],
        'nused':[],
        'must':['print','min','max'],
        'correct':[
                "nums = [10, 3, 7, 1, 5]",
                "print(max(nums))",
                "print(min(nums))",
        ]
        },

#"""----------------- 59  -----------------"""
        {
        'section':"리스트",
        'ques':[
                '리스트를 오름차순으로 정렬하여 출력하는 프로그램',
                'lst.sort() 함수를 사용',
        ],
        'hint':[
        "nums = [4, 1, 3, 5, 2]",   
        'print(nums)',   
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["[1, 2, 3, 4, 5]"],
        'nused':[],
        'must':['print','sort'],
        'correct':[
                "nums = [4, 1, 3, 5, 2]",
                "nums.sort()",
                "print(nums)",
        ]
        },

#"""----------------- 60  -----------------"""
        {
        'section':"리스트",
        'ques':[
                '리스트를 내림차순으로 정렬하여 출력하는 프로그램',
                'lst.sort(reverse=True) 함수를 사용',

        ],
        'hint':[
                "nums = [4, 1, 3, 5, 2]",   
                'print(nums)',   
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["[5, 4, 3, 2, 1]"],
        'nused':[],
        'must':['print','sort(reverse=True)'],
        'correct':[
                "nums = [4, 1, 3, 5, 2]",
                "nums.sort(reverse=True)",
                "print(nums)",
        ]
        },
        
####################################################################
#딕셔너리

#"""----------------- 61  -----------------"""
        {
        'section':"딕셔너리",
        'ques':[
                '다음과 같은 학생 점수를 저장하는 딕셔너리를 만들어 출력하세요.',
                '키(강감찬)와 값(78)을 추가합니다.',
        ],
        'hint':[
                "scores = {'홍길동': 85, '이순신': 92}",   
                'print(scores)',    
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["{'홍길동': 85, '이순신': 92, '강감찬': 78}"],
        'nused':[],
        'must':['print'],
        'correct':[
                "scores = {'홍길동': 85, '이순신': 92, '강감찬': 78}",
                "print(scores)",
        ]
        },

#"""----------------- 62  -----------------"""
        {
        'section':"딕셔너리",
        'ques':[
                '딕셔너리에서 이순신의 점수를 출력하세요.',
                '딕셔너리의 값은 키를 사용해서 가져옵니다.',
                "키 홍길동을 사용하여 값을 가져오면 score['홍길동']",
                '85를 가져옵니다.',
        ],
        'hint':[
                "scores = {'홍길동': 85, '이순신': 92, '강감찬': 78}",   
                "print(scores['홍길동'])",    
        ],
        'bonus':40,

        'input':[],  
        'answ_in':None,
        'answ':["이순신 점수 : 92"],
        'nused':[],
        'must':['print',["['이순신']",'["이순신"]']],
        'correct':[
                "scores = {'홍길동': 85, '이순신': 92, '강감찬': 78}",
                "print(f\"이순신 점수 : {scores['이순신']}\")",
        ]
        },

#"""----------------- 63  -----------------"""
        {
        'section':"딕셔너리",
        'ques':[
                '딕셔너리에 유관순: 88 을 추가하고 출력하세요.',
                '초기값이 아닌 코드 실행중에 값을 넣을 때는',
                "새로운 키 '김코딩' 에 값을 넣으면 추가됩니다.",
                "scores['김코딩'] = 87",
        ],
        'hint':[
                "scores = {'홍길동': 85, '이순신': 92, '강감찬': 78}",   
                'print(scores)',  
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["{'홍길동': 85, '이순신': 92, '강감찬': 78, '유관순': 88}"],
        'nused':[],
        'must':['print',["['유관순']",'["유관순"]']],
        'correct':[
                "scores = {'홍길동': 85, '이순신': 92, '강감찬': 78}",
                "scores['유관순'] = 88",
                "print(scores)",
        ]
        },

#"""----------------- 64  -----------------"""
        {
        'section':"딕셔너리",
        'ques':[
                '딕셔너리에서 홍길동을 삭제한 후 출력하세요.',
                '딕셔너리에서 키를 사용하여 삭제하려면 del 사용합니다.',
                "del scores['키']",
        ],
        'hint':[
                "scores = {'홍길동': 85, '이순신': 92, '강감찬': 78, '유관순': 88}",   
                'print(scores)',    
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["{'이순신': 92, '강감찬': 78, '유관순': 88}"],
        'nused':[],
        'must':['print','del'],
        'correct':[
                "scores = {'홍길동': 85, '이순신': 92, '강감찬': 78, '유관순': 88}",
                "del scores['홍길동']",
                "print(scores)",
        ]
        },

#"""----------------- 65  -----------------"""
        {
        'section':"딕셔너리",
        'ques':[
                '딕셔너리에서 점수만 모두 출력하세요.',
                'values() 확인 해 봅니다.',
                "list에서 배운 list의 합을 구해 출력합니다. sum( )",
        ],
        'hint':[
                "scores = {'이순신': 92, '강감찬': 78, '유관순': 88}",   
                'print(scores.values()) # dict_values',    
                'a = list(scores.values()) #리스트로 변환',    
                'print(a)',    
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["[92, 78, 88]","합 : 258"],
        'nused':[],
        'must':['print','list','values()','sum'],
        'correct':[
                "scores = {'이순신': 92, '강감찬': 78, '유관순': 88}",
                "a = list(scores.values()) ",
                "print(a)",
                "print('합:',sum(a))",
        ]
        },

#"""----------------- 66  -----------------"""
        {
        'section':"딕셔너리",
        'ques':[
                '딕셔너리에서 학생 이름만 모두 출력하세요.',
                'keys() 확인 해 봅니다.',
                "list로 변환해서 출력 합니다.",
        ],
        'hint':[
                "scores = {'이순신': 92, '강감찬': 78, '유관순': 88}",    
                'print(scores.keys())', 
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["['이순신', '강감찬', '유관순']"],
        'nused':[],
        'must':['print','list','keys()'],
        'correct':[
                "scores = {'이순신': 92, '강감찬': 78, '유관순': 88}",
                "keys = list(scores.keys())",
                "print(keys)",
        ]
        },

#"""----------------- 67  -----------------"""
        {
        'section':"딕셔너리",
        'ques':[
                '딕셔너리에 저장된 학생 수(항목 개수)를 출력하세요.',
                'len 함수 사용',
                "list와 동일하게 len 함수를 사용하여 딕셔너리의 항목 개수를 구할 수 있습니다.",
        ],
        'hint':[
                "scores = {'이순신': 92, '강감찬': 78, '유관순': 88}",    
                'length = ???',    
                'print(length)',  
        ],
        'bonus':40,
        'answ_in':None,

        'input':[],  
        'answ':["3"],
        'nused':[],
        'must':['print','len'],
        'correct':[
                "scores = {'이순신': 92, '강감찬': 78, '유관순': 88}",
                "length = len(scores)",
                "print(length)",
        ]},
#"""----------------- 68  -----------------"""
        {
        'section':"딕셔너리",
        'ques':[
                '학생들의 평균 점수를 계산해서 출력하세요.',
                '딕셔너리의 모든 값을 score.values() 리스트로 가져오고 합을 구합니다. sum()',
                "딕셔너리의 항목 수를 가져옵니다. len()",
        ],
        'hint':[
        "scores = {'이순신': 92, '강감찬': 78, '유관순': 88}",    
        "print('평균점수')",  
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["평균 점수: 86.0"],
        'nused':[],
        'must':['print','len','sum','values'],
        'correct':[
                "scores = {'이순신': 92, '강감찬': 78, '유관순': 88}",
                "avr = sum(scores.values()) / len(scores)",
                "print('평균점수:',avr)",
        ]
        },

#"""----------------- 69  -----------------"""
        {
        'section':"딕셔너리",
        'ques':[
                '80점 이상인 학생의 이름과 점수를 출력하세요.',
                'items를 사용하면 각 항목을 튜플로 가져옵니다.',
                "조건문을 활용하여 80점 이상인 학생을 구분해 봅니다.",
        ],
        'hint':[
                "scores = {'이순신': 92, '강감찬': 78, '유관순': 88}",
                "for i in scores.items():",
                "\tprint(i)",
                "",
                "for name, score in scores.items():",
                "\tprint(f'{name} {score}')",
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["이순신: 92","유관순: 88"],
        'nused':[],
        'must':['print','items','if'],
        'correct':[
                "scores = {'이순신': 92, '강감찬': 78, '유관순': 88}",
                "",
                "for name, score in scores.items():",
                "\tif score >= 80:",
                "\t\tprint(f'{name} : {score}')",
        ]
        },

#"""----------------- 70  -----------------"""
        {
        'section':"딕셔너리",
        'ques':[
                '사용자로부터 이름을 입력받아 해당 학생의 점수를 출력하세요.',
                "학생이 없으면 '해당 학생이 없습니다.'를 출력하세요.",
                "in을 사용하면 딕셔너리에 키가 있는지 확인 할 수 있습니다.",
        ],
        'hint':[
                "scores = {'이순신': 92, '강감찬': 78, '유관순': 88}",

                "name = input('이름을 입력하세요: ')",
                "if name in scores:",
                "\tprint(f'score에 있습니다.')",   
        ],
        'bonus':40,
        'answ_in':[
                ['이름을 입력하세요: 강감찬'],
                ['이름을 입력하세요: 김유신']
        ],
        'input':[['강감찬'],['김유신']],  
        'answ':["강감찬의 점수는 78점입니다.","해당 학생이 없습니다."],
        'nused':[],
        'must':['print','input','if','in'],
        'correct':[
                "scores = {'이순신': 92, '강감찬': 78, '유관순': 88}",
                "name = input('이름을 입력하세요: ')",
                "",
                "if name in scores:",
                "\tprint(f'{name}의 점수는 {scores[name]}점입니다.')",
                "else:",
                "\tprint('해당 학생이 없습니다.')",
        ]
        },
        
####################################################################   
#함수

#"""----------------- 71  -----------------"""

        {
        'section':"함수",
        'ques':[
                "두 수를 입력받아 합계를 반환하는 함수를 완성하세요.",
        ],
        'hint':[
                "def add(a, b):",
                "\tc = 0",
                "\treturn c",
                "",
                "num1 = int(input('첫번째:'))",
                "num2 = int(input('두번째:'))",
                "",
                "result = add(3,5)",
                "print(result)",
        ],
        'bonus':40,
        'answ_in':[
                ["첫번째: 4","두번째: 6"],
                ["첫번째: 3","두번째: 4"]
        ],

        'input':[['4','6'],['3','4']],  
        'answ':["두수의 합 : 10","두수의 합 : 7"],
        'nused':['num1+num2'],
        'must':['print','input','def','add','num1','num2'],
        'correct':[
                "def add(a, b):",
                "\tc = a + b",
                "\treturn c",
                "num1 = int(input('첫번째:'))",
                "num2 = int(input('두번째:'))",
                "result = add(num1,num2)",
                "print('두수의 합 : ',result)",
        ]
        },

#"""----------------- 72  -----------------"""
        {
        'section':"함수",
        'ques':[
                "두 수를 입력받아 차를 반환하는 함수를 완성하세요.",
        ],
        'hint':[
                "def sub(a, b):",
                "\tpass",
                "",
                "num1 = int(input('첫번째:'))",
                "num2 = int(input('두번째:'))",
                "",
                "print(result)",
        ],
        'bonus':40,
        'answ_in':[
                ["첫번째: 4","두번째: 6"],
                ["첫번째: 3","두번째: 4"]
        ],
        'input':[['4','6'],['3','4']],  
        'answ':["두수의 차 : -2","두수의 차 : -1"],
        'nused':['num1-num2'],
        'must':['print','input','def','num1','num2'],
        'correct':[
                "def sub(a, b):",
                "\tc = a - b",
                "\treturn c",
                "num1 = int(input('첫번째:'))",
                "num2 = int(input('두번째:'))",
                "result = sub(num1,num2)",
                "print('두수의 차 : ',result)",
        ]
        },

#"""----------------- 73  -----------------"""
        {
        'section':"함수",
        'ques':[
                "두 수를 입력받아 곱을 반환하는 함수를 완성하세요.",                   
        ],
        'hint':[
                "num1 = int(input('첫번째:'))",
                "num2 = int(input('두번째:'))",
                "",
                "print(result)",
        ],
        'bonus':40,
        'answ_in':[
                ["첫번째: 4","두번째: 6"],
                ["첫번째: 3","두번째: 4"]
        ],
        'input':[['4','6'],['3','4']],  
        'answ':["두수의 곱 : 24","두수의 곱 : 12"],
        'nused':['num1*num2'],
        'must':['print','input','def','num1','num2'],
        'correct':[
                "def mul(a, b):",
                "\tc = a * b",
                "\treturn c",
                "num1 = int(input('첫번째:'))",
                "num2 = int(input('두번째:'))",
                "result = mul(num1,num2)",
                "print('두수의 곱 : ',result)",
        ]
        },

#"""----------------- 74  -----------------"""
        {
        'section':"함수",
        'ques':[
                "두 수를 입력받아 나눈값을 반환하는 함수를 완성하세요.",
        ],
        'hint':[
                "num1 = int(input('첫번째:'))",
                "num2 = int(input('두번째:'))",
                "",
                "print(result)",
        ],
        'bonus':40,
        'answ_in':[
                ["첫번째: 4","두번째: 2"],
                ["첫번째: 8","두번째: 2"]
        ],
        'input':[['4','2'],['8','2']],  
        'answ':["두수의 나눈값 : 2.0","두수의 나눈값 : 4.0"],
        'nused':['num1/num2'],
        'must':['print','input','def','num1','num2'],
        'correct':[
                "def div(a, b):",
                "\tc = a / b",
                "\treturn c",
                "num1 = int(input('첫번째:'))",
                "num2 = int(input('두번째:'))",
                "result = div(num1,num2)",
                "print('두수의 나눈값 : ',result)",
        ]
        },

#"""----------------- 75  -----------------"""
        {
        'section':"함수",
        'ques':[
                "리스트를 입력받아 그 평균을 반환하는 함수를 완성하세요.",
        ],
        'hint':[
                "def average(lst):",
                "\tresult = lst",
                "\treturn result ",
                "",
                "values = [10, 20, 30]",
                "avr = average(values)",

                "print('평균 : ',avr)",
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["평균 : 20.0"],
        'nused':['num1/num2'],
        'must':['print','def','sum'],
        'correct':[
                "def average(lst):",
                "\tresult = sum(lst)/len(lst)",
                "\treturn result ",
                "values = [10, 20, 30]",
                "avr = average(values)",
                "print('평균 : ',avr)",
        ]
        },
        
####################################################################   
#함수

#"""----------------- 76  -----------------"""
        {
        'section':"클래스",
        'ques':[
                "생성자(__init__)만 있는 Calculator 클래스를 생성하세요.",
                "",
                "실행결과는 없습니다.",
                "힌트 코드의 문제 점을 수정하세요.",
        ],
        'hint':[
                "class Calculator:",
                "\tdef init(): #<생성자에 문제 해결!!",
                "\t\tpass",
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':[],
        'nused':[],
        'must':['def','class Calculator:','def __init__','(self):'],
        'correct':[
                "class Calculator:",
                "\tdef __init__(self):",
                "\t\tpass",
        ]
        },

#"""----------------- 77  -----------------"""
        {
        'section':"클래스",
        'ques':[
                "생성자(__init__)만 있는 Student 클래스를 생성하세요.",
                "",
                "실행결과는 없습니다.",
        ],
        'hint':[
                "class Calculator:",
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':[],
        'nused':[],
        'must':['def','class Student:','def __init__','(self):'],
        'correct':[
                "class Student:",
                "\tdef __init__(self):",
                "\t\tpass",
        ]
        },
#"""----------------- 78  -----------------"""
        {
        'section':"클래스",
        'ques':[
                "Calculator 클래스를 생성하고",
                "\tadd 함수 클래스에 추가",
                "",
                "두개의 정수를 입력받아",
                "add 함수를 호출하여 두 수의 합을 출력하세요.",
        ],
        'hint':[
                "class Calculator:",
                "\tdef add(self,a,b):",
                "\t\tpass",
                "",
                "num1 = int(input('첫번째:'))",
                "num2 = int(input('두번째:'))",
                "cal = Calculator()",
                "print(cal.add(3,4))",
        ],
        'bonus':40,
        'answ_in':None,
        'input':[['3','4'],['6','3']],  
        'answ':["합 : 7","합 : 9"],
        'nused':[],
        'must':['print','class Calculator:','input','def add(self,', 'cal.add'],
        'correct':[
                "class Calculator:",
                "\tdef add(self,a,b):",
                "\t\treturn a+b",
                "",
                "num1 = int(input('첫번째:'))",
                "num2 = int(input('두번째:'))",
                "cal = Calculator()",
                "print('합 : ',cal.add(num1,num2))",
        ]
        },

#"""----------------- 79  -----------------"""
        {
        'section':"클래스",
        'ques':[
                "힌트 코드를 사용해서",
                "greet( ) 함수를 완성하세요.",
        ],
        'hint':[
                "class Person:",
                "\tdef __init__(self, name, age):",
                "\t\tself.name = name",
                "\t\tself.age = age",
                "",
                "\tdef greet(self):",
                "\t\tpass",
                "",
                "",
                "p1 = Person('코딩', 19)",
                "p1.greet()",
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["이름:코딩, 나이:19"],
        'nused':[],
        'must':['print','class Person:','{self.name}','{self.age}', 'p1.greet()'],
        'correct':[
                "class Person:",
                "\tdef __init__(self, name, age):",
                "\t\tself.name = name",
                "\t\tself.age = age",
                "",
                "\tdef greet(self):",
                "\t\tprint(f'이름:{self.name}, 나이:{self.age}')",
                "",
                "",
                "p1 = Person('코딩', 19)",
                "p1.greet()",
        ]
        },

#"""----------------- 80  -----------------"""
        {
        'section':"클래스",
        'ques':[
                "힌트 코드를 사용해서",
                "greet( ) 함수 없이 이름과 나이를 출력하세요.",
                "클래스 변수 p1을 사용하면 ",
                "self로 선언한 변수를 접근 할 수 있어요 ",
        ],
        'hint':[
                "class Person:",
                "\tdef __init__(self, name, age):",
                "\t\tself.name = name",
                "\t\tself.age = age",
                "",
                "",
                "p1 = Person('코딩', 19)",
                "print(f'{p1.name})'",
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["이름:코딩, 나이:19"],
        'nused':['greet()'],
        'must':['print','class Person:','{p1.name}','{p1.age}'],
        'correct':[
                "class Person:",
                "\tdef __init__(self, name, age):",
                "\t\tself.name = name",
                "\t\tself.age = age",
                "",
                "",
                "p1 = Person('코딩', 19)",
                "print(f'이름:{p1.name}, 나이:{p1.age}')",
        ]
        },

#"""----------------- 81  -----------------"""
        {
        'section':"클래스",
        'ques':[
                "힌트 코드를 사용해서",
                "가로3, 세로5 사각형의 넓이를 구합니다.",
                "클래스의 area를 사용 ",
        ],
        'hint':[
                "class Rectangle:",
                "\tdef __init__(self, width, height):",
                "\t\tpass",
                "",
                "\tdef area(self):#넓이",
                "\t\tpass",
                "",
                "",
                "width = 3",
                "height = 5",
                "#클래스 생성",
                "",
                "#area 함수 호출해서 결과값 받아오기",
        ],
        'bonus':40,
        'answ_in':None,
        'input':[],  
        'answ':["직사각형의 넓이 : 15"],
        'nused':['width*height','width * height'],
        'must':['print','class Rectangle:','self.width','self.height' ,'self.width * self.height'],
        'correct':[
                "class Rectangle:",
                "\tdef __init__(self, width, height):",
                "\t\tself.width = width",
                "\t\tself.height = height",
                "",
                "\tdef area(self):#넓이",
                "\t\treturn self.width * self.height",
                "",
                "",
                "width = 3",
                "height = 5",
                "r = Rectangle(width, height)",
                "",
                "area = r.area()",
                "print(f'직사각형의 넓이 : ',area)",
        ]
        },
####################################################################   
#"""----------------- 79  -----------------"""

        {
        'section':"완료",
        'ques':[
        "완료했습니다.",
        ],
        'hint':[],    
        'bonus':40,
        'answ_in':None,     
        'input':[],  
        'answ':[],
        'nused':[],
        'must':[],
        'correct':[
                
        ]
        },
    ]