class User:

    def __init__(self, 
                 username,
                 lastQuestionSubmitted,
                 lastTime,
                 modemQuestionCompleted,
                 codeQuestionCompleted
                ):
        
        self.username = username
        self.lastQuestionSubmitted = lastQuestionSubmitted
        self.lastTime = lastTime
        self.modemQuestionCompleted = modemQuestionCompleted
        self.codeQuestionCompleted = codeQuestionCompleted