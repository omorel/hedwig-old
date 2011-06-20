import transaction
import usertools
import constants

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import DateTime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class DbUser(Base):
	"""DbUser class"""
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True, nullable=False)
	username = Column(Unicode(255), unique=True, nullable=False)
	email = Column(Unicode(255), unique=True, nullable=False)
	password = Column(Unicode(255), nullable=False)
	salt = Column(Unicode(255), nullable=False)
	creation_date = Column(DateTime, nullable=False)
	last_connection_date = Column(DateTime, nullable=False)
	last_synchro_date = Column(DateTime, nullable=False)
	status = Column(Integer, index=True, nullable=False)

	def __init__(self, username):
		self.username = username
		self.creation_date = datetime.now()
		self.last_connection_date = datetime.now()
		self.last_synchro_date = datetime.now()
		self.status = constants.USER_STATUS_DISABLED
		
	def __repr__(self):
		return "DbUser(id=%r,username=%r,email=%r,status=%r)" % (self.id, self.username, self.email, self.status)
		
	def set_status(self, status):
		self.status = status
		
	def set_password(self, password, salt):
		self.password = password 
		self.salt = salt
        

class User():
	"""User class"""
	def __init__(self, username):
		self.session = DBSession()
		self.dbuser = None
		if(usertools.is_username_valid(username)): 
			self.username = username		

	def set_status(status):
		self.dbuser.set_status(status)
	
	def is_active(): 
		return (self.dbuser.status == constants.USER_STATUS_ACTIVE)
		
	def create(self, email, password):
		valid = True
		if(usertools.is_username_valid(getattr(self, 'username', ''))): 
			self.dbuser = DbUser(getattr(self, 'username', ''))
		else:
			self.username = ''
			valid = False 
		
		if(valid and usertools.is_email_valid(email)): 
			self.dbuser.email = email
		else:
			valid = False 
			
		if(valid and usertools.is_password_valid(password)): 
			salt = usertools.generate_salt()
			encrypted_password = usertools.create_password(self.dbuser.username, salt, self.dbuser.email, password)
			self.dbuser.set_password(encrypted_password, salt)
		else:
			valid = False 
			
		if (valid): 
			return self.insert()
		else:
			return False
		
	def change_password(self, password):
		if (usertools.is_password_valid(password)): 
			salt = usertools.generate_salt()
			encrypted_password = usertools.create_password(self.username, salt, self.email, password)
			dbuser.set_password(encrypted_password, salt)
			return self.update
		else: 
			return False
			
	def update(self):
		try:
			#TODO: change self.session(self.dbuser) 
			self.session.commit()
			return True
		except :
			self.session.rollback()
			return False		
			
	def insert(self):
		try: 
			self.session.add(self.dbuser)
			self.session.flush()
			transaction.commit()
			return True 
		except: 
			self.session.rollback()
			return False 
			
	def load(self):
		self.session.query(DbUser).filter(DbUser.username==self.username).first()
		
	def check_password(password):
		if (usertools.is_password_valid(password)): 
			pass
	 	else: 
			return False 


def populate():
	user = User(u'omorel')
	if (user.create(u'omorel@gmail.com', u'')):
		print ("success")
    
def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        DBSession.rollback()
