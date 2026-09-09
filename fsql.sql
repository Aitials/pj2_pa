#初始脚本，创建数据库和表结构

create database pj2_pachong;
USE pj2_pachong;

create table videos (
    aid char(15) primary key not null ,
    tname varchar (20) not null ,
    title varchar(150) not null ,
    deses varchar(500),
    author varchar(50) not null ,
    view int not null ,
    reply int not null ,
    ulike int not null ,
    favorite int not null ,
    share int not null ,
    coin int not null

);

#测试区
#drop table videos

