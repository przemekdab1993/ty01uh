create table user_game ( 
	user_ID INT(12) PRIMARY KEY AUTO_INCREMENT,
	user_name VARCHAR(24) NOT NULL, 
	user_password VARCHAR(24) NOT NULL,
	email varchar(64) not null,
	action_punkts int(8) not null,
	lvl int(4) not null,
	experience int(24) not null,
	silver_coins int(24) not null,
	gold_coins int(24) not null,
	premium_day int(16) not null,
	date_reg timestamp default current_timestamp
	);
