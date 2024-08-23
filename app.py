from flask import Flask ,render_template ,request
import sqlite3
import pickle


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/contact',methods=['GET','POST'])
def contactus():
    if request.method =='POST':
        fname =request.form.get('name')
        pnumber=request.form.get('phone')
        email=request.form.get('email')
        addr=request.form.get('address')
        msg=request.form.get('message')
        print(fname,pnumber,email,addr,msg)
        conn=sqlite3.connect('youtube database.db')
        cur=conn.cursor()
        cur.execute(f'''
                    insert into contact values('{fname}','{pnumber}','{email}',
                    '{addr}','{msg}')
                    ''')
        conn.commit()
        return render_template('message.html')
    else:
        return render_template('contactus.html')



@app.route('/analytical')
def analytical():
    return render_template('analytical.html')




@app.route('/prediction',methods=['GET','POST'])
def prediction():
    if request.method == 'POST':
        views = int(request.form['views'])
        dislikes = int(request.form['dislikes'])
        comment_count = int(request.form['comment_count'])
        comments_disabled = int(request.form.get('comments_disabled', 0))
        ratings_disabled = int(request.form.get('ratings_disabled', 0))
        video_error_or_removed = int(request.form.get('video_error_or_removed', 0))
        genre = int(request.form['genre'])
        input_data = [[views, dislikes, comment_count, comments_disabled, ratings_disabled, video_error_or_removed, genre]]
        
        with open('model.pickle','rb') as mod:
            model=pickle.load(mod)
        
        pred=model.predict(input_data)
        return render_template('result.html',pred= str(round(pred[0])))
    else:
        return render_template('prediction.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050)