create table cron (
	queue varchar(32),
	name varchar(128),
	last datetime,
	schedule varchar(64),
	primary key (queue, name)
);

create table task (
	id int primary key auto_increment,
	args text not null,
	eta datetime not null,
	name varchar(128) not null,
	queue varchar(32) not null,
	retries tinyint not null
);
