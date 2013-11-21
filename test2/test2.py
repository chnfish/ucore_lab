from z3 import *

N = 5
OP_ADD  = 0
OP_SUB  = 1
OP_MUL  = 2
OP_DIV  = 3

Input = [1,1,1,1,6]
op = [ Int("op_%s" % (i)) for i in range(N - 1) ]
left1_array = Array('left1', IntSort(), IntSort())
left2_array = Array('left2', IntSort(), IntSort())
right_array = Array('right', IntSort(), IntSort())
leftp = [ Int("leftp_%s" % (i)) for i in range(N * 2 - 1) ]
rightp = [ Int("rightp_%s" % (i)) for i in range(N * 2 - 1) ]
value = Array('value', IntSort(), RealSort())
output = range(2 * N)


def get_symbol(op):
    if (op == OP_ADD):
        return "+"
    if (op == OP_SUB):
        return "-"
    if (op == OP_MUL):
        return "*"
    return "/"

def some_ope_app(op, x1, x2, x3):
    return If(op == OP_ADD, value[x1] + value[x2] == value[x3],
           If(op == OP_SUB, value[x1] - value[x2] == value[x3],
           If(op == OP_MUL, value[x1] * value[x2] == value[x3],
           And(value[x1] == value[x2] * value[x3], value[x2] != 0 ))))


S = Solver()
#Posistions for determined variables and the answer
for i in range(N):
	S.add(rightp[i] == i) 
S.add(leftp[2 * N - 2] == 2 * N - 1)
S.add(rightp[2 * N - 2] == 2 * N - 2)
#Constraint for the position
for i in range(2 * N - 1):
    if (i != 2 * N - 2):
        S.add(leftp[i] < 2 * N - 1, leftp[i] >= N)
    S.add(rightp[i] >= 0, rightp[i] < 2 * N - 1)
    S.add(leftp[i] > rightp[i])
    S.add(right_array[rightp[i]] == i)
    S.add(Or(left1_array[leftp[i]] == i, left2_array[leftp[i]] == i))

#The determined values
S.add(right_array[2 * N - 2] == left1_array[2 * N - 1])
for i in range(N):
	S.add(value[right_array[i]] == Input[i]);
S.add(value[left1_array[2 * N - 1]] == 24);

#Operation correctness
for i in range(N, 2 * N - 1):
    #print i
    S.add(left1_array[i] >= 0, left1_array[i] < 2 * N)
    S.add(left2_array[i] >= 0, left2_array[i] < 2 * N)
    S.add(right_array[i] >= 0, right_array[i] < 2 * N)
    S.add(left1_array[i] != left2_array[i])
    S.add(some_ope_app(op[i - N], left1_array[i], left2_array[i], right_array[i]));

#print !S.assertions()
#check and output
r = S.check()
if r == unsat:
    print("no solution")
elif r == unknown:
    print("failed")
    print S.reason_unknown()
else:
    print("found solution")
    m = S.model()
    for i in range(N):
        #print i
        output[i] = str(Input[i])
    for i in range(N, 2 * N - 1):
        
        #print int(str(m.eval(left1_array[i])))
        #print m.eval(left2_array[i])
        #output[m[right_array][i]]
        output[int(str(m.eval(right_array[i])))] = "(" + str(output[int(str(m.eval(left1_array[i])))]) + get_symbol(int(str(m.eval(op[i - N])))) + str(output[int(str(m.eval(left2_array[i])))]) + ")"
    #print "outputs:"
    #print [m.eval(leftp[i]) for i in range(N * 2 - 1)]
    #print [m.eval(rightp[i]) for i in range(N * 2 - 1)]
    #print m[rightp]
    #print m[value]
    #for i in range(2 * N - 1):
    #    print output[i]
    print output[2 * N - 2]


