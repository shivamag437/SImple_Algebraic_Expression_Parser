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

	def next_token(self):

		if self.char == None:
			result = token(EOF, '$')
		
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

		self.pos += 1

		if(self.pos > len(self.stream) - 1) :
			self.char = None
		else:
			self.char = self.stream[self.pos]

		return result

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

	def consume(self, input_type):
		if self.current_token.type == input_type:
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
			output = self.expr()
			self.consume(RBRAC)
			return output
		else:
			raise Exception("Syntax is invalid")

		token = self.current_token
		print("parsing", self.current_token.value)
		self.consume(INT)
		return token.value

	def multiple(self):
		output = self.item()

		while (self.current_token.type == MUL or self.current_token.type == DIV):
			if(self.current_token.type == MUL):
				self.consume(MUL)
				output *= self.item()

			else:
				self.consume(DIV)
				output /= self.item()

		return output

	def expr(self):
		output = self.multiple()

		while (self.current_token.type == ADD or self.current_token.type == SUB):
			if(self.current_token.type == ADD):
				self.consume(ADD)
				output += self.multiple()
			else:
				self.consume(SUB)
				output -= self.multiple()

		if(self.current_token.type == RBRAC or self.current_token.type == EOF):
			return output

		else:
			raise Exception("Syntax is invalid")

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
for i in token_stream:
	print(i.type, i.value,",",)
Parser = parser(token_stream)
result = Parser.expr()
print(result)
#2+3+7*2+5
#int(2) add int(3) add int(7) mul int(2) add int(5)