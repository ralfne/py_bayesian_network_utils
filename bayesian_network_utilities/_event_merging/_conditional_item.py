

class _ConditionalItem(object):
    def __init__(self, vector, is_conditional=True):
        self._is_conditional = is_conditional
        if self._is_conditional:
            self._outcome = vector[-2]
            self._conditions = vector[0:len(vector) - 2]
            self._p = vector[-1]
        else:
            self._outcome = vector[0]
            self._conditions = None
            self._p = vector[1]

    def get_is_conditional(self):
        return self._is_conditional

    def get_outcome(self):
        return self._outcome

    def get_conditions(self):
        return self._conditions

    def get_probability(self):
        return self._p

    def export_probabilities(self):
        out = []
        for item in self._conditions:
            out.append(item)
        out.append(self._outcome)
        out.append(self._p)
        return out

    def has_condition_or_outcome(self, key):
        if self.contains_condition(key): return True
        if self._outcome == key: return True
        return False

    def contains_condition(self, condition):
        if self._conditions is None: return False
        for c in self._conditions:
            if c == condition: return True
        return False

    def get_signature(self, except_conditions=None):
        out = ''
        if self._is_conditional:
            for c in self._conditions:
                if except_conditions is None:
                    out += c + '_'
                else:
                    if c not in except_conditions: out += c + '_'
            if not self._outcome in except_conditions:
                out += self._outcome
        else:
            if except_conditions is None: out += self._outcome
            else:
                if self._outcome not in except_conditions: out += self._outcome
        return out

    def __str__(self):
        out = ''
        if self._conditions is not None:
            for c in self._conditions:
                out += c + ' '
        out += self._outcome + ' '
        out += str(self._p)
        return out

