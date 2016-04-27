package com.example.emily.recipeapp;

import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;


public class MainActivity extends ActionBarActivity {

    EditText searchBar;
    Button searchButton;
    ListView recipeList;
    TextView listText;
    TextView text1;
    TextView text2;
    ArrayAdapter<String> arrayAdapterIngredient;

    private MyDatabase db;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        searchBar = (EditText) findViewById(R.id.searchBar);
        searchButton = (Button) findViewById(R.id.buttonSearch);
        recipeList = (ListView) findViewById(R.id.recipeList);


        db = new MyDatabase(this);

        searchButton.setOnClickListener(new View.OnClickListener() {
            Cursor c;

            public void onClick(View v) {
                String[] searchTerms = searchBar.getText().toString().split(",");
                c = db.getRecipesByIngredient(searchTerms);
                //final ArrayList<MyArrayList> recipeNames = new ArrayList<MyArrayList>();
                final ArrayList<String> recipeNames = new ArrayList<String>();
                while (c.moveToNext())

                {
                    String recipeName = c.getString(c.getColumnIndexOrThrow(MyDatabase.RecipeColumns.REC_NAME));
                    String recipeUrl = c.getString(c.getColumnIndexOrThrow(MyDatabase.RecipeColumns.REC_URL));
                    MyArrayList tempList = new MyArrayList(recipeName, recipeUrl);
                    //recipeNames.add(tempList);
                    recipeNames.add(recipeName + "@@!@@" + recipeUrl);
                }

                c.close();
                arrayAdapterIngredient = new ArrayAdapter<String>(MainActivity.this, android.R.layout.simple_list_item_2, android.R.id.text1, recipeNames) {
                    @Override
                    public View getView(int position, View convertView, ViewGroup parent) {
                        View view = super.getView(position, convertView, parent);
                        text1 = (TextView) view.findViewById(android.R.id.text1);
                        text2 = (TextView) view.findViewById(android.R.id.text2);

                        String[] tempArray = recipeNames.get(position).split("@@!@@");

                        text1.setText(tempArray[0]);
                        text2.setText(tempArray[1]);
                        return view;
                    }


                };
                recipeList.setAdapter(arrayAdapterIngredient);
            }
        });



        recipeList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                String item = (String) parent.getItemAtPosition(position);
                Uri uriUrl = Uri.parse(text2.getText().toString());
                Intent launchBrowser = new Intent(Intent.ACTION_VIEW, uriUrl);
                startActivity(launchBrowser);
            }
        });

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }


}
