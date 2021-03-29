from dummy_predictor import dummy_model
from flask import Flask, render_template, request
from flask_executor import Executor
import pandas as pd


app = Flask(__name__)
executor = Executor(app)

##############
## Flask #####
##############

# @app.route('/')
# def my_form():
#     return render_template('index.html')

@app.route('/', methods=['GET','POST'])
def my_form_post():
    query = request.args.get("text")
    df = pd.read_csv("../raw_data/mag_test.csv")
    search_query = query
    df_res = dummy_model(df, str(search_query))
    df_res.drop_duplicates(subset='product_id',inplace=True)
    # df_list_photos = []
    # for i in range(len(df_res)):
    #     df_list_photos.append(df_res['photos'])
    return render_template('index.html', data=df_res['photos'],query=query)


##############
## dummy model  #####
##############
request_ctx = app.test_request_context()
request_ctx.push()


#############
#dummy fonction#
#############
# df = pd.read_csv("../raw_data/mag_test.csv")
# search_query = my_form_post()[1]
# df_res = dummy_model(df, str(search_query))
# df_res.drop_duplicates(subset='product_id',inplace=True)

# test = df_res.iloc[0]['photos']

# data = []
# for i in range (len(df_res)):
#     data.append(df_res.iloc[i]['photos'])

# image = df_res.to_dict()
# print(test)




if __name__ == "__main__":
    app.run(debug=True)
