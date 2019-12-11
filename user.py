class Users(object):

    def __init__(self, idu, name, name2, status, point, groups, ret, kod, obr):
        self.idu = idu
        self.name = name
        self.name2 = name2
        self.status = status
        self.point = point
        self.groups = groups
        self.ret = ret
        self.kod = kod
        self.obr = obr

    def chpo(self):
        s = ''
        if self.name is None:
            s = 'имя, '
        if self.name2 is None:
            s = s + 'фамилию, '
        if self.groups is None:
            s = s + 'номер группы, '
        if s == '':
            return False
        else:
            return s


