from flask import Flask, render_template, url_for , redirect, flash, request, abort
from datetime import datetime, timezone
from functools import wraps

# IMPORTING FOR LAB FOR ENV FILE 
import os
from dotenv import load_dotenv

#IMPORTING FORMS FROM forms.py
from forms import LoginForm, RegisterForm, CampaignForm, DonateForm, ProfileForm, PasswordForm

# IMPORTING TOOLS FOR HASHING PASSWORD
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, LoginManager, UserMixin, login_user, logout_user

# IMPORTING FOR DATABASE
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpora_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db= SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login_page'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def admin_only(f):
    @wraps(f)
    def check_admin(*args,**kwargs):
        if not current_user.is_authenticated:
            abort(403)
        if not current_user.id == 1:
            abort(403)

        return f(*args, **kwargs)

    return check_admin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer , primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    campaigns: Mapped[list["Campaign"]] = relationship('Campaign',backref='user' , lazy=True)
    donations: Mapped[list["Donation"]] = relationship('Donation', backref='donator', lazy=True)


class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    goal_amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    donations: Mapped[list["Donation"]] = relationship('Donation', backref='campaign', lazy=True)

class Donation(db.Model):
    __tablename__ = 'donations'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    donated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    donator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    campaign_id: Mapped[int] = mapped_column(ForeignKey('campaigns.id'))

with app.app_context():
    db.create_all()

### ROUTES FOR ALL USERS


@app.route('/')
def homepage():
    query = db.select(Campaign)
    campaigns = db.session.scalars(query).all()
    return render_template('homepage.html', campaigns=campaigns)

@app.route('/all-campaigns')
def all_campaigns():

    category = request.args.get('category')

    query = db.select(Campaign).where(
        Campaign.status == 'approved'
    )

    if category:
        query = query.where(
            Campaign.category == category
        )

    campaigns = db.session.scalars(query).all()

    return render_template(
        'all_campaigns.html',
        campaigns=campaigns,
        category=category
    )


@app.route('/single-campaign/<int:campaign_id>')
def single_campaign(campaign_id):
    campaign = db.get_or_404(Campaign, campaign_id)
    return render_template('single_campaign.html', campaign=campaign)

@app.route('/about')
def about_page():
    return render_template('about_page.html')


@app.route('/login' , methods=['GET','POST'])
def login_page():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_email = login_form.email.data
        user_password = login_form.password.data

        user_exists = db.session.scalar(db.select(User).where(User.email == user_email))
        if not user_exists:
            flash("User with this email does not exist!")
            return redirect(url_for('login_page'))

        if not check_password_hash(user_exists.password, user_password):
            flash("Incorrent password!")
            return redirect(url_for('login_page'))

        login_user(user_exists)
        return redirect(url_for('homepage'))
        
    return render_template('login_page.html', form=login_form)



