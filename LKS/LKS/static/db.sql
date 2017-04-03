Create table log_pass(user_id VARCHAR(6) PRIMARY KEY, login VARCHAR(60) NOT NULL, password VARCHAR(60) NOT NULL, role int not null);

Create table comands(comand_id VARCHAR(6) PRIMARY KEY, name Varchar(60) not null,  grad1 int , grad2 int, nomination varchar (30) NOT NULL);

CREATE TABLE judge(judge_id int Primary Key,
                   user_id VARCHAR(6) REFERENCES log_pass NOT NULL ,
                   comand_id VARCHAR(6) REFERENCES comands NOT NULL,
                   technique int, production int, teamwork int,artistry int,
                   musicality int,show int,creativity int);
-- ---------------------------------------------------------------------------------------------------------------------------------------------
Alter Table comands Add Column C_order int unique ;
Alter Table comands Add Column C_order2 int unique ;
Alter Table log_pass Add Column name VARCHAR(45) unique ;
Alter Table judge Add Column sum int ;

-- --------
Alter table judge add column final bool not null;

Create or replace function judgesum() RETURNS TRIGGER AS
$BODY$
BEGIN
UPDATE comands SET grad1=grad1+new.technique+new.production+new.teamwork+new.artistry+new.musicality+new.show+new.creativity
WHERE comand_id=new.comand_id and final='0';
RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

DELETE FROM JUDGE;
CREATE TRIGGER sumgrad
after insert on judge for each row execute procedure judgesum();
SELECT * FROM log_pass;
SELECT * FROM comands ;
SELECT * FROM judge;
INSERT INTO judge VALUES(2,'101010','101010',10,10,10,10,10,10,10,0,'0');

ALTER TABLE judge ADD CONSTRAINT unqi UNIQUE (user_id,comand_id,final);

-- --------- NEW function to Nastya
Create or replace function judgesum() RETURNS TRIGGER AS
$BODY$
BEGIN
IF new.final='0' then
UPDATE comands SET grad1=grad1+new.technique+new.production+new.teamwork+new.artistry+new.musicality+new.show+new.creativity
WHERE comand_id=new.comand_id and new.final='0';
ELSE
UPDATE comands SET grad2=grad2+new.technique+new.production+new.teamwork+new.artistry+new.musicality+new.show+new.creativity
WHERE comand_id=new.comand_id and new.final='1';
END IF;
RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;


Select MAX(c_order) from comands Natural join judge WHERE user_id='101010';


CREATE or replace function judgeupdate() RETURNS TRIGGER AS
$BODY$
BEGIN
IF old.final='0' then
UPDATE comands SET grad1=grad1+new.technique+new.production+new.teamwork+new.artistry+new.musicality+new.show+new.creativity-old.technique-old.production-old.teamwork-old.artistry-old.musicality-old.show-old.creativity WHERE comand_id=old.comand_id and old.final='0';
ELSE
UPDATE comands SET grad2=grad2+new.technique+new.production+new.teamwork+new.artistry+new.musicality+new.show+new.creativity -old.technique-old.production-old.teamwork-old.artistry-old.musicality-old.show-old.creativity WHERE comand_id=old.comand_id and old.final='1';
End IF;
RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER upgrad
after update on judge for each row execute procedure judgeupdate();
--------------------------------
insert into comands values('111111', 'comtest', 0, 0, 'kids', 1);
Create or replace function judgesum() RETURNS TRIGGER AS
$BODY$
BEGIN
UPDATE comands SET grad1=grad1+new.technique+new.production+new.teamwork+new.artistry+new.musicality+new.show+new.creativity
WHERE comand_id=new.comand_id and final='0';
RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER sumgrad
after insert on judge for each row execute procedure judgesum();

ALTER TABLE judge ADD CONSTRAINT unqi UNIQUE (user_id,comand_id,final);

Create or replace function judgesum() RETURNS TRIGGER AS
$BODY$
BEGIN
IF new.final='0' then
UPDATE comands SET grad1=grad1+new.technique+new.production+new.teamwork+new.artistry+new.musicality+new.show+new.creativity
WHERE comand_id=new.comand_id and new.final='0';
ELSE
UPDATE comands SET grad2=grad2+new.technique+new.production+new.teamwork+new.artistry+new.musicality+new.show+new.creativity
WHERE comand_id=new.comand_id and new.final='1';
END IF;
RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TYPE test1 AS (id varchar(6));

CREATE FUNCTION test() RETURNS test1
   AS $$ SELECT array_to_string(ARRAY(SELECT chr((65 + round(random() * 25)) :: integer)FROM generate_series(1,6)), ''); $$
   LANGUAGE SQL;


CREATE or replace function judgeupdate() RETURNS TRIGGER AS
$BODY$
BEGIN
IF old.final='0' then
UPDATE comands SET grad1=grad1+new.technique+new.production+new.teamwork+new.artistry+new.musicality+new.show+new.creativity-old.technique-old.production-old.teamwork-old.artistry-old.musicality-old.show-old.creativity WHERE comand_id=old.comand_id and old.final='0';
ELSE
UPDATE comands SET grad2=grad2+new.technique+new.production+new.teamwork+new.artistry+new.musicality+new.show+new.creativity -old.technique-old.production-old.teamwork-old.artistry-old.musicality-old.show-old.creativity WHERE comand_id=old.comand_id and old.final='1';
End IF;
RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER upgrad
after update on judge for each row execute procedure judgeupdate();
