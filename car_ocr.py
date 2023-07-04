import easyocr
import re

def recognition(file):
    reader = easyocr.Reader(['ko'],) # 'en': 영어로 설정
    result = reader.readtext(file) 
    temp=[]

    #1차 가공
    for i in result:
        if any(c.isdigit() for c in i[1]) and len(i[1])>=3:
            temp.append(i[1])
    for i in range(0,len(temp)):
        temp[i]=re.sub(r"[^\uAC00-\uD7A30-9]", "", temp[i])  
    for i in range(0,len(temp)):
        #길이가 3 미만일 때
        if len(temp[i])<3:
            temp[i]=''
        
        #숫자개수가 2개 미만일 때
        cnt=0
        for j in temp[i]:
            if j.isdigit():
                cnt+=1
        if cnt<2:
            temp[i]=''

    while '' in temp:
        temp.remove('')
    print(temp)

    #2차 가공
    if len(temp)>=2 and 3<=len(temp[0]) and len(temp[1])>=4:
        if len(temp[0])>4:
            temp[0]=temp[0][len(temp[0])-4:len(temp[0])]
        if len(temp[1])>4:
            temp[1]=temp[1][0:4]
        print(temp)
        temp[0]+=temp[1]
        del temp[1]
        print(temp)

    judge_list="가,나,다,라,마,거,너,더,러,머,버,서,어,저,고,노,도,로,모,보,소,오,조,구,누,두,루,무,부,수,우,주,아,바,사,자,배,허,하,호"



    flag=[False,False]
    #차량번호판 형식 판별
    def judge(temp,flag):
    #정상적으로 판별되었을 경우
        for i in temp:
            if len(i)>=7:
                word=list(i)
                if flag[0]==False:
                    for index in range(0,len(word)-6):
                        #12가3456 형식
                        if word[index].isdigit() and word[index+1].isdigit() and word[index+2].isdigit()==False and \
                        word[index+3].isdigit() and word[index+4].isdigit() and word[index+5].isdigit() and word[index+6].isdigit():
                            if word[index+2]!=' ' and int(i[index:index+2])<=669 and word[index+2] in judge_list:
                                flag[0]=True
                                return i[index:index+8]

                        #123가3456 형식
                        elif word[index].isdigit() and word[index+1].isdigit() and word[index+2].isdigit() and word[index+3].isdigit()==False and\
                        word[index+4].isdigit() and word[index+5].isdigit() and word[index+6].isdigit() and word[index+7].isdigit():
                            if word[index+3]!=' ' and int(i[index:index+3])<=669 and word[index+3] in judge_list:     
                                flag[0]=True
                                return i[index:index+9]
                else:
                    break
        #차량 용도 글자 부분이 숫자로 인식되었을 때
        if flag[0]==False:
            for i in range(0,len(temp)):
                #12'가'3456 형식
                if len(temp[i])==7 and temp[i][2]=='7':
                    temp[i]=temp[i][0:2]+'가'+temp[i][3:8]
                    flag[1]=True
                #12'나'3456 형식   
                elif len(temp[i])==7 and temp[i][2]=='4':
                    temp[i]=temp[i][0:2]+'나'+temp[i][3:8]
                    flag[1]=True
                #123'다'4567 형식  
                elif len(temp[i])==8 and temp[i][3]=='7':
                    temp[i]=temp[i][0:3]+'가'+temp[i][4:8]
                    flag[1]=True
                #123'나'4567 형식   
                elif len(temp[i])==8 and temp[i][3]=='4':
                    temp[i]=temp[i][0:3]+'나'+temp[i][4:8]
                    flag[1]=True
            if flag[1]==False:
                return "!에러!"
            else:
                return judge(temp,flag)
        
            
    result=judge(temp,flag)
    return result


