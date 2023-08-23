from .engine import expired_but_showing_live

class ExpiredButShowingLive():
    
    def __init__(self, cib_list):
        self.funded_ins = expired_but_showing_live.funded_ins_details(cib_list)
        self.funded_nonins= expired_but_showing_live.funded_nonins(cib_list)
        self.nonfunded = expired_but_showing_live.nonfunded_details(cib_list)
    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])


