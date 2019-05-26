import re
import pandas as pd
class LexicalAnalysis:
    def __init__(self,file):
        self.fp = file
        
    #def for create switchState state
    def switchState(self, state ,*argv):
        return getattr(self, 'state_' + str(state))(*argv)
        
    def state_0(self):
        char = self.fp.nextChar()
        if char == 'eof':
            print("'<eof>'")
        elif char == '<':
            return LexicalAnalysis.switchState(self,1)
        elif char == '=':
            return LexicalAnalysis.switchState(self,5)
        elif char == '>':
            return LexicalAnalysis.switchState(self,6)
        elif char == ' ':
            return LexicalAnalysis.switchState(self,22)
        elif char == ';':
            return LexicalAnalysis.switchState(self,25)
        elif re.search('[A-Z]|[a-z]',char):
            return LexicalAnalysis.switchState(self,9,char)
        
    def state_1(self):
        char = self.fp.nextChar()
        if char == 'eof':
            print("'<relop,LE>'")
            print("'<eof>'")
        elif char == '=':
            return LexicalAnalysis.switchState(self,2)
        elif char == '>':
            return LexicalAnalysis.switchState(self,3)
        else:
            return LexicalAnalysis.switchState(self,4)
        
    def state_2(self):
        print("'<relop,LE>'")
        return LexicalAnalysis.switchState(self,0)
    
    def state_3(self):
        print("'<relop,NE>'")
        return LexicalAnalysis.switchState(self,0)
        
    def state_4(self):
        self.fp.previousChar()
        print("'<relop,LT>'")
        return LexicalAnalysis.switchState(self,0)
        
    def state_5(self):
        print("'<relop,EQ>'")
        return LexicalAnalysis.switchState(self,0)
    
    def state_6(self):
        char = self.fp.nextChar()
        if char == 'eof':
            print("'<eof>'")
        elif char == '=':
            return LexicalAnalysis.switchState(self,7)
        else:
            return LexicalAnalysis.switchState(self,8)
    
    def state_7(self):
        print("'<relop,GE>''")
        return LexicalAnalysis.switchState(self,0)
    
    def state_8(self):
        self.fp.previousChar()
        print("'<relop,GT>'")
        return LexicalAnalysis.switchState(self,0)

    def checkKeyword(self):
        string = self.identifiers
        tokenDataFrame = pd.read_csv('token.csv',index_col=0)
        for item,value in tokenDataFrame.iterrows():
            if value['tokenName'] == 'keyword' and value['attributeValue'] == string:
                return value['id']
    
    def state_9(self,*argv):
        if argv:
            self.identifiers = argv[0]
        char = self.fp.nextChar()
        if char == 'eof':
            if LexicalAnalysis.checkKeyword(self):
                print("'<keyword,{}>'".format(self.identifiers))
            else:
                print("'<identifiers,{}>'".format(self.identifiers))
            print("'<eof>'")
        elif re.search('[A-Z]|[a-z]|[0-9]',char):
            self.identifiers = self.identifiers + char
            return LexicalAnalysis.switchState(self,9)
        else:
            self.fp.previousChar()
            if LexicalAnalysis.checkKeyword(self):
                print("'<keyword,{}>'".format(self.identifiers))
            else:
                print("'<identifiers,{}>'".format(self.identifiers))
            return LexicalAnalysis.switchState(self,0)
    
    def state_22(self):
        char = self.fp.nextChar()
        if char == 'eof':
            print("'<delim>'")
            print("'<eof>'")
        elif char == ' ':
            return LexicalAnalysis.switchState(self,22)
        else:
            print("'<delim>'")
            self.fp.previousChar()
            return LexicalAnalysis.switchState(self,0)
    
    def state_25(self):
        char = self.fp.nextChar()
        if char == 'eof':
            print("'<punctuation,semicolon>'")
            print("'<eof>'")
        else:
            print("'<punctuation,semicolon>'")
            self.fp.previousChar()
            return LexicalAnalysis.switchState(self,0)
