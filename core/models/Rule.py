from core.config import db

class Rule(db.Model):

    __tablename__ = 'rules'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CE = db.Column(db.JSON(), nullable=True)
    Pattern = db.Column(db.JSON(), nullable=True)

    def __init__(self, CE, Pattern) -> 'Rule':
        self.CE = CE
        self.Pattern = Pattern