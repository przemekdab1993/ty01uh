create table fields_user 
(	user_ID int(12) not null,
	krotka_ID int(8) not null,
    content_ID int(8) not null,
    counter int(3) not null,
    time_out int(16) ,
    
    foreign key (user_ID) references user_game(user_ID),
    foreign key (content_ID) references content_krotka(content_ID)
    );
    