package com.example.emily.recipeapp;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteQueryBuilder;

import com.readystatesoftware.sqliteasset.SQLiteAssetHelper;

public class MyDatabase extends SQLiteAssetHelper {

    //private static DatabaseHelper sInstance;

    private static final String TAG = SQLiteAssetHelper.class.getSimpleName();
    private static final String DATABASE_NAME = "cooking.db.zip";
    private static final int DATABASE_VERSION = 1;

    public interface TABLES {
        String INGREDIENT = "ingredient";
        String RECIPE = "recipe";
        String ING_REC = "ingRec_xref";
        String INGREDIENT_MASTER = "ingredientMaster";
    }

    public interface IngredientColumns {
        String ING_ID = "_id";
        String ING_NAME = "name";
        String ING_MASTER_ID = "masterId";
    }

    public interface RecipeColumns {
        String REC_ID = "_id";
        String REC_NAME = "name";
        String REC_URL = "url";
    }

    public MyDatabase(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    public Cursor getIngredientItems() {
        SQLiteDatabase db = getReadableDatabase();
        SQLiteQueryBuilder qb = new SQLiteQueryBuilder();
        qb.setTables(TABLES.INGREDIENT);
        Cursor c = qb.query(db, null, null, null, null, null, null);
        c.moveToFirst();
        return c;
    }

    public Cursor getRecipesByIngredient(String[] recipes) {
        SQLiteDatabase db = getReadableDatabase();
        SQLiteQueryBuilder qb = new SQLiteQueryBuilder();

        StringBuffer searchTerms = new StringBuffer();
        searchTerms.append("('");
        for (int i = 0; i < recipes.length; i++){
            if (i > 0) {
                searchTerms.append("AND ");
            }
            searchTerms.append(recipes[i]);
        }
        searchTerms.append("')");


        String tables =
                "SELECT recipe.name,  recipe.url " +
                        "FROM ingredient, recipe, ingRec_xref, ingredientMaster WHERE recipe._id IN " +
                        "(SELECT recipe._id FROM recipe, ingredient, ingRec_xref WHERE (ingredient.name = " +
                        searchTerms.toString() +
                        " OR (ingredient.masterId = ingredientMaster._id) AND ingredientMaster.name = " +
                        searchTerms.toString() +
                        ") AND ingredient._id = ingRec_xref.ingId AND recipe._id = ingRec_xref.recId) " +
                        "AND ingredient._id = ingRec_xref.ingId AND recipe._id = " +
                        "ingRec_xref.recId AND ingredient.masterId = ingredientMaster._id";

        Cursor c = db.rawQuery(tables.toString(), null);
        c.moveToFirst();
        return c;
    }
}