from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.users_model import User
from pprint import pprint
from flask import flash

class Recipe:
    db="recipe_share"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.date_cooked = data['date_cooked']
        self.under_30_min = data['under_30_min']
        self.cook = None

    @classmethod
    def create_recipe(cls, data):
        # print("request.form")
        query= """INSERT INTO recipe (name, description, instructions, user_id, date_cooked, under_30_min) 
                    VALUES ( %(name)s, %(description)s, %(instructions)s, %(user_id)s, %(date_cooked)s, %(under_30_min)s )
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_recipes(cls):
        all_recipes = []
        query="SELECT * FROM recipe JOIN users ON recipe.user_id = users.id"
        results = connectToMySQL(cls.db).query_db(query)
        for rows in results:
            one_recipe = cls(rows)
            one_recipe_cook = {
                "id" : rows['users.id'],
                "first_name" : rows['first_name'],
                "last_name" : rows['last_name'],
                "email" : rows['email'],
                "password" : rows['password'],
                "created_at" : rows['users.created_at'],
                "updated_at" : rows['users.updated_at']
            }
            chef = User(one_recipe_cook)
            one_recipe.cook = chef
            all_recipes.append( one_recipe )
        return all_recipes

    @classmethod
    def get_one_recipe(cls, id):
        one_dish = []
        query="SELECT * FROM recipe JOIN users ON recipe.user_id = users.id WHERE recipe.id = %(id)s"
        data = {"id": id}
        results = connectToMySQL(cls.db).query_db(query, data)
        pprint(results, sort_dicts=False)
        for rows in results:
            one_recipe = cls(rows)
            one_recipe_cook = {
                "id" : rows['users.id'],
                "first_name" : rows['first_name'],
                "last_name" : rows['last_name'],
                "email" : rows['email'],
                "password" : rows['password'],
                "created_at" : rows['users.created_at'],
                "updated_at" : rows['users.updated_at']
            }
            chef = User(one_recipe_cook)
            one_recipe.cook = chef
            one_dish.append( one_recipe )
        return one_dish
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid=True
        if len(recipe['name']) < 3 or len(recipe['description']) < 3 or len(recipe['instructions']) < 3:
            flash("Name, Description and instructions must be at least 3 characters")
            is_valid = False
        if recipe.get('under_30_min') == None:
            flash("Please specify if your dish can be cooked under 30 minutes")
            is_valid = False
        return is_valid
    
    @classmethod
    def edit_my_recipe(cls, recipe):
        query = """UPDATE recipe
                    SET name = %(name)s, 
                        instructions = %(instructions)s,
                        description = %(description)s,
                        date_cooked = %(date_cooked)s,
                        under_30_min = %(under_30_min)s
                    WHERE id = %(id)s """
        data = { "name" : recipe['name'],
                "instructions" : recipe['instructions'],
                "description" : recipe['description'],
                "date_cooked" : recipe['date_cooked'],
                "under_30_min" : recipe['under_30_min'],
                "id" : recipe['id']
                }
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_recipe(cls, id):
        query="DELETE FROM recipe WHERE id = %(id)s"
        data = {"id": id}
        return connectToMySQL(cls.db).query_db(query, data)