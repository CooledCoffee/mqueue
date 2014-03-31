Introduction
============

MQueue is a simple task queue implementation based on mysql.

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
	
	dao = Dao('mysql://test:test@localhost/queue')
    mqueue.init('test-queue', dao)
	tasks.mail.enqueue('test@test.com', 'hello', 'This is a test mail.')

Now create a daemon module:

	from sqlalchemy_dao import Dao
	import mqueue
	
	dao = Dao('mysql://test:test@localhost/queue')
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

Author
======

Mengchen LEE: <a href="https://plus.google.com/117704742936410336204" target="_blank">Google Plus</a>, <a href="https://cn.linkedin.com/pub/mengchen-lee/30/8/23a" target="_blank">LinkedIn</a>
