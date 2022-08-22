from belt_app.config.mysqlconnection import connectToMySQL, db
from belt_app.models import user,tree
from flask import session


# ===================
# INITIALIZE INSTANCE
# ===================
class Visitor:
    def __init__(self,data):
        self.user_id = data['user_id']
        self.tree_id = data['tree_id']
        self.user = None
        self.tree = None



    # =============
    # CLASS METHODS
    # =============

    # ===========
    #  CREATE SQL
    # ===========
    @classmethod
    def create_new_visit(cls,id):
        data = {
            'user_id': session['user_id'],
            'tree_id': id
        }
        query = '''
        INSERT INTO visitors
        (user_id,tree_id)
        VALUES
        (%(user_id)s,%(tree_id)s);
        '''
        return connectToMySQL(db).query_db(query,data)



    # =================================
    # READ SQL -- just to show cls ass.
    # =================================
    @classmethod
    def fecth_visitors_by_tree_id(cls,id):
        data = {'id':id}
        query = '''
        SELECT * FROM visitors
        JOIN users
        ON users.id = visitors.user_id
        JOIN trees
        ON trees.id = visitors.tree_id
        WHERE tree_id = %(id)s;
        '''
        results = connectToMySQL(db).query_db(query,data)
        all_visitors = []
        if results:
            for row in results:
                this_visitor = cls(results[0])
                user_data = {
                        'id': row['id'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'email': row['email'],
                        'password': row['password'],
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at']
                    }
                tree_data = {
                        'id': row['trees.id'],
                        'user_id': row['trees.user_id'],
                        'species': row['species'],
                        'location': row['location'],
                        'reason': row['reason'],
                        'plant_date': row['plant_date'],
                        'created_at': row['trees.created_at'],
                        'updated_at': row['trees.updated_at']
                    }
                this_visitor.user = user.User(user_data)
                this_visitor.tree = tree.Tree(tree_data)
                all_visitors.append(this_visitor)
        return all_visitors



    @staticmethod
    def did_user_visit_tree_already(id):
        this_tree_visitors = Visitor.fecth_visitors_by_tree_id(id)
        for visitor in this_tree_visitors:
            if visitor.user.id == session['user_id']:
                return True
        return False