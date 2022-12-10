text("""
    use capstone;

    create table REVIEW (
     SEQ int(11) NOT NULL AUTO_INCREMENT,
     ID varchar(50) NOT NULL,
     CONTENT varchar(200) NOT NULL,
     CREATED_AT datetime DEFAULT current_timestamp(),
     USERNAME varchar(30),
     SOURCE_TYPE varchar(20),
     LIKE_COUNT int(11),
     PRIMARY KEY (SEQ)
     )default character set utf8 collate utf8_general_ci;
    """
