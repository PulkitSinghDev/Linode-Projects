import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()

store = {}


def normal(q):
    if q[0] == '~':
        return q[1:]
    else:
        return q


# backward chaining on kb for q
def backward_chain(kb, q, d = 0):
    global store

    print('{1}Subgoal: {0}'.format(q, '    '*d))
    # if already proved
    if q in store:
        print('{0}{1} (previous).'.format('    '*(d+1), store[q]))
        return store[q]
    # find rules that conclude q
    for c in kb:
        if c == q:
            # check trivial case
            if kb[c] is None:
                print('{0}True.'.format('    '*(d+1)))
                store[c] = True
                return True

            # attempt to prove its premises
            store[c] = all([(not backward_chain(kb, normal(p), d+1)) if p[0] == '~' else backward_chain(kb, p, d+1) for p in kb[c]])
            return store[c]
    # not provable
    print('{0}False.'.format('    '*(d+1)))
    store[c] = False
    return False

# populate KB
kb = {}
lines = form['kb'].value.split('\r\n')
for line in lines:
    tmp = line.strip().split(': ')
    conclusion = tmp[0]
    premises = None
    if len(tmp) > 1:
        premises = tmp[1].split(', ')

    kb[conclusion] = premises

# prove query by backward chaining
result = None
q = form['q'].value
if q[0] == '~':
    result = not backward_chain(kb, normal(q))
else:
    result = backward_chain(kb, q)
print('Query is: {0}'.format(result))
