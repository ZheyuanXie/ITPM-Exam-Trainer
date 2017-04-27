#coding:utf-8
import json
import random

class question:
    def __init__(self,s):
        j = json.loads(s)
        self.category = j['category']
        self.id = j['id']
        self.answer = j['answer']
        self.content = j['content']
        self.choiceA = j['A']
        self.choiceB = j['B']
        self.choiceC = j['C']
        self.choiceD = j['D']
        self.answerNum = 0
        self.answerList = [False,False,False,False,False,False]
        self.answerNum = len(self.answer)
        for a in list(self.answer):
            a0 = ord(a.upper()) - 65
            self.answerList[a0] = True
        self.shufflechoice()

    def display(self):
        print '----------------C%02dQ%02d--------------------'%(self.category,self.id)
        print self.content
        print 'A.',self.choiceA
        print 'B.',self.choiceB
        print 'C.',self.choiceC
        print 'D.',self.choiceD
        print '------------------------------------------'
        # print self.answerNum
        # print self.answerList

    def shufflechoice(self):
        choices = [[self.choiceA,self.answerList[0]],[self.choiceB,self.answerList[1]], [self.choiceC,self.answerList[2]], [self.choiceD,self.answerList[3]]]
        random.shuffle(choices)
        self.answerList[0] = choices[0][1]
        self.answerList[1] = choices[1][1]
        self.answerList[2] = choices[2][1]
        self.answerList[3] = choices[3][1]
        self.choiceA = choices[0][0]
        self.choiceB = choices[1][0]
        self.choiceC = choices[2][0]
        self.choiceD = choices[3][0]
        self.answer = ''
        for i in range(len(self.answerList)):
            if self.answerList[i] == True:
                self.answer = self.answer + chr(i+65)

    def checkans(self, userans):
        try:
            useransList = [False,False,False,False,False,False]
            for a in list(userans):
                a0 = ord(a.upper()) - 65
                useransList[a0] = True
            #print useransList
            #print self.answerList
            for i in range(6):
                if useransList[i] != self.answerList[i]:
                    return False
        except:
            return  False
        return True

