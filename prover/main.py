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
def backward_chain(kb, q, d = 0, hist):
    global store

    # check for cycles
    if q in hist and not q in store:
        print('Cycle detected: {0}'.format(q))
        return False

    # record the query
    hist.add(q)

    print('{1}Subgoal: {0}'.format(q, '    '*d))
    # if already proved
    if q in store:
        print('{0}{1} (previous).'.format('    '*(d+1), store[q]))
        return store[q]
    # find rules that conclude q
    if q in kb:
        # check trivial case
        if kb[q] is None:
            print('{0}True.'.format('    '*(d+1)))
            store[q] = True
            return True

        # attempt to prove its premises
        store[q] = all([(not backward_chain(kb, normal(p), d+1, hist)) if p[0] == '~' else backward_chain(kb, p, d+1, hist) for p in kb[q]])
    else:
        # not provable
        print('{0}False.'.format('    '*(d+1)))
        store[q] = False
    return store[q]

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
    result = not backward_chain(kb, normal(q), set())
else:
    result = backward_chain(kb, q, set())
print('Query is: {0}'.format(result))
