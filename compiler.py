INT = 'INT'
MUL = 'MUL'
DIV = 'DIV'
ADD = 'ADD'
SUB = 'SUB'
LBRAC = 'LBRAC'
RBRAC = 'RBRAC'
EOF = 'EOF'

#Used to store tokens
class token:
	def __init__(self, type, value):
		self.type = type
		self.value = value

#Helps in classifying the input stream in the form of tokens
class lexer:
	def __init__(self, stream):
		self.stream = stream
		self.pos = 0
		self.char = self.stream[0]

	#Used to obtain the next token from the stream
	def next_token(self):

		#Return the token that the current character represents
		if self.char == None:
			result = token(EOF, '$')
		elif self.char == " ":
			self.pos += 1

			if(self.pos > len(self.stream) - 1) :
				self.char = None
			else:
				self.char = self.stream[self.pos]
			return self.next_token()
		
		elif self.char == '+':
			result = token(ADD, self.char)

		elif self.char == '*':
			result = token(MUL, self.char)

		elif self.char == '/':
			result = token(DIV, self.char)

		elif self.char == '-':
			result = token(SUB, self.char)

		elif self.char == '(':
			result = token(LBRAC, self.char)

		elif self.char == ')':
			result = token(RBRAC, self.char)

		elif(self.char.isdigit()):
			integer = self.char
			while((self.pos < len(self.stream)-1) and self.stream[self.pos + 1].isdigit() ):
				self.pos+=1
				self.char = self.stream[self.pos]
				integer += self.char
			result = token(INT, int(integer))
		#Error if the current character does not fall into any of the tokens
		else:
			raise Exception("Syntax is invalid")

		#Change current character to next character
		self.pos += 1

		if(self.pos > len(self.stream) - 1) :
			self.char = None
		else:
			self.char = self.stream[self.pos]

		return result

	#Convert the input stream to a list of tokens
	def tokenize(self):
		token_stream = []
		while(self.char != None):
			token_stream.append(self.next_token())
		token_stream.append(self.next_token())
		return token_stream


class parser:
	def __init__(self, token_stream):
		self.token_stream = token_stream
		self.pos = 0
		self.current_token = self.token_stream[self.pos]

	#Check if the current token is the expected one
	def consume(self, input_type):
		if self.current_token.type == input_type:
			if(self.current_token.type != EOF):
				self.pos+=1
				self.current_token = self.token_stream[self.pos]

		else:
			raise Exception("Syntax is invalid")

	def item(self):
		if(self.current_token.type == INT):
			output = self.current_token.value
			self.consume(INT)
			return output
		elif(self.current_token.type == LBRAC):
			self.consume(LBRAC)
			output = self.expr(False)
			self.consume(RBRAC)
			return output
		else:
			raise Exception("Syntax is invalid")

		token = self.current_token
		print("parsing", self.current_token.value)
		self.consume(INT)
		return token.value

	def factor(self):
		output = self.item()

		while (self.current_token.type == MUL or self.current_token.type == DIV):
			if(self.current_token.type == MUL):
				self.consume(MUL)
				output *= self.item()

			else:
				self.consume(DIV)
				output /= self.item()

		return output

	def expr(self,first = True):
		output = self.factor()

		while (self.current_token.type == ADD or self.current_token.type == SUB):
			if(self.current_token.type == ADD):
				self.consume(ADD)
				output += self.factor()
			else:
				self.consume(SUB)
				output -= self.factor()
		if(first):
			self.consume(EOF)
		return output

expression = input("Expression: ")
test = expression
# test_lexicon = lexer(test)
# i= test_lexicon.next_token()
# print(i.type,)
# while(i != EOF):
# 	i = test_lexicon.next_token()
# 	print(i.type,)
lexicon = lexer(expression)
token_stream = lexicon.tokenize()
print("tokens:",)
for i in token_stream[:-2]:
	print("(", i.type, ",", i.value,") ,", end =" ")
i = token_stream[-1]
print("(", i.type, ",", i.value,")")
Parser = parser(token_stream)
result = Parser.expr()
print(result)
#2+3+7*2+5
#int(2) add int(3) add int(7) mul int(2) add int(5)