@app.route('/register', methods=['GET', 'POST'])
def register_page():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        new_name = register_form.name.data
        new_email = register_form.email.data
        new_password = register_form.password.data

        user_exists = db.session.scalar(db.select(User).where(User.email == new_email))
        if user_exists:
            flash('This email is already taken!')
            return redirect(url_for('register_page'))


        hashed_password = generate_password_hash(new_password)

        new_user = User(
            name=new_name,
            email=new_email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('homepage'))


    return render_template('register_page.html', form=register_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/add-campaign', methods=['GET', 'POST'])
@login_required
def add_campaign():
    campaign_form = CampaignForm()

    if campaign_form.validate_on_submit():

        image = campaign_form.image.data

        if  not image:
            flash('Please enter an image file')
            return redirect(url_for('add_campaign'))
        
        filename = image.filename

        
        image.save(
            os.path.join(
                app.root_path,
                'static',
                'uploads',
                filename
            )
        )

        if current_user.id == 1:
            campaign_status = 'approved'
        else:
            campaign_status = 'pending'

        new_campaign = Campaign(
            title=campaign_form.title.data,
            description=campaign_form.description.data,
            category=campaign_form.category.data,
            goal_amount=campaign_form.goal_amount.data,
            image_url=filename,
            status=campaign_status,
            user=current_user
        )

        db.session.add(new_campaign)
        db.session.commit()

        return redirect(url_for('homepage'))

    return render_template(
        'add_campaign_form.html',
        form=campaign_form
    )

@app.route('/my-profile')
@login_required
def my_profile():
    return render_template('my_profile.html')

@app.route('/donate/<int:campaign_id>', methods=['GET','POST'])
@login_required
def donate(campaign_id):
    campaign = db.get_or_404(Campaign, campaign_id)
    donate_form = DonateForm()
    if donate_form.validate_on_submit():
        new_donation = Donation(
            amount=donate_form.amount.data,
            donator=current_user,
            campaign=campaign
        )

        db.session.add(new_donation)
        db.session.commit()

        return redirect(url_for('success_donate'))
    return render_template('donate.html', campaign=campaign, form=donate_form)

@app.route('/successfully-donated')
def success_donate():
    return render_template('success_donate.html')

@app.route('/profile-settings', methods=['GET','POST'])
@login_required
def settings():
    password_form = PasswordForm()
    profile_form = ProfileForm()


    if profile_form.submit.data and profile_form.validate_on_submit():
        user = db.get_or_404(User, current_user.id)
        user.name = profile_form.name.data
        user.email = profile_form.email.data

        db.session.commit()
        return redirect(url_for('my_profile'))

    if password_form.submit.data and password_form.validate_on_submit():
        user = db.get_or_404(User, current_user.id)

        if check_password_hash(user.password , password_form.current_password.data):

            user.password = generate_password_hash(password_form.new_password.data)
            db.session.commit()
        return redirect(url_for('my_profile'))


    return render_template('profile_settings.html', password_form=password_form, profile_form=profile_form)



@app.route('/delete-account',methods=['POST'])
@login_required
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return redirect(url_for('homepage'))


###################################
### END OF ROUTES FOR ALL USERS ####
###################################

@app.route('/admin')
@admin_only
def admin():
    pending_query = db.select(Campaign).where(Campaign.status == "pending")
    pending_campaigns = db.session.scalars(pending_query).all()

    approved_query = db.select(Campaign).where(Campaign.status == 'approved')
    approved_campaigns = db.session.scalars(approved_query).all()

    users = db.session.scalars(db.select(User)).all()
    all_campaigns = db.session.scalars(db.select(Campaign)).all()
    all_donations = db.session.scalars(db.select(Donation)).all()

    return render_template('admin.html', pending_campaigns=pending_campaigns, approved_campaigns=approved_campaigns, users=users, all_campaigns=all_campaigns, all_donations=all_donations)

@app.route('/campaign/<int:campaign_id>/status/<action>')
@admin_only
def change_status(campaign_id, action):
    campaign = db.session.get(Campaign, campaign_id)

    if action == 'approve':
        campaign.status = 'approved'
    else:
        campaign.status = 'reject'

    db.session.commit()

    return redirect(url_for('admin'))


@app.route('/edit-campaign/<int:campaign_id>', methods=['GET','POST'])
@login_required
def edit_campaign(campaign_id):
    campaign = db.get_or_404(Campaign, campaign_id)

    if current_user.id == campaign.user_id or current_user.id == 1:
        form = CampaignForm(obj=campaign)

        if form.validate_on_submit():
            campaign.title = form.title.data
            campaign.description = form.description.data
            campaign.category = form.category.data
            campaign.goal_amount = form.goal_amount.data

            image = form.image.data

            if image:
                filename = image.filename

                image.save(
                    os.path.join(
                        app.root_path,
                        'static',
                        'uploads',
                        filename
                    )
                )

                campaign.image_url = filename

            

            db.session.commit()

            if current_user.id == 1:
                return redirect(url_for('admin'))

            return redirect(url_for('my_profile'))

        return render_template('edit.html', form=form, campaign=campaign)

    return abort(403)

@app.route('/delete-campaign/<int:campaign_id>',  methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    campaign = db.get_or_404(Campaign, campaign_id)


    if current_user.id == 1:
        db.session.delete(campaign)
        db.session.commit()
        return redirect(url_for('admin'))

    if current_user.id == campaign.user_id:
        db.session.delete(campaign)
        db.session.commit()
        return redirect(url_for('my_profile'))




if __name__ == "__main__":
    app.run(debug=True)