import array
import sys

ram = array.array('I',[0x00,0x00,0x00,0x00,
					   0x00,0x00,0x00,0x00,
					   0x00,0x00,0x00,0x00,
					   0x00,0x00,0x00,0x00
					   ])

#instruction set
LDA=0x01 #load value from the RAM location to register A
ADD=0x02 #add value from the RAM location to register A
SUB=0x03 #subtract value at the RAM location from register A
OUT=0x04 #load A to out register
HLT=0x05 #halt execution of the program

out = 0x00
A = 0x01
PC = 0x00
ID = 0x00

def decodeInstruction(ID):
	global A
	global out
	global PC

	operand = ID & 0x0F
	opcode = ID >> 4
	
	if opcode == LDA:
		#load RAM data into A
		A = ram[operand]
		PC = PC+1

	elif opcode == ADD:
		#add RAM data to A
		A = A + ram[operand]
		PC = PC+1

	elif opcode == SUB:
		#subtract RAM data from A
		A = A - ram[operand]
		PC = PC+1

	elif opcode == OUT:
		#output to out register
		out = A
		PC = PC+1

	elif opcode == HLT:
		# print(hex(PC),hex(A),hex(out))
		print("Out:",hex(out))
		sys.exit("HALTED!")



def executeProgram():
	#load instruction to instruction decoder 
	#from the address pointed out by PC
	ID = ram[PC]
	decodeInstruction(ID)
	executeProgram()

def loadCodeInRAM():
	global ram
	with open('code.s') as fp:
		line = fp.readline()
		cnt = 1
		while line:
			data = line.split()
			if len(data) == 2:
				instruction = globals()[data[0]] << 4 | int(data[1],0)
				# print(cnt-1,hex(instruction))
				ram[cnt-1] = instruction
			elif len(data) == 1:
				instruction = globals()[data[0]] << 4 | 15	
				# print(cnt-1,hex(instruction))
				ram[cnt-1] = instruction
			elif len(data) == 3:
				if data[0] == 'DATA':
					ram[int(data[1],0)] = int(data[2],0)
				
			line = fp.readline()
			cnt += 1

		

loadCodeInRAM()
print([hex(i) for i in ram])

executeProgram()
print(out)