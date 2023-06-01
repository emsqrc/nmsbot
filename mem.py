



class mem:
    def __init__(self) -> None:
        self.memory = dict()
        self.delmemory = dict()
        self.sitimemory = dict()

    def addClient(self,id,c_id):
        self.memory[id] = c_id

    def getClient(self, id):
        if id in self.memory.keys():
            return self.memory[id]
        else:
            return ''
    
    def addMessageId(self,id,m_id):
        self.delmemory[id] = m_id

    def getMessageId(self, id):
        if id in self.delmemory.keys():
            return self.delmemory[id]
        else:
            return ''
    
    def addSiti(self,id,siti):
        self.sitimemory[id] = siti

    def getSiti(self, id):
        if id in self.sitimemory.keys():
            return self.sitimemory[id]
        else:
            return ''