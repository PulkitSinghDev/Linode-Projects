import random

class Rule(object):
    """
    General rule object.
    Rules can be executed.
    """
    def __init__(self):
        pass

    # execute this rule in the context of a given grammar
    def execute(self):
        pass

class TextNode(Rule):
    """
    Text nodes just return strings when executed.
    """
    def __init__(self, text):
        super(TextNode, self).__init__()
        self.text = text

    # text rules simply return their given text
    def execute(self):
        return self.text

    def __repr__(self):
        return self.text

class SequentialNode(Rule):
    """
    Sequential nodes call their given rules in sequence.
    """
    def __init__(self, others):
        super(SequentialNode, self).__init__()
        self.others = others

    def execute(self):
        result = ''
        for other in self.others:
            result = '{0}{1}'.format(result, other.execute())

        return result

    def add_other(self, other):
        self.others.append(other)

    def __repr__(self):
        result = ''
        for other in self.others:
            result = '{0}{1}'.format(result, other)

        return result

class GrammarRule(Rule):
    def __init__(self, grammar, label):
        self.grammar = grammar
        self.label = label

    def execute(self):
        return self.grammar.get(self.label).execute()

    def __repr__(self):
        return '`{0}`'.format(self.label)

    def to_cnf(self):
        return [self]

class Grammar(object):
    """
    Context-free grammar.
    Associates labels with rules.
    """
    def __init__(self):
        self.rules = {}

    # add a rule with a name
    def add_rule(self, name, rule):
        # check if it exists
        if name not in self.rules:
            self.rules[name] = []

        # add to list
        self.rules[name].append(rule)

    # get a rule
    def get(self, name):
        # check if it exists
        if name not in self.rules:
            raise ValueError('Rule not found: {0}'.format(name))

        # randomly choose a rule from the list
        index = random.randrange(0, len(self.rules[name]))
        return self.rules[name][index]

    # convert to string
    def __repr__(self):
        result = ''
        for name in self.rules:
            for rule in self.rules[name]:
                result = '{0} -> {1}\n{2}'.format(name, rule, result)
        return result

    # start derivation
    def derive(self, start):
        return self.get(start).execute()

    # convert to Chomsky normal form
    def to_cnf(self):
        # CNF equivalent of current grammar
        g_cnf = Grammar()

        # START: Eliminate the start symbol from right-hand sides
        g_cnf.add_rule('S0', GrammarRule(g_cnf, 'S'))

        # TERM: Eliminate rules with nonsolitary terminals
        counter = 0
        for name in self.rules:
            for rule in self.rules[name]:
                # check size
                if len(rule.others) > 1:
                    # replace all TextNodes
                    nodes = []
                    for i in range(0, len(rule.others)):
                        other = rule.others[i]

                        # terminal
                        if isinstance(other, TextNode):
                            # new rule
                            g_cnf.add_rule('T{0}'.format(counter), other)
                            # replace current rule
                            nodes.append(GrammarRule(g_cnf, 'T{0}'.format(counter)))
                            counter += 1
                        else:
                            # add to nodes
                            nodes.append(other)
                    # replace rule
                    g_cnf.add_rule(name, SequentialNode(nodes))
                else:
                    # just add it
                    g_cnf.add_rule(name, rule)

        # BIN: Eliminate right-hand sides with more than 2 nonterminals
        counter = 0
        rules_copy = g_cnf.rules.copy()
        for name in rules_copy:
            for rule in rules_copy[name]:
                # check type
                if not isinstance(rule, SequentialNode):
                    continue

                # check size
                if len(rule.others) > 2:
                    first = True
                    current = rule.others[0:]
                    while len(current) > 0:
                        # add link to grammar
                        parts = [current[0]]
                        if len(current) > 1:
                            parts.append(GrammarRule(g_cnf, 'B{0}'.format(counter+1)))

                        new_name = name
                        if not first:
                            new_name = 'B{0}'.format(counter)
                        g_cnf.add_rule(new_name, SequentialNode(parts))

                        # next rule
                        current = current[1:]
                        counter += 1
                        first = False
        # clean-up
        for name in g_cnf.rules:
            g_cnf.rules[name] = [rule for rule in g_cnf.rules[name] if
                                 not isinstance(rule, SequentialNode) or
                                 len(rule.others) <= 2]

        # DEL: Eliminate eps-rules

        # UNIT: Eliminate unit rules

        return g_cnf

class Parser(object):
    """
    Parser for CFGs.
    The format of a rule is A -> B where A is an alphanumeric name and B is any string.
    One can refer to a rule named S by typing `S` in the right-hand side.
    """
    def __init__(self, grammar):
        # store grammar
        self.grammar = grammar

    # parse a single rule
    def parse_rule(self, rule):
        # split into left and right parts
        tmp = rule.split(' -> ')
        if len(tmp) != 2:
            raise ValueError('Invalid rule definition: {0}'.format(rule))
        left = tmp[0]
        right = tmp[1]

        # create nodes
        nodes = []
        in_rule = False
        buffer = ''
        for i in range(0, len(right)):
            if right[i] == '`':
                result = None
                if in_rule:
                    # create call to rule
                    result = GrammarRule(self.grammar, buffer)
                else:
                    # create text node
                    result = TextNode(buffer)
                # add to nodes
                nodes.append(result)

                # invert flag
                in_rule = not in_rule
                # clear buffer
                buffer = ''
            else:
                # add to buffer
                buffer = '{0}{1}'.format(buffer, right[i])
        # check remainder
        if len(buffer) > 0:
            # verify rule
            if in_rule:
                raise ValueError('Unterminated rule `{0}` in {1}'.format(buffer, left))

            # add text node
            nodes.append(TextNode(buffer))

        # create sequential node
        result = SequentialNode(nodes)
        # register in grammar
        self.grammar.add_rule(left, result)

    # parse multiple rules
    def parse_rules(self, rules):
        for rule in rules:
            self.parse_rule(rule)

    # return grammar
    def get_grammar(self):
        return self.grammar
