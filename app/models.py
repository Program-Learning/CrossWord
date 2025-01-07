from app import db

# crossword游戏试卷
class papers(db.Model):
    id = db.Column("paper_id", db.Integer, primary_key=True, autoincrement=True)
    paper = db.Column(db.String(100))
    player = db.Column(db.Integer, db.ForeignKey("player.player_id"))

    def __init__(self, paper_json):
        self.paper = paper_json


# 试卷要求不能重复使用同一句诗词，所以需要记录一下每个试卷的历史答题诗句
class history_insert_records(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    paperID = db.Column(db.Integer, db.ForeignKey("papers.paper_id"))
    history = db.Column(db.String(100))

    def __init__(self, paperID, history):
        self.paperID = paperID
        self.history = history


# 有效诗词记录，即题库
class poems(db.Model):
    id = db.Column("poem_id", db.Integer, primary_key=True, autoincrement=True)
    poem = db.Column(db.String(100))

    def __init__(self, poem_str):
        self.poem = poem_str

    def len(self):
        return len(self.poem)

    def iter_poem(self):
        return iter(self.poem)