class questionbook():
    def __init__(self):
        self.qlist = [[] for i in range(9)]  # 9 chapter
        self.load()

    def load(self):
        for l in self.qlist:
            l[:] = []
        f = open('questions.txt','r')
        content = f.readlines()
        for line in content:
            j = json.loads(line)
            q = question(line)
            self.qlist[j['category']-1].append(q)
        f.close()

    def add(self,q):
        f = open('questions.txt','a')
        f.write(q)
        f.write('\n')
        f.close()

    def useradd(self):
        try:
            category = int(raw_input('Catagory > '))
            id = int(raw_input('id > '))
            if category < 1 or category > 9:
                print 'Category Out Of Range'
                return
        except:
            print 'Illegal Input'
            return
        for q in self.qlist[category-1]:
            if int(q.id) == int(id):
                print '该题号已存在!'
                q.display
                return
        content = raw_input('Content > ')
        choiceA = raw_input('A > ')
        choiceB = raw_input('B > ')
        choiceC = raw_input('C > ')
        choiceD = raw_input('D > ')
        answer = raw_input('answer > ')
        dict = {'category':category,'id':id,'content':content,'answer':answer,'A':choiceA,'B':choiceB,'C':choiceC,'D':choiceD}
        self.add(json.dumps(dict))
        self.load()

    def sequential(self):
        print '开始顺序出题'
        for cat in self.qlist:
            for q in cat:
                q.display()
                ans = raw_input('请输入答案：')
                if q.checkans(ans):
                    print '正确! '
                else:
                    print '错误! 答案是',q.answer
                raw_input('press enter to continue...')
        print '\n--End--'

    def chapter(self):
        try:
            cha = raw_input('Chapter 选择章节 >')
            cha = int(cha)
            if cha > 9 or cha < 1:
                print 'Invalid 无效章节'
                return
        except:
            print 'Invalid 无效输入'
            return
        exampaper = []
        cnt = 0
        for q in self.qlist[cha-1]:
            exampaper.append(q)
            cnt += 1
        random.shuffle(exampaper)
        print 'Total Question 题量：%d' % cnt
        icnt = 0
        correct = 0
        wrong = 0
        errorlist = []
        for q in exampaper:
            q.display()
            ans = raw_input('YOUR ANSWER：')
            if ans == 'q':
                print 'QUITTING EXERCISE ...'
                return
            if q.checkans(ans):
                print '\033[0;32m'
                print 'CORRECT！'
                print '\033[0m'
                correct += 1
            else:
                print '\033[0;31m'
                print 'WRONG! THE ANSWER IS', q.answer
                print '\033[0m'
                errorlist.append(q)
                wrong += 1
            icnt += 1
            raw_input('PROGRESS:(%d/%d), Press ENTER to continue ...' % (icnt, cnt))
        print '~~~~~~~~~~~~~EXERCISE RESULT~~~~~~~~~~~'
        print 'Your score: %.2f(%d/%d)' % (100 * (float(correct) / (correct + wrong)), correct, correct + wrong)
        raw_input('press enter to show error list...')
        print '~~~~~~~~~~~~ERROR LIST~~~~~~~~~~~~~'
        for q in errorlist:
            q.display()
            print 'Answer:', q.answer

    def listall(self):
        try:
            cha = raw_input('Chapter 选择章节 >')
            cha = int(cha)
            if cha > 9 or cha < 1:
                print 'Out Of Range 无此章节'
                return
        except:
            print 'Invalid 无效输入'
            return
        for q in self.qlist[cha - 1]:
            q.display()

    def exam(self):
        exampaper = []
        cnt = 0
        for cha in self.qlist:
            for q in cha:
                exampaper.append(q)
                cnt += 1
        random.shuffle(exampaper)
        print 'Total available 题库题量：%d'%cnt
        try:
            num = raw_input('Total number of questions 模拟考试出题数>')
            num = int(num)
            if num > cnt or num < 1:
                print 'Out Of Range'
                return
        except:
            print 'Invalid Input'
            return
        icnt = 0
        correct = 0
        wrong = 0
        errorlist = []
        for q in exampaper:
            if icnt >= num:
                break
            q.display()
            ans = raw_input('YOUR ANSWER：')
            if ans == 'q':
                print 'QUITTING EXAM ...'
                return
            if q.checkans(ans):
                print '\033[0;32m'
                print 'CORRECT！'
                print '\033[0m'
                correct += 1
            else:
                print '\033[0;31m'
                print 'WRONG! THE ANSWER IS', q.answer
                print '\033[0m'
                errorlist.append(q)
                wrong += 1
            icnt += 1
            raw_input('PROGRESS:(%d/%d), Press ENTER to continue ...'%(icnt,num))
        print '~~~~~~~~~~~~~EXAM RESULT~~~~~~~~~~~'
        print 'Your score: %.2f(%d/%d)'%(100*(float(correct)/(correct+wrong)),correct,correct+wrong)
        raw_input('press enter to show error list...')
        print '~~~~~~~~~~~~ERROR LIST~~~~~~~~~~~~~'
        for q in errorlist:
            q.display()
            print 'Answer:',q.answer

def displayMenu():
    print '----------Menu 菜单---------'
    #print 'a - add a question 新增题'
    #print '# f - find a question 按题号寻找'
    #print 'l - list all question 列出所有题'
    #print 's - by sequence 顺序出题'
    print 'c - by chapter 按章节训练'
    print 'e - exam simulation 模拟考试'
    print 'h - display menu 显示菜单'
    print 'q - quit 退出'
    print '-----------------------'
    print '\033[0m'

if __name__ == '__main__':
    qb = questionbook()
    displayMenu()
    while 1:
        cmd = raw_input('\nMain Menu Option >')
        if cmd == 'q':
            quit()
        elif cmd == 'a':
            qb.useradd()
        elif cmd == 'l':
            qb.listall()
        elif cmd == 'h':
            displayMenu()
        elif cmd== 's':
            qb.sequential()
        elif cmd == 'c':
            qb.chapter()
        elif cmd == 'e':
            qb.exam()
        else:
            print 'invalid 无效命令'

