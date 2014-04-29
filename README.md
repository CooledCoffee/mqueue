Introduction
============

MQueue is a simple task queue implementation based on mysql.

Installation
============

pip install mqueue

Tasks
=====

First, we need a table to store the tasks:

	create table task (
		id int primary key auto_increment,
		args text not null,
		eta datetime not null,
		name varchar(128) not null,
		queue varchar(32) not null,
		retries tinyint not null
	);
	
Second, we define a task by creating a tasks module:

	from mqueue import task
	
	@task
	def mail(receiver, subject, body):
	    print('Send mail')
	    
Init the queue and enqueue the task:

	from sqlalchemy_dao import Dao
	import mqueue
	import tasks
	
    mqueue.init('test-queue')
	dao = Dao('mysql://test:test@localhost/website')
	with dao.SessionContext():
	    tasks.mail.enqueue('test@test.com', 'hello', 'This is a test mail.')

Now create a daemon module:

	from sqlalchemy_dao import Dao
	import mqueue
	
	dao = Dao('mysql://test:test@localhost/website')
    mqueue.start('test-queue', dao)
    
Start it with

	python daemon.py
	
And it is all done.

MQueue automatically loads all tasks under the tasks package.
This is where you should place all your tasks.

Crons
=====

In order to use cron jobs, you need another table in the database:

	create table cron (
		queue varchar(32),
		name varchar(128),
		last datetime not null,
		primary key (queue, name)
	);

A cron is a task that automatically enqueue itself according to its cron expression.

	from mqueue import cron
	
	@cron('0 * * * *')
	def mail():
	    print('Send mail')
	    
Cron jobs cannot have arguments because there is no way to specify them.
Besides, a cron job is enqueued according to its schedule,
but there is no gurantee when the enqueued task will be processed.

Transaction
===========

Transaction is a very powerful feature of databases.
However, most queues do not support it.
Even if they do, you end up with distributed transaction which is very nasty to handle.

With MQueue, you can ensure that your database operations and queue operations are within the same transaction:

	def create_user(name, email)
	    dao = Dao('mysql://test:test@localhost/website')
	    with dao.SessionContext() as ctx:
	        user = User(name=name, email=email)
	        ctx.session.add(user)
	        tasks.mail.enqueue(email, 'Hello', 'Welcome on board.')
	        
When a task got run, the session context has been set up for you.
You just have to use it in your code:

	from decorated.base.context import ctx
	from mqueue import task
	
	@task
	def mail(email, subject, body):
	    # send an email
	    ...
	    user = ctx.session.query(User).filter(User.email == email).one()
	    user.email_sent = True
	    
Check out <a href="https://github.com/CooledCoffee/sqlalchemy-dao" target="_blank">SQLAlchemy-Dao</a>
for more information about daos and session contexts.

Author
======

Mengchen LEE: <a href="https://plus.google.com/117704742936410336204" target="_blank">Google Plus</a>, <a href="https://cn.linkedin.com/pub/mengchen-lee/30/8/23a" target="_blank">LinkedIn</a>
