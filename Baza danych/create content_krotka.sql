create table content_krotka (	
	content_ID int(8) auto_increment not null primary key, 
    content_name varchar(24) not null,
    content_info varchar(256),
    img_src varchar(64) not null,
    levels int(3) not null,
    time int(16) not null
    );
							