from belt_app.config.mysqlconnection import connectToMySQL, db
from belt_app.models import user
from flask import flash,session


# ===================
# INITIALIZE INSTANCE
# ===================
class Tree:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.plant_date = data['plant_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.visitors = []


    # INSTANCE METHODS
    def return_visitor_count(self):
        return len(self.visitors)




    # =============
    # CLASS METHODS
    # =============

    # ===========
    #  CREATE SQL
    # ===========
    @classmethod
    def create_tree(cls, form_data):
        if not cls.validate_tree_form(form_data): return False
        data = form_data.copy()
        data['user_id'] = session['user_id']
        query = '''
        INSERT INTO trees
        (user_id,species,location,reason,plant_date)
        VALUES
        (%(user_id)s,%(species)s,%(location)s,%(reason)s,%(plant_date)s);
        '''
        return connectToMySQL(db).query_db(query,data)


    # ========
    # READ SQL
    # ========
    @classmethod
    def fetch_all_trees(cls):
        query = '''
        SELECT
        trees.id,trees.user_id,species,location,reason,
        plant_date,trees.created_at,trees.updated_at,
        users.id,first_name,last_name,
        email,password,users.created_at,users.updated_at,
        COUNT(visitors.tree_id)
        AS visitor_count
        FROM trees
        JOIN users
        ON trees.user_id = users.id
        LEFT JOIN visitors
        ON visitors.tree_id = trees.id
        GROUP BY trees.id;
        '''
        all_trees = []
        results = connectToMySQL(db).query_db(query)
        if results:
            for row in results:
                this_tree = cls(row)
                user_data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_tree.user = user.User(user_data)
                this_tree.visitors = row['visitor_count']
                all_trees.append(this_tree)
        return all_trees

    @classmethod
    def fetch_tree_by_id(cls, id):
        data ={'id':id}
        query = '''
        SELECT * FROM trees
        LEFT JOIN users
        ON users.id = trees.user_id
        LEFT JOIN visitors
        ON visitors.tree_id = trees.id
        LEFT JOIN users As users2
        ON users2.id = visitors.user_id
        WHERE trees.id = %(id)s;
        '''
        results = connectToMySQL(db).query_db(query,data)
        if results:
            this_tree = cls(results[0])
            for row in results:
                planter_data = {
                        'id': row['users.id'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'email': row['email'],
                        'password': row['password'],
                        'created_at': row['users.created_at'],
                        'updated_at': row['users.updated_at']
                    }
                visitor_data = {
                        'id': row['users2.id'],
                        'first_name': row['users2.first_name'],
                        'last_name': row['users2.last_name'],
                        'email': row['users2.email'],
                        'password': row['users2.password'],
                        'created_at': row['users2.created_at'],
                        'updated_at': row['users2.updated_at']
                    }
                this_tree.user = user.User(planter_data)
                this_tree.visitors.append(user.User(visitor_data))
            return this_tree
        return False

    @classmethod
    def fetch_tree_by_user_id(cls,id):
        data = {'id':id}
        query = '''
        SELECT * FROM trees
        WHERE user_id = %(id)s;
        '''
        results = connectToMySQL(db).query_db(query,data)
        all_trees = []
        for row in results:
            this_tree = cls(row)
            all_trees.append(this_tree)
        return all_trees



    # ==========
    # UPDATE SQL
    # ==========
    @classmethod
    def update_tree(cls,form_data,id):
        if not cls.validate_tree_form(form_data):return False
        data = form_data.copy()
        data['id'] = id
        query = '''
        UPDATE trees
        SET
        species = %(species)s,
        location = %(location)s,
        reason = %(reason)s,
        plant_date = %(plant_date)s
        WHERE id =%(id)s;
        '''
        connectToMySQL(db).query_db(query,data)
        return True



    # ==========
    # DELETE SQL
    # ==========
    @classmethod
    def delete_tree(cls,id):
        data = {'id':id}
        query = '''
        DELETE FROM trees
        WHERE id = %(id)s;
        '''
        return connectToMySQL(db).query_db(query,data)




    # ==============
    # STATIC METHODS
    # ==============
    @staticmethod
    def validate_tree_form(form_data):
        is_valid = True
        if len(form_data['species']) < 5:
            flash('Species name must be atleast 5 characters')
            is_valid = False
        if len(form_data['location']) < 2:
            flash('Location must be atleast 2 characters')
            is_valid = False
        if len(form_data['reason']) < 2 or len(form_data['reason']) > 50:
            flash('Reason must be atleast 2 characters and less than 50')
            is_valid = False
        if not form_data['plant_date']:
            flash('Please pick a plant date')
            is_valid = False
        return is_valid