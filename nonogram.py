from itertools import combinations
import subprocess

class problem:
    def __init__(self,data):
        self.r, self.c, self.rdata, self.cdata = self.parse(data)

    def parse(self,data):
        lines = data.strip().split('\n')
        r, c = int(lines.pop(0)),int(lines.pop(0))
        rdata = map(lambda x: map(int,x.split()),lines[:r])
        cdata = map(lambda x: map(int,x.split()),lines[r:])
        return (r,c,rdata,cdata)

def find_row_case(rule,length,i):
    global rule_counter, rule_info, false_table, true_table
    sumi = sum(rule)
    start = rule_counter
    for indexs in combinations(xrange(length-sumi+1),len(rule)):
        indexs += (length-sumi,)
        blocks = (indexs[0],)
        for j in xrange(len(rule)):
            blocks += (rule[j],indexs[j+1]-indexs[j])
        j = 0
        neg = True
        for block in blocks:
            while block:
                if neg:
                    false_table[i][j] += (rule_counter,)
                else:
                    true_table[i][j] += (rule_counter,)
                block -= 1
                j += 1
            neg = 1 - neg
        rule_info.append(blocks)
        rule_counter += 1
    end = rule_counter
    return ' '.join(map(str,range(start,end))) + ' 0\n'

def find_col_case(rule,length,i):
    global rule_counter, rule_info, false_table, true_table
    sumi = sum(rule)
    start = rule_counter
    for indexs in combinations(xrange(length-sumi+1),len(rule)):
        indexs += (length-sumi,)
        blocks = (indexs[0],)
        for j in xrange(len(rule)):
            blocks += (rule[j],indexs[j+1]-indexs[j])
        j = 0
        neg = True
        for block in blocks:
            while block:
                if neg:
                    false_table[j][i] += (rule_counter,)
                else:
                    true_table[j][i] += (rule_counter,)
                block -= 1
                j += 1
            neg = 1 - neg
        #rule_info.append(blocks)
        rule_counter += 1
    end = rule_counter
    return ' '.join(map(str,range(start,end))) + ' 0\n'


if __name__ == '__main__':
    with open('CWD','r') as cwd:
        nono = problem(cwd.read())

    clauses = 0
    rule_counter = 1
    true_table = [[() for _ in xrange(nono.c)] for _ in xrange(nono.r)]
    false_table = [[() for _ in xrange(nono.c)] for _ in xrange(nono.r)]
    rule_info = [None]
    output = ''
    #print "find row case"
    for r in range(nono.r):
        #print r
        output += find_row_case(nono.rdata[r],nono.c,r)
    #print "find col case"
    for c in range(nono.c):
        #print c
        output += find_col_case(nono.cdata[c],nono.r,c)
    clauses += nono.r + nono.c

    #print "interchange rule"
    for r in range(nono.r):
        for c in range(nono.c):
            for t in true_table[r][c]:
                for f in false_table[r][c]:
                    output += '-%d -%d 0\n'%(t,f)
            clauses += len(true_table[r][c]) * len(false_table[r][c])

    with open('test.in','w') as indata:
        indata.write('p cnf %d %d\n'%(rule_counter-1,clauses))
        indata.write(output)

    #print "minisat run!"
    subprocess.call(["minisat","test.in","test.out"],stdout=open('/dev/null','w'))
    #subprocess.call("minisat test.in test.out",shell=True)


    with open('test.out','r') as outdata:
        sat = outdata.readline().strip()
        #print sat
        if sat == 'SAT':
            data = map(int,filter(lambda x: x[0]!='-', outdata.readline().strip().split()[:-1]))[:nono.r]
        for d in data:
            line = ''
            neg = True
            for block in rule_info[d]:
                if neg:
                    line += '.'*block
                else:
                    line += '#'*block
                neg = 1 - neg
            print line



