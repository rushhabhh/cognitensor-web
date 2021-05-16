from flask import Flask
from flask import jsonify
from flask import send_file
from flask import redirect
from flask import url_for
from flask import request
from flask_mail import Mail
from flask_mail import Message
import json
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from io import BytesIO
import base64
from sqlalchemy import func
from flask import send_from_directory
import os
from wtforms import validators
from flask import flash




# UPLOAD_FOLDER='/home/deepak/Desktop/website1/fileuploads'
ALLOWED_EXTENSIONS ={'pdf'}


UPLOAD_FOLDER= os.path.abspath("fileuploads")





##### DATABASE CONFIGURATION ###########

app=Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


##### CONFIG.JSON FILE CONFIGURATION ########

with open('config.json', 'r') as c:
    params = json.load(c)["params"]



###### CONFIGURING MAIL FUNCTIONALITY #######
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)







####### INDEX ROUTE ###################################

@app.route('/', methods=['GET','POST'])
def index():
   if request.method == "POST":
        name=request.form.get('name')
        company_name=request.form.get('cname')
        email=request.form.get('email')
        contact=request.form.get('contactno')
        entry = Request_Demo_Form(name=name, company_name=company_name, email=email,contact=contact)
        db.session.add(entry)
        db.session.commit()
        flash("Request Sent Successfully")
        mail.send_message('Request From  ' + name + " " + company_name,
                      sender=email,
                      recipients=['rushhabhh@gmail.com'],
                      body="Name   :  " + name+ "\n" + "Company Name   :  " + company_name+ "\n" + "Email   :  " + email + "\n" + "Contact No  :  " + contact)
        print("POST METHOD CHAL GYA")
        # return ("<h1>REQUEST SENT SUCCESFULLY<h1>")
        return render_template('index.html')
   else:
       return render_template('index.html')







######### ABOUTUS ROUTE #########################

@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('aboutus.html')






########## DEEPOPTICS ROUTE ####################

@app.route('/deepoptics', methods=['GET','POST'])
def deepoptics():
    return render_template('deepoptics.html')






############ PRODUCTS ROUTE #######################

@app.route('/products', methods=['GET','POST'])
def products():
    return render_template('product.html')





############ BLOGS ROUTE ###########################

@app.route('/blogs', methods=['GET','POST'])
def blogs():
    return render_template('blogs.html')




@app.route('/privacy', methods=['GET','POST'])
def privacy():
    return render_template('privacypolicy.html')





@app.route('/termsncondition', methods=['GET','POST'])
def term():
    return render_template('termsncondition.html')












########### HIRING ROUTE ###########################

@app.route('/hiring', methods=['GET','POST'])
def hiring():
    return render_template('hiring.html')


@app.route('/forms', methods=['GET','POST'])
def forms():
    return render_template('form.html')

########  ROUTE FORM IN HIRING #############

@app.route('/hireopening' , methods=['GET','POST'])
def hireform():
    if request.method == "POST":
        name=request.form.get('fullname')
        email=request.form.get('email')
        phone_no=request.form.get('tel')
        location=request.form.get('location')
        experience=request.form.get('experience')
        expected_ctc=request.form.get('number')
        pic=request.files['inputfile']
        filename=secure_filename(pic.filename)
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        entry = HiringForm(name=name, email=email, phone_no=phone_no,location=location,experience=experience,expected_ctc=expected_ctc,filename=filename)
        db.session.add(entry)
        db.session.commit()
        flash("Applied Successfully")
        print("store ho gya")
        msg = Message('deepak',recipients=['rushhabhh@gmail.com'],sender=email)
        # msg.body= "hello  data"
        # msg.html= "helllllll world" 
        # file=uploaded_file(filename)
        # with app.open_resource(filename) as filename:
        #     msg.attach(filename,'pdf/.pdf',filename.read())
        msg.body="Name   :  " + name + "\n" +  "Email   :  " + email + "\n" + "Phone Number  :  " + phone_no + "\n" + " Location  :  "  + location + "\n" + " Experience  :  "  + experience + "\n" + " Expected_CTC  :  "  + expected_ctc
        
        with app.open_resource('fileuploads/'+ filename) as Resume:
            msg.attach(filename,'pdf/.pdf',Resume.read())
        mail.send(msg)
        
        print("POST METHOD CHAL GYA")
        # return ("<h1>FILE SAVED SUCESSFULLY<h1>")
        return render_template('hiring.html')
    else:
        return render_template('hiring.html')


def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)





########## CONTACT US ROUTE ###############

@app.route('/contactus', methods=['GET','POST'])
def contact():
    if request.method == "POST":
        name=request.form.get('Name')
        company_name=request.form.get('Company_Name')
        email=request.form.get('email')
        contact_no=request.form.get('contact')
        message=request.form.get('subject')
        entry = Contact_Us_Form(name=name, company_name=company_name, email=email,contact_no=contact_no,message=message)
        db.session.add(entry)
        db.session.commit()
        print("chal gya")
        flash("Message Sent Successfully")
        mail.send_message('Message From  ' + name + " " + company_name,
                      sender=email,
                      recipients=['rushhabhh@gmail.com'],
                      body="Name   :  " + name+ "\n" + "Company Name   :  " + company_name+ "\n" + "Email   :  " + email + "\n" + "Contact No  :  " + contact_no+ "\n" + "Message  :  " + message)
        print("post method")
        # return ("<h1>SENT SUCESSFULLY</h1>")
        return render_template('contactus.html')
    else:
        print("GET METHOD RUNNING")
        return render_template('contactus.html')







##############################################newform###########


@app.route('/consult', methods=['GET','POST'])
def consult():
   if request.method == "POST":
        email=request.form.get('consult')
        entry = ConsultationForm(email=email)
        db.session.add(entry)
        db.session.commit()
        flash("Consultation Request Sent Successfully")
        mail.send_message('Request From  ' + email ,
                      sender=email,
                      recipients=['rushhabhh@gmail.com'],
                      body="EMAIL   :  " +email )
        print("POST METHOD CHAL GYA")
  
        # return ("<h1>REQUEST SENT SUCCESFULLY<h1>")
        return render_template('index.html')
   else:
       return render_template('index.html')
























################################### DATABASE MODEL #############################









#### FOR "/contact" ROUTE ####
#### CONTACTUS BACKEND DATABASE MODEL ######

class Contact_Us_Form(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    company_name=db.Column(db.String, nullable=False)
    email=db.Column(db.String,nullable=False)
    contact_no=db.Column(db.Integer,nullable=False)
    message=db.Column(db.String,nullable=False)

def __repr__(self):
    return 'QUERY'+ self.name














##### FOR "/" ROUTE  #######
##### REQUEST DEMO FORM BACKEND DATABASE MODEL ####

class Request_Demo_Form(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    company_name=db.Column(db.String, nullable=False)
    email=db.Column(db.String,nullable=False)
    contact=db.Column(db.Integer,nullable=False)















##### FOR '/hiring' ROUTE ########
###### VIEW OPENING FORM BACKEND DATABASE MODEL #####

class HiringForm(db.Model):

    sno= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)
    phone_no=db.Column(db.Integer,nullable=False)
    location=db.Column(db.String,nullable=False)
    experience=db.Column(db.Integer, nullable=False)
    expected_ctc=db.Column(db.Integer,nullable=False)
    # Use flask-file-upload's `file_upload.Column()` to associate a file with a SQLAlchemy Model:
    # data= file_upload.Column()
    filename=db.Column(db.String,nullable=False)




class ConsultationForm(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String,nullable=False)

















if __name__=="__main__":
    app.run(debug=True)